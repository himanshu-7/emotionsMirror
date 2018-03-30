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
	global panel, frame
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
			frame = imutils.resize(frame, width=300)
	
			# OpenCV represents images in BGR order; however PIL
			# represents images in RGB order, so we need to swap
			# the channels, then convert to PIL and ImageTk format
			image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			image = Image.fromarray(image)
			image = ImageTk.PhotoImage(image)
	
			# if the panel is not None, we need to initialize it
			if panel is None:
				panel = tki.Label(image=image)
				panel.image = image
				panel.pack(side="left", padx=10, pady=10)
	
			# otherwise, simply update the panel
			else:
				panel.configure(image=image)
				panel.image = image

	except RuntimeError, e:
		print("[INFO] caught a RuntimeError")

def takeSnapshot():
	
	# grab the current timestamp and use it to construct the
	# output path
	ts = datetime.datetime.now()
	filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
	p = os.path.sep.join((outputPath, filename))

	# save the file
	cv2.imwrite(p, frame.copy())
	print("[INFO] saved {}".format(filename))

def onClose():
	# set the stop event, cleanup the camera, and allow the rest of
	# the quit process to continue
	print("[INFO] closing...")
	stopEvent.set()
	vs.stop()
	root.quit()


print("[INFO] warming up camera...")
vs = VideoStream(src = 0).start()
time.sleep(2.0)
vs = vs
outputPath = "/media/chinmay/Important/ABHYAS/playground/tkinter-photo-booth/"
frame = None
thread = None
stopEvent = None

# initialize the root window and image panel
root = tki.Tk()
panel = None

# create a button, that when pressed, will take the current
# frame and save it to file
f = tki.Frame(root)
f.pack()
btn1 = tki.Button(f, text="Snapshot!",
	command=takeSnapshot)
btn1.pack(side="right", padx=10,
	pady=10)
btn2 = tki.Button(f, text="Quit",
	command=onClose)
btn2.pack(side="left",padx=10,
	pady=10)		

# start a thread that constantly pools the video sensor for
# the most recently read frame
stopEvent = threading.Event()
thread = threading.Thread(target=videoLoop, args=())
thread.start()

root.mainloop()