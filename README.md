Portable IoT Device for Quality Assessment of Green Coffee Beans
Overview
This repository contains the full project files for the design and implementation of a portable IoT device aimed at assessing the quality of green coffee beans using deep learning techniques. This project was developed to assist the Uganda Coffee Development Authority (UCDA) in ensuring the highest quality standards for coffee exports from Uganda.
Project Structure
```plaintext
.
├── code/
│   ├── web_app/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── static/
│   │       ├── css/
│   │       └── images/
├── docs/
│   ├── report.pdf
│   └── presentation.pptx
├── data/
│   ├── datasets/
│   └── models/
├── README.md
└── LICENSE
```
Features
Hardware Integration: Utilizes a Raspberry Pi 4, Picamera module, and DHT 11 sensor for real-time data collection.
Deep Learning Model: Implements YOLO v8 for high-accuracy defect detection in coffee beans.
User Interface: Streamlit-based web app interface for easy interaction, image upload, and report generation.
Automated Reporting: Generates and emails PDF reports with detailed quality assessment metrics.
Installation
To run this project locally, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/coffee-bean-quality-assessment.git
    cd coffee-bean-quality-assessment
    ```
2. Set up the Raspberry Pi 4 with the necessary libraries:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install python3-pip
    pip3 install -r code/web_app/requirements.txt
    ```
3. Configure the Raspberry Pi to enable camera and sensor functionalities.
Usage
1. Launch the Web App:
    ```bash
    cd code/web_app
    streamlit run app.py
    ```
2. Interact with the Interface:
   - Upload or capture an image of the coffee beans.
   - View real-time temperature and humidity readings.
   - Generate and email PDF reports with the assessment results.
Methodology
The project follows a structured methodology:
1. Field Consultation: Collaboration with UCDA experts to understand the coffee bean quality assessment process.
2. Software Design: Development of the web app interface using Streamlit.
3. Model Development: Training and evaluating SSD-MobileNet, YOLO v7, and YOLO v8 models, with YOLO v8 showing the best performance.
4. Hardware Implementation: Integrating sensors and camera with the Raspberry Pi 4.
5. Prototype Assembly and Testing: Physical assembly, wiring, and field testing at UCDA labs.
Results and Discussion
Model Performance: YOLO v8 achieved the highest accuracy in defect detection.
Quality Assessment: Effective real-time evaluation based on UCDA metrics.
Field Testing: Positive feedback with iterative improvements based on UCDA's inputs.

Challenges and Future Work
Challenges:
- Limited availability of local datasets and computational resources.
- Library conflicts and hardware limitations of the Raspberry Pi 4.
Future Work:
- Connect the device to a cloud platform for secure data storage.
- Use a more powerful microcontroller for enhanced performance.
- Adapt the device for other agricultural products like maize and beans.
Contributors
Your Name - Project Lead – KIWEEWA DENIS INNOCENT
Team Member 1 – DESTINY MULUNGI SANYU



