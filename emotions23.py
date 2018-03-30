## This code is made from snippets all around the internet, need to include a header or disclaimer later.
## Detect emotions using RPi and Google's vision api

import argparse
import base64
import os

#for parsing google's string reply
import json
import cv2

import RPi.GPIO as GPIO

# might be useful later
import time

# debugging colorful prints is easier
from lazyme.string import color_print

# google's vision api was easy to install
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'

emotions = ['UNKNOWN','VERY_UNLIKELY','UNLIKELY','POSSIBLE','LIKELY','VERY_LIKELY']
frame = 0
buttonPin=18

def press_cb(eV=None):
    print "in callback"
    cv2.imwrite("capture.jpg", frame)
    with open('capture.jpg','rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(body={
                    'requests': [{
                            'image': {
                                    'content': image_content.decode('UTF-8')
                            },
                            'features': [{
                                    'type': 'FACE_DETECTION',
                                    'maxResults': 10
                            }]
                    }]
            })
            try:
                response = service_request.execute()
                data = json.dumps(response)
                json_data = json.loads(data)
            except Exception:
                color_print("abrupt disconnection, check internet connectivity", color='red')
            # print json_data
            try:
                joy = json_data['responses'][0]['faceAnnotations'][0]['joyLikelihood']
                sorrow = json_data['responses'][0]['faceAnnotations'][0]['sorrowLikelihood']
                anger = json_data['responses'][0]['faceAnnotations'][0]['angerLikelihood']
                surprise = json_data['responses'][0]['faceAnnotations'][0]['surpriseLikelihood']
                
                for i in emotions:
                        if(joy == i):
                                joy_likelihood = emotions.index(i)
                        if(sorrow == i):
                                sorrow_likelihood = emotions.index(i)
                        if(anger == i):
                                anger_likelihood = emotions.index(i)
                        if(surprise == i):
                                surprise_likelihood = emotions.index(i)

                likelihood = [joy_likelihood, sorrow_likelihood, anger_likelihood, surprise_likelihood]
                likelihood_str = ['Happy','Sad','Angry','Surprised']
                final_emotion = likelihood.index(max(likelihood))
                # keep prints off, try to squeeze out all the fps
                # print likelihood
                # print final_emotion                               
                face_coordinate_one_x   = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][0]['x'])
                face_coordinate_two_x   = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][1]['x'])
                face_coordinate_three_x = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][2]['x'])
                face_coordinate_four_x  = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][3]['x'])

                face_coordinate_one_y   = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][0]['y'])              
                face_coordinate_two_y   = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][1]['y'])
                face_coordinate_three_y = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][2]['y'])
                face_coordinate_four_y  = int(json_data['responses'][0]['faceAnnotations'][0]['boundingPoly']['vertices'][3]['y'])
                print "Joy: ", joy, "Sorrow: ", sorrow, "anger: ", anger, "Surprise: ", surprise 
                cv2.rectangle(frame, (face_coordinate_one_x, face_coordinate_two_y), (face_coordinate_three_x, face_coordinate_four_y), (255,0,0), 2)
                cv2.putText(frame, likelihood_str[final_emotion], (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.CV_AA)
                cv2.namedWindow('emo_img')
                cv2.imshow('emo_img', frame)
            
            except KeyError:
                color_print("no face in callback", color = 'red')

# this function forces the resources to be freed: need a keyboard
def forceExit():                
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print "pressed q"
        cv2.destroyAllWindows()
        cap.release()
        GPIO.cleanup()  # Release resource
        quit()

if __name__ == '__main__':
    # initialize the pins (don't forget to release the GPIO (cleanup)
    GPIO.setmode(GPIO.BOARD)
    # pull up the input and register the callback, don't press quicker than 1000ms
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=press_cb, bouncetime=1000)
    
    # initialize the camera, don't forget to release the camera resource
    cap = cv2.VideoCapture(0)
    try:
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('vision','v1',credentials=credentials)
    except Exception:
        color_print("ServerNotFoundError: Unable to find the server at www.googleapis.com", bold=True, color='white', highlight='pink')

    while(True):
        # Capture frame-by-frame
        try:
            # changing the resolution to lower or higher resolutions changes the FPS. Use threads?
            # cap.set(3, 1000)
            # cap.set(4, 1000)
            ret, frame = cap.read()
            cv2.namedWindow('frame')
            cv2.imshow('frame', frame)
        except Exception:
            color_print('cant connect to usb-camera, reconnect and run script again', bold=True, color='white', highlight='red')
            cv2.destroyAllWindows()
            cap.release()
            quit()

        try:
            forceExit()
        
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            cap.release()
            cv2.destroyAllWindows()
            GPIO.cleanup()  # Release resource
