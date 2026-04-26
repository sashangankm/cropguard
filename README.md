# CropGuard 🌱
[cite_start]A real-time, fully autonomous plant disease monitoring system combining edge hardware and computer vision[cite: 62].

## 📌 Overview
[cite_start]CropGuard is a cost-effective system designed to deliver high-accuracy, autonomous plant disease detection directly to farmers[cite: 18]. [cite_start]The system integrates a single, low-power ESP32-CAM unit, deployed in the field and sustainably powered by a solar panel, to capture high-resolution images of plant leaves[cite: 19]. [cite_start]It wirelessly transmits these images in real time to a cloud-based server where an optimized YOLOv8 object detection model identifies and localizes diseases with high accuracy[cite: 20, 21]. [cite_start]The centralized dashboard, powered by the iotbegineer platform, alerts farmers immediately and provides actionable remedies to treat the diseases[cite: 22].

## ✨ Features
* [cite_start]**Fully Autonomous & Solar Powered:** Continuously powered by a dedicated solar panel setup and battery management system[cite: 75, 86].
* [cite_start]**Cloud-Offloaded Edge ML:** Uses YOLOv8 on a cloud server for rapid, high-precision disease identification and localization, avoiding slow on-device inference[cite: 76, 77].
* [cite_start]**Actionable Remedies:** Cross-references detected diseases with a database to provide specific chemical or biological treatment plans[cite: 94].
* [cite_start]**Real-Time Web Platform:** Live feeds, historical reports, and alerts accessible via a user-friendly interface[cite: 95].

## 🛠️ Hardware Setup
[cite_start]The physical hardware acts as the central processing unit at the edge[cite: 84]. The custom setup includes:
* [cite_start]ESP32-CAM Module (Microcontroller & OV2640 2MP Camera) [cite: 81, 84]
* [cite_start]Solar Panel [cite: 86]
* [cite_start]Rechargeable Battery Pack [cite: 86]
* [cite_start]Power Management Module (TP4056 charging circuit / Buck converters) [cite: 86]
* FTDI Programmer (for initial flashing)
* Custom baseplate, toggle switches, and jumper wires

## 💻 Software & AI Stack
* [cite_start]**Computer Vision Model:** YOLOv8 (You Only Look Once, Version 8) [cite: 97]
* [cite_start]**Architecture:** Convolutional Neural Networks (CNN) with Softmax Regression [cite: 98, 99]
* **Dataset:** Cloud-hosted custom plant disease image dataset
* **IoT Integration:** iotbegineer platform for data logging, stream buffering, and remote monitoring

## 📊 Performance Metrics
[cite_start]The system achieves excellent performance by offloading heavy processing to the cloud, significantly outperforming local edge-inference models[cite: 122]:
* [cite_start]**Disease Detection Accuracy:** > 95.0% [cite: 79]
* **System Uptime:** ~98% 
* **Cloud Data Streaming Latency:** ~2.4 seconds 
* **AI Inference Processing Speed:** ~180 milliseconds 

## 🚀 Future Scope
[cite_start]Continuous development aims to make the system more energy-efficient and user-friendly[cite: 128]:
* [cite_start]**Environmental Sensors:** Integrating temperature, humidity, and soil moisture sensors to improve disease prediction accuracy[cite: 125].
* [cite_start]**Advanced Lightweight Models:** Deploying architectures like MobileNetV3 or EfficientNet to maintain precision while optimizing performance[cite: 126].
* [cite_start]**Large-Scale Farm Management:** Enhancing cloud and mobile application integration for broader remote monitoring[cite: 127].
* [cite_start]**Automated Alerts:** Adding SMS or push notification alerts for immediate intervention[cite: 128].

## 👥 Team & Credits
[cite_start]Developed by:
* [cite_start]Naveen Khumar S [cite: 5]
* [cite_start]Sashangan K M [cite: 6]
* [cite_start]Venkatesan R [cite: 7]

