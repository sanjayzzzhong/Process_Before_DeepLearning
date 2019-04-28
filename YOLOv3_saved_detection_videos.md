# 保存YOLOv3的检测视频
> 官网项目在测试本地视频或通过摄像头(webcam)获得的视频时，默认是没有保存运行结果的，因此这里主要讲的是如何保存yolo3运行检测的视频结果。


**假设你的项目路径为`./darknet`，需要改动的主要有两个文件，
分别是位于`./darknet/src/`路径下的`demo.c`和`image.c`文件**

1. 首先在image.c文件中添加save_video的定义，代码及注释如下：
```c
void save_video(image p, CvVideoWriter *mVideoWriter)
{
    //复制传入的图片到copy
    image copy = copy_image(p);
    //如果图片是三通道的，
    if(p.c == 3) 
        rgbgr_image(copy);
    int x, y, k;

    IplImage *disp = cvCreateImage(cvSize(p.w,p.h), IPL_DEPTH_8U,p.c);
    int step = disp->widthStep;
    for(y = 0; y < p.h; ++y){
        for (x = 0; x < p.w; ++x){
            disp->imageData[y*step + x*p.c + k] = (unsigned char)(get_pixel(copy, x, y, k) * 255);
        }
    }
    cvWriterFrame(mVideoWriter, disp);
    cvReleaseImage(&disp);
    free_image(copy);
}
```

