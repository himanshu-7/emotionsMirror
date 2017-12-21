import requests

import time
headers = {
    'Content-Type': 'application/json',
}

#hello world
data_1 = '{"method": "helloCloud","params": { "appPackageName": "com.tplink.kasa_android", "appType": "Kasa_Android", "tcspVer" : 1.1, "terminalUUID": "e36193be-f046-43d4-9669-ceab734b05a3"}}'
response = requests.post('https://wap.tplinkcloud.com/', headers=headers, data=data_1)


#get token
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

while 1:

	#	data_4 ='{"method": "passthrough", "params":{"deviceId": "8012C3C1DED0BCD794179E8675A70FE9189105B5","requestData": json.dumps()}'
	data_4 = '{"method":"passthrough", "params": {"deviceId": "8012C3C1DED0BCD794179E8675A70FE9189105B5", "requestData": "{\\"smartlife.iot.smartbulb.lightingservice\\":{\\"transition_light_state\\":{\\"on_off\\":1}}}" }}'
	response = requests.post('https://wap.tplinkcloud.com/?token=%s'%token1,headers=headers, data=data_4)
	r = response.text
	print ("%s" %r)

	time.sleep(5)

	#	data_4 ='{"method": "passthrough", "params":{"deviceId": "8012C3C1DED0BCD794179E8675A70FE9189105B5","requestData": json.dumps()}'
	data_4 = '{"method":"passthrough", "params": {"deviceId": "8012C3C1DED0BCD794179E8675A70FE9189105B5", "requestData": "{\\"smartlife.iot.smartbulb.lightingservice\\":{\\"transition_light_state\\":{\\"on_off\\":0}}}" }}'
	response = requests.post('https://wap.tplinkcloud.com/?token=%s'%token1,headers=headers, data=data_4)
	r = response.text
	print ("%s" %r)
	time.sleep(5)
