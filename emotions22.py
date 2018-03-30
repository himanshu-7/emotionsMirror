import argparse
import base64
import os
import json
import cv2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'

emotions = ['UNKNOWN','VERY_UNLIKELY','UNLIKELY','POSSIBLE','LIKELY','VERY_LIKELY']

				
def main():

	cap = cv2.VideoCapture(0)
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('vision','v1',credentials=credentials)
	# cv2.startWindowThread()
	
	while(True):
	# Capture frame-by-frame
		ret, frame = cap.read()
		cv2.namedWindow('frame')
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('d'):
			# cv2.imwrite("capture.jpg", frame)
			################################################################ todo: Make a different fn with exception handling
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
				response = service_request.execute()
				data = json.dumps(response)
				json_data = json.loads(data)
				# print json_data
                        ############################################################# new function to map the faces
				
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
				cv2.imshow('emo_img', frame);
			
                if cv2.waitKey(1) & 0xFF == ord('q'): # dont touch this!!!
                        break
                
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
