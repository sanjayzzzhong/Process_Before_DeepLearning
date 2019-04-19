from requests import exceptions
import requests
import cv2
import os
import gevent

# poke name to download
pokemon = 'mewtwo'
output = 'datasets/mewtwo'

API_KEY = "375d7899eca84397aa2d182c5d97dd54"
MAX_RESULTS = 250
GROUP_SIZE = 50

# set the endpoint API URL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

# when attempting to download images from the web both the Python
# programming language and the requests library have a number of
# exceptions that can be thrown so let's build a list of them now
# so we can filter on them
EXCEPTIONS = {IOError, FileNotFoundError, exceptions.RequestException, exceptions.HTTPError, exceptions.ConnectionError,
              exceptions.Timeout}

# store the search term in a convenience variable then set the
# headers and search parameters
term = pokemon
headers = {"Ocp-Apim-Subscription-Key": API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

# make the search
print("[INFO] searching Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

# grab the results from the search, including the total number of
# estimated results returned by the Bing API
results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults, term))

# initialize the total number of images downloaded thus far
total = 0


def grab_page(url, ext, total):

    try:
        # total += 1
        print("[INFO] fetching: {}".format(url))
        r = requests.get(url, timeout=30)
        # build the path to the output image

        #here total is only for filename creation
        p = os.path.sep.join([output, "{}{}".format(
            str(total).zfill(8), ext)])

        # write the image to disk
        f = open(p, "wb")
        f.write(r.content)
        f.close()

        # try to load the image from disk
        image = cv2.imread(p)

        # if the image is `None` then we could not properly load the
        # image from disk (so it should be ignored)
        if image is None:
            print("[INFO] deleting: {}".format(p))
            os.remove(p)
            return

    # catch any errors that would not unable us to download the
    # image
    except Exception as e:
        # check to see if our exception is in our list of
        # exceptions to check for
        if type(e) in EXCEPTIONS:
            print("[INFO] skipping: {}".format(url))
            return

# loop over the estimated number of results in `GROUP_SIZE` groups
for offset in range(0, estNumResults, GROUP_SIZE):
    # update the search parameters using the current offset, then
    # make the request to fetch the results
    print("[INFO] making request for group {}-{} of {}...".format(
        offset, offset + GROUP_SIZE, estNumResults))
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    print("[INFO] saving images for group {}-{} of {}...".format(
        offset, offset + GROUP_SIZE, estNumResults))
    # loop over the results
    jobs = []
    for v in results["value"]:
        total += 1
        ext = v["contentUrl"][v["contentUrl"].rfind("."):]
        url = v["contentUrl"]
        
        # create gevent job
        jobs.append(gevent.spawn(grab_page, url, ext, total))

    # wait for all jobs to complete
    gevent.joinall(jobs, timeout=10)
    print(total)