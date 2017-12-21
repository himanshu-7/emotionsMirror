########### Python 2.7 #############
import httplib, urllib, base64, json

headers_octet = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '6a4951f9624543d58a63634fe264e3e7',
}

headers_json = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '6a4951f9624543d58a63634fe264e3e7',
}


params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': '',
})
#
#body1 = F:\Python\emotions_mirror\emotionsMirror\200px-Katrina_Kaif.jpg
#body2 = F:\Python\emotions_mirror\emotionsMirror\220px-Katrina_Kaif.jpg

body1 = ""
# filename = 'F:\Python\emotions_mirror\emotionsMirror\Katrina_Kaif_1.jpg'
filename = 'himanshu_7.jpg'
f = open(filename, "rb")
body1 = f.read()
f.close()

body2 = ""
filename = 'himanshu_6.jpg'
f = open(filename, "rb")
body2 = f.read()
f.close()



try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body1, headers_octet)
    response1 = conn.getresponse()
    data1 = response1.read()
    print(data1)
        # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed1 = json.loads(data1)
    #print ("Response:")
    #print (json.dumps(parsed, sort_keys=True, indent=2))
    #print(parsed1[0]['faceId'])
    id1 = parsed1[0]['faceId']
    #conn.close()
    print(id1)
    print("did you reach here?")
    #conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body2, headers_octet)
    response2 = conn.getresponse()
    data2 = response2.read()
    print(data2)
        # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed2 = json.loads(data2)
    #print ("Response:")
    #print (json.dumps(parsed, sort_keys=True, indent=2))
    #print(parsed2[0]['faceId'])
    id2 = parsed2[0]['faceId']
    print(id2)

    params3 = urllib.urlencode({
    })
    body = "{'faceId1':'"+id1+"','faceId2':'"+id2+"'}"
        # print(body)

    conn.request("POST", "/face/v1.0/verify?%s" %params3, body, headers_json)
    response = conn.getresponse()
    data = response.read()
    print(data)
        # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
        # print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        # print(parsed['isIdentical'])
    if(parsed['isIdentical'] == True):
        print("Images are of same person.")
    else:
        print("Different person")
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