插入位置如下：   
![插入位置](https://img-blog.csdn.net/20180416191717105)   

2. 然后更改demo.c文件代码 

**由于改动内容有多处，因此这里帖是完整的demo.c文件代码，每一组
``//*********rs20180415***********``之间代码就是新添加的代码内容，可自行对比，包括设置你输出检测视频的名称和帧率。**

```c
#include "network.h"
#include "detection_layer.h"
#include "region_layer.h"
#include "cost_layer.h"
#include "utils.h"
#include "parser.h"
#include "box.h"
#include "image.h"
#include "demo.h"
#include <sys/time.h>
 
#define DEMO 1
 
//*********rs20180415***********start
#define SAVEVIDEO
//*********rs20180415***********end
 
#ifdef OPENCV
 
//*********rs20180415***********start
#ifdef SAVEVIDEO
   static CvVideoWriter *mVideoWriter;
#endif
//*********rs20180415***********end
 
static char **demo_names;
static image **demo_alphabet;
static int demo_classes;
static network *net;
static image buff [3];
static image buff_letter[3];
static int buff_index = 0;
static CvCapture * cap;
static IplImage  * ipl;
static float fps = 0;
static float demo_thresh = 0;
static float demo_hier = .5;
static int running = 0;
 
static int demo_frame = 3;
static int demo_index = 0;
static float **predictions;
static float *avg;
static int demo_done = 0;
static int demo_total = 0;
double demo_time;
 
detection *get_network_boxes(network *net, int w, int h, float thresh, float hier, int *map, int relative, int *num);
 
int size_network(network *net)
{
    int i;
    int count = 0;
    for(i = 0; i < net->n; ++i){
        layer l = net->layers[i];
        if(l.type == YOLO || l.type == REGION || l.type == DETECTION){
            count += l.outputs;
        }
    }
    return count;
}
 
void remember_network(network *net)
{
    int i;
    int count = 0;
    for(i = 0; i < net->n; ++i){
        layer l = net->layers[i];
        if(l.type == YOLO || l.type == REGION || l.type == DETECTION){
            memcpy(predictions[demo_index] + count, net->layers[i].output, sizeof(float) * l.outputs);
            count += l.outputs;
        }
    }
}
 
detection *avg_predictions(network *net, int *nboxes)
{
    int i, j;
    int count = 0;
    fill_cpu(demo_total, 0, avg, 1);
    for(j = 0; j < demo_frame; ++j){
        axpy_cpu(demo_total, 1./demo_frame, predictions[j], 1, avg, 1);
    }
    for(i = 0; i < net->n; ++i){
        layer l = net->layers[i];
        if(l.type == YOLO || l.type == REGION || l.type == DETECTION){
            memcpy(l.output, avg + count, sizeof(float) * l.outputs);
            count += l.outputs;
        }
    }
    detection *dets = get_network_boxes(net, buff[0].w, buff[0].h, demo_thresh, demo_hier, 0, 1, nboxes);
    return dets;
}
 
void *detect_in_thread(void *ptr)
{
    running = 1;
    float nms = .4;
 
    layer l = net->layers[net->n-1];
    float *X = buff_letter[(buff_index+2)%3].data;
    network_predict(net, X);
 
    /*
       if(l.type == DETECTION){
       get_detection_boxes(l, 1, 1, demo_thresh, probs, boxes, 0);
       } else */
    remember_network(net);
    detection *dets = 0;
    int nboxes = 0;
    dets = avg_predictions(net, &nboxes);
 
 
    /*
       int i,j;
       box zero = {0};
       int classes = l.classes;
       for(i = 0; i < demo_detections; ++i){
       avg[i].objectness = 0;
       avg[i].bbox = zero;
       memset(avg[i].prob, 0, classes*sizeof(float));
       for(j = 0; j < demo_frame; ++j){
       axpy_cpu(classes, 1./demo_frame, dets[j][i].prob, 1, avg[i].prob, 1);
       avg[i].objectness += dets[j][i].objectness * 1./demo_frame;
       avg[i].bbox.x += dets[j][i].bbox.x * 1./demo_frame;
       avg[i].bbox.y += dets[j][i].bbox.y * 1./demo_frame;
       avg[i].bbox.w += dets[j][i].bbox.w * 1./demo_frame;
       avg[i].bbox.h += dets[j][i].bbox.h * 1./demo_frame;
       }
    //copy_cpu(classes, dets[0][i].prob, 1, avg[i].prob, 1);
    //avg[i].objectness = dets[0][i].objectness;
    }
     */
 
 
 if (nms > 0) do_nms_obj(dets, nboxes, l.classes, nms);
 
    printf("\033[2J");
    printf("\033[1;1H");
    printf("\nFPS:%.1f\n",fps);
    printf("Objects:\n\n");
    image display = buff[(buff_index+2) % 3];
    draw_detections(display, dets, nboxes, demo_thresh, demo_names, demo_alphabet, demo_classes);
    free_detections(dets, nboxes);
 
    demo_index = (demo_index + 1)%demo_frame;
    running = 0;
    return 0;
}
 
void *fetch_in_thread(void *ptr)
{
    int status = fill_image_from_stream(cap, buff[buff_index]);
    letterbox_image_into(buff[buff_index], net->w, net->h, buff_letter[buff_index]);
    if(status == 0) demo_done = 1;
    return 0;
}
 
void *display_in_thread(void *ptr)
{
    show_image_cv(buff[(buff_index + 1)%3], "Demo", ipl);
    int c = cvWaitKey(1);
    if (c != -1) c = c%256;
    if (c == 27) {
        demo_done = 1;
        return 0;
    } else if (c == 82) {
        demo_thresh += .02;
    } else if (c == 84) {
        demo_thresh -= .02;
        if(demo_thresh <= .02) demo_thresh = .02;
    } else if (c == 83) {
        demo_hier += .02;
    } else if (c == 81) {
        demo_hier -= .02;
        if(demo_hier <= .0) demo_hier = .0;
    }
    return 0;
}
 
void *display_loop(void *ptr)
{
    while(1){
        display_in_thread(0);
    }
}
 
void *detect_loop(void *ptr)
{
    while(1){
        detect_in_thread(0);
    }
}
 
void demo(char *cfgfile, char *weightfile, float thresh, int cam_index, const char *filename, char **names, int classes, int delay, char *prefix, int avg_frames, float hier, int w, int h, int frames, int fullscreen)
{
    //demo_frame = avg_frames;
    image **alphabet = load_alphabet();
    demo_names = names;
    demo_alphabet = alphabet;
    demo_classes = classes;
    demo_thresh = thresh;
    demo_hier = hier;
    printf("Demo\n");
    net = load_network(cfgfile, weightfile, 0);
    set_batch_network(net, 1);
    pthread_t detect_thread;
    pthread_t fetch_thread;
 
    srand(2222222);
 
    int i;
    demo_total = size_network(net);
    predictions = calloc(demo_frame, sizeof(float*));
    for (i = 0; i < demo_frame; ++i){
        predictions[i] = calloc(demo_total, sizeof(float));
    }
    avg = calloc(demo_total, sizeof(float));
 
    if(filename){
        printf("video file: %s\n", filename);
        cap = cvCaptureFromFile(filename);
//*********rs20180415***********start
    #ifdef SAVEVIDEO
        if(cap){
            int mfps = cvGetCaptureProperty(cap,CV_CAP_PROP_FPS);   //local video file，needn't change
            mVideoWriter=cvCreateVideoWriter("Output.avi",CV_FOURCC('M','J','P','G'),mfps,cvSize(cvGetCaptureProperty(cap,CV_CAP_PROP_FRAME_WIDTH),cvGetCaptureProperty(cap,CV_CAP_PROP_FRAME_HEIGHT)),1);
        }
    #endif
//*********rs20180415***********end
    }else{
        cap = cvCaptureFromCAM(cam_index);
//*********rs20180415***********start
    #ifdef SAVEVIDEO
        if(cap){
            //int mfps = cvGetCaptureProperty(cap,CV_CAP_PROP_FPS);  //webcam video file，need change.
            int mfps = 25;     //the output video FPS，you can set here.
            mVideoWriter=cvCreateVideoWriter("Output_webcam.avi",CV_FOURCC('M','J','P','G'),mfps,cvSize(cvGetCaptureProperty(cap,CV_CAP_PROP_FRAME_WIDTH),cvGetCaptureProperty(cap,CV_CAP_PROP_FRAME_HEIGHT)),1);
        }
    #endif
//*********rs20180415***********end
        if(w){
            cvSetCaptureProperty(cap, CV_CAP_PROP_FRAME_WIDTH, w);
        }
        if(h){
            cvSetCaptureProperty(cap, CV_CAP_PROP_FRAME_HEIGHT, h);
        }
        if(frames){
            cvSetCaptureProperty(cap, CV_CAP_PROP_FPS, frames);
        }
    }
 
    if(!cap) error("Couldn't connect to webcam.\n");
 
    buff[0] = get_image_from_stream(cap);
    buff[1] = copy_image(buff[0]);
    buff[2] = copy_image(buff[0]);
    buff_letter[0] = letterbox_image(buff[0], net->w, net->h);
    buff_letter[1] = letterbox_image(buff[0], net->w, net->h);
    buff_letter[2] = letterbox_image(buff[0], net->w, net->h);
    ipl = cvCreateImage(cvSize(buff[0].w,buff[0].h), IPL_DEPTH_8U, buff[0].c);
 
    int count = 0;
    if(!prefix){
        cvNamedWindow("Demo", CV_WINDOW_NORMAL); 
        if(fullscreen){
            cvSetWindowProperty("Demo", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
        } else {
            cvMoveWindow("Demo", 0, 0);
            cvResizeWindow("Demo", 1352, 1013);
        }
    }
 
    demo_time = what_time_is_it_now();
 
    while(!demo_done){
        buff_index = (buff_index + 1) %3;
        if(pthread_create(&fetch_thread, 0, fetch_in_thread, 0)) error("Thread creation failed");
        if(pthread_create(&detect_thread, 0, detect_in_thread, 0)) error("Thread creation failed");
        if(!prefix){
//*********rs20180415***********start
            #ifdef SAVEVIDEO
                save_video(buff[0],mVideoWriter);    
            #endif
//*********rs20180415***********end
            fps = 1./(what_time_is_it_now() - demo_time);
            demo_time = what_time_is_it_now();
            display_in_thread(0);
        }else{
            char name[256];
            sprintf(name, "%s_%08d", prefix, count);
//*********rs20180415***********start
            #ifdef SAVEVIDEO
                  save_video(buff[0],mVideoWriter);
            #else
            save_image(buff[(buff_index + 1)%3], name);
            #endif
//*********rs20180415***********end
        }
        pthread_join(fetch_thread, 0);
        pthread_join(detect_thread, 0);
        ++count;
    }
}
 
/*
   void demo_compare(char *cfg1, char *weight1, char *cfg2, char *weight2, float thresh, int cam_index, const char *filename, char **names, int classes, int delay, char *prefix, int avg_frames, float hier, int w, int h, int frames, int fullscreen)
   {
   demo_frame = avg_frames;
   predictions = calloc(demo_frame, sizeof(float*));
   image **alphabet = load_alphabet();
   demo_names = names;
   demo_alphabet = alphabet;
   demo_classes = classes;
   demo_thresh = thresh;
   demo_hier = hier;
   printf("Demo\n");
   net = load_network(cfg1, weight1, 0);
   set_batch_network(net, 1);
   pthread_t detect_thread;
   pthread_t fetch_thread;
   srand(2222222);
   if(filename){
   printf("video file: %s\n", filename);
   cap = cvCaptureFromFile(filename);
   }else{
   cap = cvCaptureFromCAM(cam_index);
   if(w){
   cvSetCaptureProperty(cap, CV_CAP_PROP_FRAME_WIDTH, w);
   }
   if(h){
   cvSetCaptureProperty(cap, CV_CAP_PROP_FRAME_HEIGHT, h);
   }
   if(frames){
   cvSetCaptureProperty(cap, CV_CAP_PROP_FPS, frames);
   }
   }
   if(!cap) error("Couldn't connect to webcam.\n");
   layer l = net->layers[net->n-1];
   demo_detections = l.n*l.w*l.h;
   int j;
   avg = (float *) calloc(l.outputs, sizeof(float));
   for(j = 0; j < demo_frame; ++j) predictions[j] = (float *) calloc(l.outputs, sizeof(float));
   boxes = (box *)calloc(l.w*l.h*l.n, sizeof(box));
   probs = (float **)calloc(l.w*l.h*l.n, sizeof(float *));
   for(j = 0; j < l.w*l.h*l.n; ++j) probs[j] = (float *)calloc(l.classes+1, sizeof(float));
   buff[0] = get_image_from_stream(cap);
   buff[1] = copy_image(buff[0]);
   buff[2] = copy_image(buff[0]);
   buff_letter[0] = letterbox_image(buff[0], net->w, net->h);
   buff_letter[1] = letterbox_image(buff[0], net->w, net->h);
   buff_letter[2] = letterbox_image(buff[0], net->w, net->h);
   ipl = cvCreateImage(cvSize(buff[0].w,buff[0].h), IPL_DEPTH_8U, buff[0].c);
   int count = 0;
   if(!prefix){
   cvNamedWindow("Demo", CV_WINDOW_NORMAL); 
   if(fullscreen){
   cvSetWindowProperty("Demo", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
   } else {
   cvMoveWindow("Demo", 0, 0);
   cvResizeWindow("Demo", 1352, 1013);
   }
   }
   demo_time = what_time_is_it_now();
   while(!demo_done){
buff_index = (buff_index + 1) %3;
if(pthread_create(&fetch_thread, 0, fetch_in_thread, 0)) error("Thread creation failed");
if(pthread_create(&detect_thread, 0, detect_in_thread, 0)) error("Thread creation failed");
if(!prefix){
    fps = 1./(what_time_is_it_now() - demo_time);
    demo_time = what_time_is_it_now();
    display_in_thread(0);
}else{
    char name[256];
    sprintf(name, "%s_%08d", prefix, count);
    save_image(buff[(buff_index + 1)%3], name);
}
pthread_join(fetch_thread, 0);
pthread_join(detect_thread, 0);
++count;
}
}
*/
#else
void demo(char *cfgfile, char *weightfile, float thresh, int cam_index, const char *filename, char **names, int classes, int delay, char *prefix, int avg, float hier, int w, int h, int frames, int fullscreen)
{
    fprintf(stderr, "Demo needs OpenCV for webcam images.\n");
}
#endif
```

运行的过程，碰到了很多问题，比如在通过摄像头实时检测时，遇到了下面这个问题，这个错误不致命，就是可执行检测但是保存不了检测视频，错误提示如下：

`HIGHGUI ERROR： V4L/V4L2：VIDIOC_S_CROP`

`HIGHGUI ERROR： V4L/V4L2：getting property #5 is not supported`

`GLib-GIOMessage: Using the 'memory' GSettings backend.  Your settings will not be saved or shared with other applications`

如下图：
![](https://img-blog.csdn.net/20180416193312777)

* solution
    * 第一个问题   
    `HIGHGUI ERROR： V4L/V4L2：VIDIOC_S_CROP`
     `HIGHGUI ERROR： V4L/V4L2：getting property #5 is not supported`  
测试了下，是代码问题，上面给的代码已更改，主要在通过摄像头获取视频帧率时采用了：  
`//int mfps = cvGetCaptureProperty(cap,CV_CAP_PROP_FPS); `指令，这样是不行的，测试本地时可以，所以这里给帧率设置了一个常数：`int mfps = 25;`可以结合demo.c文件对应着看，给了相应的注释。

    * 第二个问题  
     `GLib-GIOMessage: Using the 'memory' GSettings backend.  Your settings will not be saved or shared with other applications. `     
需要添加一个路径，操作如下：  
        1. 在ubuntu终端执行：  
        `sudo gedit /etc/profile`  
        2. 然后在打开的文件内(需要sudo权限)添加下面内容： 
        `export GIO_EXTRA_MODULES=/usr/lib/x86_64-linux-gnu/gio/modules/ `
        3. 最后是上面的更改立即生效：  
        `source .bashrc`
