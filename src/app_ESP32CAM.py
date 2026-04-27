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


stream_url = "http://10.16.131.238:81/stream"

try:
    stream = requests.get(stream_url, stream=True)
    buffer = bytes()

    for chunk in stream.iter_content(chunk_size=8192):
        if not chunk:
            print("Received empty chunk.")
            continue

        buffer += chunk
        start = buffer.find(b'\xff\xd8')
        end = buffer.find(b'\xff\xd9')

        if start != -1 and end != -1:
            jpg_data = buffer[start:end + 2]
            buffer = buffer[end + 2:]

            if len(jpg_data) > 0:
                nparr = np.frombuffer(jpg_data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if frame is not None:
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    roi = cv2.resize(gray_frame, (224, 224))

                    pred, prob = model.predict(roi[np.newaxis, :, :])
                    print(prob)
                    print(pred)
                    prob = (round(prob[0][0]*100, 2))
                    if pred == 'Rust' or pred == 'Powdery':
                        url = "http://iotbegineer.com/api/sensors"
                        myobj={'sensor2':'Plant Disease Detection'}
                        r = requests.post(url,json=myobj,headers={'username': 'iotbegin090','Content-Type':'application/json'})
                        print('data updated')
                 
                        

                    cv2.rectangle(frame, (0, 0), (280, 40), (0,0, 0), -1)
                    cv2.putText(frame, pred+" "+str(prob), (20, 30), font, 1, (255, 255, 0), 2)


                   

                    cv2.imshow("Live Classification", frame)

                else:
                    print("Failed to decode frame.")
            else:
                print("Received empty JPEG data.")
        else:
            print("Waiting for complete JPEG data...")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except requests.exceptions.RequestException as e:
    print(f"Error connecting to the stream: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    cv2.destroyAllWindows()
