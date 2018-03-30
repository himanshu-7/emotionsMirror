# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
from imutils.video import VideoStream
import time



def videoLoop():
	global panelA, frame
	# DISCLAIMER:
	# I'm not a GUI developer, nor do I even pretend to be. This
	# try/except statement is a pretty ugly hack to get around
	# a RunTime error that Tkinter throws due to threading
	try:
		# keep looping over frames until we are instructed to stop
		while not stopEvent.is_set():
			# grab the frame from the video stream and resize it to
			# have a maximum width of 300 pixels
			frame = vs.read()
			#frame = imutils.resize(frame, width=300)
	
			# OpenCV represents images in BGR order; however PIL
			# represents images in RGB order, so we need to swap
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
		print("[INFO] caught a RuntimeError")

def takeSnapshot():
	global filename
	# grab the current timestamp and use it to construct the
	# output path
	#ts = datetime.datetime.now()
	filename = "capture.jpg"
	p = os.path.sep.join((outputPath, filename))

	# save the file
	cv2.imwrite(p, frame.copy())
	print("[INFO] {} saved".format(filename))
	display_image()

def display_image():
	global panelB

	
	image = cv2.imread(filename)
	image = cv2.flip(image,1)
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



def Quit():
	# set the stop event, cleanup the camera, and allow the rest of
	# the quit process to continue
	print("[INFO] closing...")
	vs.stop()
	root.destroy()
	root.quit()

print("[INFO] warming up camera...")
vs = VideoStream(src = 0).start()
time.sleep(2.0)
outputPath = "/media/chinmay/Important/ABHYAS/playground/tkinter-photo-booth/"
frame = None
thread = None
stopEvent = None

# initialize the root window and image panel
root = tki.Tk()
panelA = None
panelB = None
# create a button, that when pressed, will take the current
# frame and save it to file
f = tki.Frame(root)
f.pack()
btn1 = tki.Button(f, text="Snapshot!",
	command=takeSnapshot)
btn1.pack(side="right", padx=10,
	pady=10)
btn2 = tki.Button(f, text="Quit",
	command=Quit)
btn2.pack(side="left", padx=10,
	pady=10)

# start a thread that constantly pools the video sensor for
# the most recently read frame
stopEvent = threading.Event()
thread = threading.Thread(target=videoLoop, args=())
thread.start()

root.mainloop()