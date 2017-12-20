########### Python 2.7 #############

import httplib, urllib, base64, json
import RPi.GPIO as GPIO
import time

# This script has been pulled from the repository at https://github.com/wyvette0542/ECE497_Final
# It does include some modifications for GPIOs to be controlled on a Raspberry Pi 3

# Part that Works:
# 1) Sending images to the cloud
# 2) Rpi GPIOs

# Doesn't work yet:
# 1) Debouncing.
# 2) Webcam feed
# 3) Safe termination resource Rpi: GPIO

# Yet to be implemented:
# 1) Latency calculations
# 2) Error free API calls and safe termination in case of occourance (absence of connection to the cloud etc.)

# Optimization:
# 1) Callbacks shouldn't have so much to do, it looks against its purpose. Use a queue to synchronize tasks.
# 2) Code structure, datatypes and loop structure. (Queues, Callbacks, structures, errors)
# 3) Change the Processor(PC/RPi) by a preprocessor macro

cnt = 0  # count for button presses
LedGPIO = 16
ButGPIO = 18

headers_octet = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'ENTER_KEY',
}

headers_json = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ENTER_KEY',
}

params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': '',
})

body2 = ""
filename = 'STATIC_IMAGE'
f = open(filename, "rb")
body2 = f.read()
f.close()


##########
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LedGPIO, GPIO.OUT)
    GPIO.setup(ButGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(LedGPIO, GPIO.LOW)
    GPIO.add_event_detect(ButGPIO, GPIO.RISING, callback=press_cb, bouncetime=1000)


def press_cb(ev=None):
    body1 = ""
    filename = 'CLICKED_IMAGE'
    f = open(filename, "rb")
    body1 = f.read()
    f.close()
    # flag = 1
    # cnt = cnt + 1
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body1, headers_octet)
    response1 = conn.getresponse()
    data1 = response1.read()
    print(data1)
    parsed1 = json.loads(data1)
    id1 = parsed1[0]['faceId']
    print(id1)
    print("why did you reach here?")
    conn.request("POST", "/face/v1.0/detect?%s" % params, body2, headers_octet)
    response2 = conn.getresponse()
    data2 = response2.read()
    print(data2)
    parsed2 = json.loads(data2)
    id2 = parsed2[0]['faceId']
    print(id2)

    params3 = urllib.urlencode({
    })
    body = "{'faceId1':'" + id1 + "','faceId2':'" + id2 + "'}"
    conn.request("POST", "/face/v1.0/verify?%s" % params3, body, headers_json)
    response = conn.getresponse()
    data = response.read()
    print(data)
    parsed = json.loads(data)
    if parsed['isIdentical']: # i.e. it returns true
        print("Images are of same person.")
        # GPIO.output(LedGPIO, GPIO.HIGH)
        match = 1
    else:
        print("Images are of different person")
        print("Different person")
        # GPIO.output(LedGPIO, GPIO.LOW)
        match = 0

    if match == 1:
        GPIO.output(LedGPIO, GPIO.HIGH)
    if match == 0:
        GPIO.output(LedGPIO, GPIO.LOW)


def loop():
    while True:
        time.sleep(1)

        # if(flag == 1):
        # flag = 0


# Get this back!
# except Exception as e:
#    print("[Errno {0}] {1}".format(e.errno, e.strerror))


def destroy():  # Looks like Destroy Doesn't work yet
    GPIO.output(LedPin, GPIO.HIGH)  # led off
    GPIO.cleanup()  # Release resource


if __name__ == "__main__":
    setup()
    print('IOT-lab')
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
