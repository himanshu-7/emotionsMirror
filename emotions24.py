## This code is made from snippets all around the internet, need to include a header or disclaimer later.
## Detect emotions using RPi and Google's vision api

# for parsing google's string reply
import argparse
import base64
import os
import json
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import cv2								# obviously...
import RPi.GPIO as GPIO					# funny button to click a photo
import datetime 						# might be useful later
import time
from lazyme.string import color_print   # debugging colorful prints is easier

# for gui
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import imutils
from imutils.video import VideoStream

# Google's Vision API credentails should be in the root directory
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'

# semi-fuzzy logic to interpret Google's individual emotions to most likely emotion
emotions = ['UNKNOWN','VERY_UNLIKELY','UNLIKELY','POSSIBLE','LIKELY','VERY_LIKELY']

buttonPin=18    # input GPIO

# thread to display frames in the UI
def videoLoop():
    global panelA, frame
    try:
        while not stopEvent.is_set():
            frame = vs.read()
            #frame = imutils.resize(frame, width=300)

            # the channels, then convert to PIL and ImageTk format
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # if the panel is not None, we need to initialize it
            if panelA is None:
                panelA = tki.Label(image=image)
                panelA.image = image
                panelA.pack(side="left", padx=10, pady=10)

            # otherwise, simply update the panel
            else:
                panelA.configure(image=image)
                panelA.image = image

    except RuntimeError, e:
            print("caught a RuntimeError")

# find a way to prioritize GPIO over the Tkinter button
# def press_cb(eV=None):
                
# takeSnapshot is a callback registered to save images, and send them to Google Vision               
def takeSnapshot(eV=None):
    global filename
    filename = "capture.jpg"
    new_img = frame.copy()
    p = os.path.sep.join((outputPath, filename)) 
    cv2.imwrite(p, new_img)				
    print "in callback"
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
                joy      = json_data['responses'][0]['faceAnnotations'][0]['joyLikelihood']
                sorrow   = json_data['responses'][0]['faceAnnotations'][0]['sorrowLikelihood']
                anger    = json_data['responses'][0]['faceAnnotations'][0]['angerLikelihood']
                surprise = json_data['responses'][0]['faceAnnotations'][0]['surpriseLikelihood']
                
                for i in emotions:
					if(joy == i):
							joy_likelihood      = emotions.index(i)
					if(sorrow == i):
							sorrow_likelihood   = emotions.index(i)
					if(anger == i):
							anger_likelihood    = emotions.index(i)
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
                cv2.rectangle(new_img, (face_coordinate_one_x, face_coordinate_two_y), (face_coordinate_three_x, face_coordinate_four_y), (255,0,0), 2)
                cv2.putText(new_img, likelihood_str[final_emotion], (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.CV_AA)
                # cv2.namedWindow('emo_img')
                cv2.imwrite(p, new_img)
            
            except KeyError:
                color_print("no face in callback", color = 'red')
    display_image()

# display image with emotions overlapped
def display_image():
	global panelB

	image = cv2.imread(filename)
	# image = cv2.flip(image,1)
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	image = Image.fromarray(image)
	image = ImageTk.PhotoImage(image)

	if panelB is None:
		panelB = tki.Label(image = image)
		panelB.image = image
		panelB.pack(side="left", padx =10, pady=10)
	else:
		# panelA = Label(image= image)
		panelB.configure(image=image)
		panelB.image = image
		# panelA.pack(side="left", padx = 10, pady = 10)

# this function forces the resources to be freed: need a keyboard (todo: yet to be handled) 
def forceExit():                
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print "pressed q"
		cv2.destroyAllWindows()
		cap.release()
		GPIO.cleanup()  # Release resource
		quit()
		
        
# onClose callback is the only way to close the application, 
# so make sure you release all the resources here      
def onClose():
	# set the stop event, cleanup the camera, (allow rest to continue)
	print("closing Tk...")
	root.quit()
	vs.stop()
	stopEvent.set()
	GPIO.cleanup()  # Release resource   
 

if __name__ == '__main__':	
    # initialize the pins (don't forget to release the GPIO (cleanup)
    GPIO.setmode(GPIO.BOARD)
    
    # pull up the input and register the callback, don't press quicker than 1000ms
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=takeSnapshot, bouncetime=1000)
    
    try:
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('vision','v1',credentials=credentials)
    except Exception:
        color_print("ServerNotFoundError: Unable to find the server at www.googleapis.com", bold=True, color='white', highlight='pink')

            
    print("warming up camera...")
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)
    outputPath = "/home/pi/Desktop/iot_emotionsMirror/"
    frame = None
    thread = None
    stopEvent = None

    # initialize the root window and image panel
    root = tki.Tk()
    panelA = None
    panelB = None
    
    # create a button, that when pressed, will take the current frame and save it to file
    f = tki.Frame(root)
    f.pack()
    
    btn1 = tki.Button(f, text="Snapshot!", command=takeSnapshot)
    btn1.pack(side="right", padx=10, pady=10)
    # btn2 = tki.Button(f, text="Quit", command = Destroy.root)
    # btn2.pack(side="left", padx=10, pady=10)

    # start a thread for recently read frame
    stopEvent = threading.Event()
    thread = threading.Thread(target=videoLoop, args=())
    thread.start()
    
    # what happens on window close: callback
    root.wm_protocol('WM_DELETE_WINDOW', onClose)

    root.mainloop()
