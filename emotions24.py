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
import RPi.GPIO as GPIO			        # funny button to click a photo
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

buttonPin=18    # input GPIO

# Class to store faces detected , their emotions and co-ordinates of the face
class Faces:
	def __init__(self,joy,sorrow,anger,surprise,x1,x2,y1,y2):
		self.joy = joy
		self.sorrow = sorrow 
		self.anger = anger
		self.surprise = surprise
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2

	
#Funtion to change the string values of emotions to numerals    
	@staticmethod
	def emotionToVal(emotion):
		if(emotion == 'UNKNOWN'):
			return 0
		elif(emotion == 'VERY_UNLIKELY'):
			return 1
		elif(emotion == 'UNLIKELY'):
			return 2
		elif(emotion == 'POSSIBLE'):
			return 3
		elif(emotion == 'LIKELY'):
			return 4
		elif(emotion == 'VERY_LIKELY'):
			return 5
		else: 
			return 0

#Detects the emotion for detected faces
	def emotion(self):
		joyVal = self.emotionToVal(self.joy)
		sorrowVal = self.emotionToVal(self.sorrow)
		angerVal = self.emotionToVal(self.anger)
		surpriseVal = self.emotionToVal(self.surprise)
		if(joyVal == sorrowVal and joyVal == angerVal and joyVal == surpriseVal):                              #if values of all emotions are equal, set emotion to neutral 
			return 'Neutral'
		elif(joyVal > sorrowVal and joyVal > angerVal and joyVal > surpriseVal):                              #if joy is greater than other emotions, set emotion to Happy
			return 'Happy'
		elif(sorrowVal > joyVal and sorrowVal > angerVal and sorrowVal > surpriseVal):                        #if sorrow is greater than other emotions, set emotion to Sad
			return 'Sad'
		elif(angerVal > joyVal and angerVal > sorrowVal and angerVal > surpriseVal):                          #if anger is greater than other emotions, set emotion to Angry
			return 'Angry'
		elif(surpriseVal > joyVal and surpriseVal > angerVal and surpriseVal > sorrowVal):                    #if surprise is greater than other emotions, set emotion to surprise 
			return 'Surprised'

		else:
			return 'Sorry!! Please try again'

#Set co-ordinates for face rectangles
def setCoordinates(x1,x2,x3,x4,y1,y2,y3,y4):
	one_x = x1
	one_y = y1
	if(x1 != x2):
		two_x = x2
	elif(x1 != x3):
		two_x = x3
	else:
		two_x = x4
	if(y1 != y2):
		two_y = y2
	elif(y1 != y3):
		two_y = y3
	else: 
		two_y = y4
	if(one_y > two_y):
		y1 = one_y
		one_y = two_y
		two_y = y1

	return one_x,two_x,one_y,two_y                                                                          #return the vertex co-ordinates of the rectangle                    


# thread to display frames in the UI
def videoLoop():
	global panelA, frame
	try:
		while not stopEvent.is_set():
			frame = vs.read()
			frame = imutils.resize(frame, width=1280, height=720)

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
	faceObj = []
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
				faces = json_data['responses'][0]['faceAnnotations']
				for face in faces: 
					joy      = face['joyLikelihood']
					sorrow   = face['sorrowLikelihood']
					anger    = face['angerLikelihood']
					surprise = face['surpriseLikelihood']
					face_one_x   = face['boundingPoly']['vertices'][0]['x']
					face_two_x   = face['boundingPoly']['vertices'][1]['x']
					face_three_x = face['boundingPoly']['vertices'][2]['x']
					face_four_x  = face['boundingPoly']['vertices'][3]['x']
					face_one_y   = face['boundingPoly']['vertices'][0]['y']
					face_two_y   = face['boundingPoly']['vertices'][1]['y']
					face_three_y = face['boundingPoly']['vertices'][2]['y']
					face_four_y  = face['boundingPoly']['vertices'][3]['y']
					[x1,x2,y1,y2] = setCoordinates(face_one_x,face_two_x,face_three_x,face_four_x,face_one_y,face_two_y,face_three_y,face_four_y)
					face_detected = Faces(joy,sorrow,anger,surprise,x1,x2,y1,y2)
					faceObj.append(face_detected)
			except KeyError:
				color_print("no face in callback", color = 'red')
			for value in range(0,len(faceObj)):
				final_emotion = faceObj[value].emotion()
				cv2.rectangle(new_img, (faceObj[value].x1, faceObj[value].y1), (faceObj[value].x2, faceObj[value].y2), (255,255,255), 2)
				cv2.putText(new_img, final_emotion, ((faceObj[value].x1)+5,(faceObj[value].y1)-10), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 2, cv2.CV_AA)
				# cv2.namedWindow('emo_img')
			cv2.imwrite(p, new_img)
	display_image()

# display image with emotions overlapped
def display_image():
	global panelB

	image = cv2.imread(filename)
	image = imutils.resize(image, height=240, width=480)
	# image = cv2.flip(image,1)
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	image = Image.fromarray(image)
	image = ImageTk.PhotoImage(image)

	if panelB is None:
		panelB = tki.Label(image = image)
		panelB.image = image
		panelB.pack(side="right", padx =10, pady=10)
	else:
		# panelA = Label(image= image)
		panelB.configure(image=image)
		panelB.image = image
		# panelA.pack(side="left", padx = 10, pady = 10)

# this function forces the resources to be freed: need a keyboard (todo: yet to be handled) 
def forceExit():                
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print "pressed q"
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
	vs = VideoStream(src = 0, resolution=(1280,720)).start()
	time.sleep(2.0)
	outputPath = "/home/pi/Desktop/iot_emotionsMirror"
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

	# start a thread for recently read frame
	stopEvent = threading.Event()
	thread = threading.Thread(target=videoLoop, args=())
	thread.start()
	
	# what happens on window close: callback
	root.wm_protocol('WM_DELETE_WINDOW', onClose)
	
	root.mainloop()
	# force quit remains to be implemented
	# while(True):
	#	forceExit()	
