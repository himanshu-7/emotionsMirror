########### Python 2.7 #############

# Implementation of this script is unclear and this is been lying around since the first commit.
# Clean this up when/if not required
import httplib, urllib, base64

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'YOUR_HEX_KEY',
}

params = urllib.urlencode({
})

# Replace the example URL below with the URL of the image you want to analyze.
body = "{ 'url': 'https://www.cynthiacorsetti.com/wp-content/uploads/2011/05/cynthiacorsetti-com-five-tips-for-keeping-emotions-in-check-at-work.jpg' }"

try:
    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
    #   URL below with "westcentralus".
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
