import cv2
import numpy as np
import requests
import threading
import time
import tkinter as tk
from tkinter import Label, Text, Scrollbar, END, Frame
from tensorflow.keras.models import model_from_json
from PIL import Image, ImageTk

BG_COLOR = "#1e272e"       
CARD_COLOR = "#2f3640"     
ACCENT_COLOR = "#2ecc71"   
TEXT_COLOR = "#ffffff"     

root = tk.Tk()
root.title("Leaf Health Monitor Pro")
root.geometry("700x850")
root.config(bg=BG_COLOR)

last_frame = None
frame_lock = threading.Lock()

last_prediction = {
    "disease": "Scanning...",
    "confidence": 0.0,
    "recommendation": ""
}
prediction_lock = threading.Lock()
detection_start_time = None

class DetectionModel(object):
    class_nums = ['Healthy', 'Neutral', 'Powdery', 'Rust']

    def __init__(self, model_json_file, model_weights_file):
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights(model_weights_file)

    def predict(self, img):
        self.preds = self.loaded_model.predict(img)
        return DetectionModel.class_nums[np.argmax(self.preds)], self.preds

try:
    leaf_model = DetectionModel("model/model.json", "model/model_weights.keras")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

def get_recommendation(disease):
    recommendations = {
        "Healthy": "Your plant is in great condition! No need for treatment.\n\nTip: Continue regular care. Ensure proper sunlight.",
        "Neutral": "The plant looks fine, but it needs monitoring.\n\nTip: Check for signs of spots in the next few days.",
        "Powdery": "Powdery mildew detected. Apply sulfur fungicide spray.\n\nTip: Increase airflow and reduce humidity.",
        "Rust": "Rust detected. Use a copper-based fungicide.\n\nTip: Prune affected leaves immediately."
    }
    return recommendations.get(disease, "No recommendation available.")

def fetch_frames():
    global last_frame, detection_start_time
    ESP32_STREAM = "http://10.52.171.238:81/stream"

    while True:
        try:
            stream = requests.get(ESP32_STREAM, stream=True, timeout=5)
            bytes_data = bytes()
            for chunk in stream.iter_content(chunk_size=4096):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b+2]
                    bytes_data = bytes_data[b+2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if frame is None: continue

                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    roi = cv2.resize(rgb_frame, (224, 224))
                    pred, prob = leaf_model.predict(roi[np.newaxis, :, :])
                    confidence = round(np.max(prob) * 100, 2)
                    if pred == 'Rust' or pred == 'Powdery':
                        url = "http://iotbegineer.com/api/sensors"
                        myobj={'sensor2':'Plant Disease Detection'}
                        r = requests.post(url,json=myobj,headers={'username': 'iotbegin090','Content-Type':'application/json'})
                        print('data updated')
              

                    if confidence >= 50:
                        if detection_start_time is None:
                            detection_start_time = time.time()
                        recommendation = get_recommendation(pred) if (time.time() - detection_start_time > 3) else "Analyzing..."
                    else:
                        pred, confidence, recommendation, detection_start_time = "Scanning...", 0.0, "", None

                    with prediction_lock:
                        last_prediction.update({"disease": pred, "confidence": confidence, "recommendation": recommendation})
                    with frame_lock:
                        last_frame = frame
        except Exception:
            time.sleep(2)

threading.Thread(target=fetch_frames, daemon=True).start()


main_container = Frame(root, bg=BG_COLOR)
main_container.place(relx=0.5, rely=0.5, anchor="center") 

title_lbl = Label(main_container, text="LEAF HEALTH MONITOR", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
title_lbl.pack(pady=(0, 20))

video_card = Frame(main_container, bg="black", bd=2, relief="flat")
video_card.pack()
video_label = Label(video_card, bg="black")
video_label.pack()

info_frame = Frame(main_container, bg=BG_COLOR)
info_frame.pack(pady=20, fill="x")

disease_label = Label(info_frame, text="Disease: Scanning...", font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
disease_label.pack()

confidence_label = Label(info_frame, text="Confidence: 0%", font=("Segoe UI", 12), bg=BG_COLOR, fg="#bdc3c7")
confidence_label.pack()

rec_title = Label(main_container, text="Expert Recommendation", font=("Segoe UI", 12, "italic"), bg=BG_COLOR, fg=ACCENT_COLOR)
rec_title.pack(pady=(10, 5))

recommendation_text = Text(main_container, wrap="word", font=("Segoe UI", 11), height=6, width=50, 
                         bg=CARD_COLOR, fg="#ecf0f1", bd=0, padx=15, pady=15)
recommendation_text.pack(pady=5)

def update_gui():
    if last_frame is not None:
        cv2image = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)
        cv2image = cv2.resize(cv2image, (480, 320))
        img = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
        video_label.config(image=img)
        video_label.image = img

    with prediction_lock:
        d, c, r = last_prediction["disease"], last_prediction["confidence"], last_prediction["recommendation"]
    
    disease_label.config(text=f"{d.upper()}")
    confidence_label.config(text=f"Match Accuracy: {c}%")
    
    disease_label.config(fg=ACCENT_COLOR if d == "Healthy" else "#e74c3c")

    recommendation_text.delete(1.0, END)
    recommendation_text.insert(END, r)
    root.after(100, update_gui)

update_gui()
root.mainloop()
