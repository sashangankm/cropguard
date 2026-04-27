from tensorflow.keras.models import model_from_json
import numpy as np
import requests



class DetectionModel(object):

    class_nums = ['Healthy','Neutral','Powdery','Rust']

    def __init__(self, model_json_file, model_weights_file):
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        self.loaded_model.load_weights(model_weights_file)
        self.loaded_model.make_predict_function()

    def predict(self, img):
        self.preds = self.loaded_model.predict(img)
        return DetectionModel.class_nums[np.argmax(self.preds)], self.preds


import tensorflow as tf 
from tensorflow.keras.models import load_model
import numpy as np
from keras.preprocessing import image
import cv2
import numpy as np
import os

model = DetectionModel("model/model.json", 'model/model_weights.keras')
font = cv2.FONT_HERSHEY_SIMPLEX


def startapplication():
    video = cv2.VideoCapture(0) 
    while True:
        ret, frame = video.read()
        if not ret or frame is None:
            print("Error: Unable to read frame from the camera.")
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (224, 224))

        pred, prob = model.predict(roi[np.newaxis, :, :])
        print(prob)
        print(pred)
        prob = (round(prob[0][0]*100, 2))
##        if pred == 'Rust' or pred == 'Powdery':
##                        url = "http://iotbegineer.com/api/sensors"
##                        myobj={'sensor2':'Plant Disease Detection'}
##                        r = requests.post(url,json=myobj,headers={'username': 'iotbegin090','Content-Type':'application/json'})
##                        print('data updated')
##                 
            

        cv2.rectangle(frame, (0, 0), (280, 40), (0,0, 0), -1)
        cv2.putText(frame, pred+" "+str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
        cv2.imshow('Video', frame)  


if __name__ == '__main__':
    startapplication()

