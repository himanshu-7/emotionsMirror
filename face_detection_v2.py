########### Python 2.7 #############
import httplib, urllib, base64, json, requests, time, urllib

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

headers = {
    'Content-Type': 'application/json'
}

params = urllib\
    .urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': '',
})


raw_input("Press Enter to continue...")
resource = urllib.urlopen("http://192.168.1.39:8080/photo.jpg")
output = open("file01.jpg", "wb")
output.write(resource.read())
output.close()

body1 = ""
filename = 'file01.jpg'
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
        #login and get token
        data_2 = '{"method": "login","params": { "appType": "Kasa_Android", "cloudPassword" : "15111992k","cloudUserName": "himanshu.7.shah@gmail.com", "terminalUUID": "e36193be-f046-43d4-9669-ceab734b05a3"}}'
        response = requests.post('https://wap.tplinkcloud.com/', headers=headers, data=data_2)
        r = response.json()
        print ("%s" %r)
        token1 = r['result']['token']
        print ("%s" %token1)

        #get device list
        data_3 = '{"method": "getDeviceList","params": {}}'
        response = requests.post('https://wap.tplinkcloud.com/?token=%s'%token1,headers=headers, data=data_3)
        r = response.json()
        print ("%s" %r)
        device1 = r['result']['deviceList'][0]['deviceId']
        print ("%s" %device1)

        #turn lamp on
        data_4 = '{"method":"passthrough", "params": {"deviceId": "8012C3C1DED0BCD794179E8675A70FE9189105B5", "requestData": "{\\"smartlife.iot.smartbulb.lightingservice\\":{\\"transition_light_state\\":{\\"on_off\\":1}}}" }}'
    	response = requests.post('https://wap.tplinkcloud.com/?token=%s'%token1,headers=headers, data=data_4)
    	r = response.text
    	print ("%s" %r)

        #wait for some time
        time.sleep(10)

        data_4 = '{"method":"passthrough", "params": {"deviceId": "8012C3C1DED0BCD794179E8675A70FE9189105B5", "requestData": "{\\"smartlife.iot.smartbulb.lightingservice\\":{\\"transition_light_state\\":{\\"on_off\\":0}}}" }}'
    	response = requests.post('https://wap.tplinkcloud.com/?token=%s'%token1,headers=headers, data=data_4)
    	r = response.text
    	print ("%s" %r)

    else:
        print("Different person")
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
