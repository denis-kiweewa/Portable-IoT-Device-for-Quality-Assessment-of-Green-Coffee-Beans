# Python In-built packages
from pathlib import Path
import PIL
import os

from collections import Counter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


import mailsender
from mailsender import send_email
import board
import adafruit_dht
# External packages
import streamlit as st
import cv2
import time

# Local Modules
import settings
import helper

import psutil

# Additional imports for PiCamera
from picamera2 import Picamera2, Preview
import uuid

# imports for email sending

from mailsender import send_email


# Setting page layout
st.set_page_config(
    page_title="Object Detection using YOLOv8",
    page_icon="♨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Object Detection And Quality Assessment of green coffee beans using YOLOv8")

# Initialize PiCamera
# picam2 = Picamera2()
# camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
# picam2.configure(camera_config)
# picam2.start_preview(Preview.QTGL)
# picam2.start()
# time.sleep(2)



# Ensure TEMP_DIR exists
TEMP_DIR = settings.ROOT / 'temp'
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to save image with bounding boxes temporarily
def save_temp_image(image):
    temp_image_path = TEMP_DIR / "temp_image.jpg"
    image.save(temp_image_path)
    return temp_image_path

# Function to classify coffee quality
def classify_coffee_quality(class_names):
    total_count = len(class_names)
    broken_count = class_names.count("broken")
    black_count = class_names.count("black")
    cherry_count = class_names.count("cherry")
    defect_percentage = (broken_count + black_count + cherry_count) / total_count * 100
    
    if defect_percentage <= 7:
        return "Good Quality"
    elif 7 < defect_percentage <= 10:
        return "Moderate Quality"
    else:
        return "Poor Quality"


def detect_objects(image, confidence):
    res = model.predict(image, conf=confidence)
    boxes = res[0].boxes
    detected_classes = []
    for box in boxes:
        class_index = int(box.data[0][-1])
        class_name = res[0].names[class_index]
        detected_classes.append(class_name)
    return res, detected_classes

def assess_quality(detected_classes):
    class_counts = Counter(detected_classes)
    total_count = sum(class_counts.values())
    if total_count >= 10:
        quality_comment = "Bad quality"
        quality_reason = "High proportion of black, broken, or cherry beans. Unsuitable for premium coffee."
    elif total_count >= 7:
        quality_comment = "Medium quality"
        quality_reason = "Moderate proportion of black, broken, or cherry beans. Acceptable for regular coffee."
    else:
        quality_comment = "Good quality"
        quality_reason = "Low proportion of black, broken, or cherry beans. Ideal for high-quality coffee."
    return quality_comment, quality_reason, total_count


def generate_pdf_report(quality_comment, quality_reason, detected_classes, total_count,dht_temperature, dht_humidity,humidity_recommendation,temperature_recommendation, image_path=None):
    styles = getSampleStyleSheet()
    pdf_filename = TEMP_DIR / "coffee_quality_report.pdf"
    pdf_filename_str = str(pdf_filename) # Convert Path object to string
    doc = SimpleDocTemplate(pdf_filename_str, pagesize=letter)
    elements = []

    # Add Title
    elements.append(Paragraph("Coffee Beans Quality Report", styles['Title']))

    # Add Quality Assessment
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Quality Assessment: {quality_comment}", styles['Heading2']))
    elements.append(Paragraph(f"Reason: {quality_reason}", styles['Normal']))

# Add Humidity and Temperature values
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Humidity : {dht_humidity}", styles['Heading2']))
    elements.append(Paragraph(f"Humidity recommendation: {humidity_recommendation}", styles['Normal']))
    elements.append(Paragraph(f"Temperature : {dht_temperature}", styles['Heading2']))
    elements.append(Paragraph(f"Temperature recommendation: {temperature_recommendation}", styles['Normal']))
    
    # Add Detected Classes
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Detected Classes:", styles['Heading2']))
    for cls in detected_classes:
        elements.append(Paragraph(f"- {cls}", styles['Normal']))

    # Add Total Count
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total Count: {total_count}", styles['Normal']))

    # Add Image with Bounding Boxes
    if image_path:
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Image with Bounding Boxes:", styles['Heading2']))
        elements.append(Image(image_path, width=400, height=300))

    doc.build(elements)
    return pdf_filename_str  # Return the string path

def send_report(receiver_email, quality_comment, quality_reason, pdf_filename, image_filename):
#    try:
    send_email(receiver_email, quality_comment, quality_reason, pdf_filename, image_filename)
    st.success("Report sent successfully!")
#    except Exception as e#:
#        st.error(f"Error sending report: {e}")


# Function to provide temperature recommendations
def temperature_recommendation(temperature):
    if 13 <= temperature <= 21:
        return "Ambient temperature within recommended values"
    elif temperature < 13:
        return "Dry beans again"
    else:
        return "Beans too dry"

# Function to provide humidity recommendations
def humidity_recommendation(humidity):
    if 50 <= humidity <= 55:
        return "Humidity within recommended values"
    elif humidity < 50:
        return "Beans may dry out excessively"
    else:
        return "Beans susceptible to mold growth and spoilage"   
def read_dht_sensor():
    """
    Reads temperature and humidity from DHT11 sensor.

    Returns:
        tuple: Temperature and humidity values.
    """
   #  try:
        
        # sensor = adafruit_dht.DHT11(board.D27)
        # time.sleep(3.0)
        
        # temperature = sensor.temperature
        # humidity = sensor.humidity
        
        # return temperature, humidity
    # except Exception as e:
       #  st.sidebar.error("Error reading DHT11 sensor: " + str(e))
        # return None, None

def capture_image():
    """
    Captures an image using the PiCamera.

    Returns:
        str: File path of the captured image.
    """
    try:
 #       from picamera2 import Picamera2, Preview
        import time
        img_filename = f"captured_image_{uuid.uuid4().hex}.jpg"
        img_path = os.path.join("temp_images", img_filename)
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
        picam2.configure(camera_config)
        # picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(3)
        picam2.capture_file(img_path)
        picam2.close()
        return img_path
    except Exception as e:
        st.sidebar.error("Error capturing image using PiCamera: " + str(e))
        return None


# Sidebar
st.sidebar.header("Model Hyperparameters")

# Model Options
model_type = 'Detection'  # Always set to 'Detection'

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 0, 100, 50)) / 100

# Temperature and Humidity input from DHT11 sensor

try:
    dht_temperature, dht_humidity =read_dht_sensor()

except:
    dht_temperature, dht_humidity = 28, 70


if dht_temperature is not None and dht_humidity is not None:
    st.sidebar.write(f"Temperature: {dht_temperature}°C")
    st.sidebar.write(f"Humidity: {dht_humidity}%")
else:
    st.sidebar.error("Failed to read sensor data")



    


# Selecting Detection Or Segmentation (always set to 'Detection')
model_path = Path(settings.DETECTION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Input Data Source")
source_radio = st.sidebar.radio(
    "Select Source", ['PiCamera', 'Upload'])
 
source_img = None

# Default images
default_image_path = str(settings.DEFAULT_IMAGE)
default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)

col1, col2 = st.columns(2)

if 'detected_image' not in st.session_state:
    st.session_state['detected_image'] = None
    st.session_state['detected_classes'] = []
    st.session_state['quality_comment'] = ""
    st.session_state['quality_reason'] = ""
    st.session_state['total_count'] = 0

with col1:
    default_image = PIL.Image.open(default_image_path)
    st.image(default_image_path, caption="Default Image", use_column_width=True)

with col2:
    default_detected_image = PIL.Image.open(default_detected_image_path)
    st.image(default_detected_image_path, caption='Default detected Image', use_column_width=True)

# If image is selected
if source_radio == 'Upload':
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    with col1:
        if source_img is not None:
            uploaded_image = PIL.Image.open(source_img)
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            # Display temperature recommendation
            st.write("Temperature Recommendation:", temperature_recommendation(dht_temperature))

            # Display humidity recommendation
            st.write("Humidity Recommendation:", humidity_recommendation(dht_humidity))

    with col2:

        if source_img is not None:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                    # Calculate class_names for coffee quality classification
                class_names = [res[0].names[int(box.data[0][-1])] for box in boxes]
                    
                    # Classify coffee quality
                quality = classify_coffee_quality(class_names)
                    
                    # Display coffee quality result
                st.write("Coffee Quality:", quality)
                print("here now")


                res, detected_classes = detect_objects(uploaded_image, confidence)
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image', use_column_width=True)
                st.session_state['detected_image'] = res_plotted
                st.session_state['detected_classes'] = detected_classes
                quality_comment, quality_reason, total_count = assess_quality(detected_classes)
                st.session_state['quality_comment'] = quality_comment
                st.session_state['quality_reason'] = quality_reason
                st.session_state['total_count'] = total_count
                st.session_state['dht_temperature'] = dht_temperature
                st.session_state['dht_humidity'] = dht_humidity
                st.session_state['temperature_recommendation'] = "temperature_recommendation"
                st.session_state['humidity_recommendation'] = humidity_recommendation
                    
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            for r in res:
                                    class_index = int(box.data[0][-1])
                                    class_name = r.names[class_index]
                                    score = float(box.data[0][-2])
                                    st.write(f"Class: {class_name.upper()} Confidence: {score*100:.1f}%")
                except Exception as ex:
                        st.write("No image is uploaded yet!")
                    
                    # Count of coffee beans for each class
                st.write("Count of coffee beans:")
                bean_counts = {}
                for class_name in set(class_names):
                        count = class_names.count(class_name)
                        bean_counts[class_name] = count
                for class_name, count in bean_counts.items():
                        st.write(f"- {class_name}: {count}")
                    
                    # Unique identifier for each detected image
                if not os.path.exists("results"):
                        os.makedirs("results")
                unique_id = f"Sample{len(os.listdir('results')) + 1}"
                    
                    # Save detected image
                detected_image_path = os.path.join("results", f"{unique_id}.png")
                try:
                        PIL.Image.fromarray(res_plotted).save(detected_image_path)
                except Exception as e:
                        st.error(f"Error saving image: {e}")
                    
                    # Save results to text file
                with open(os.path.join("results", f"{unique_id}.txt"), "w") as f:
                        f.write(f"Detected Image: {unique_id}\n")
                        f.write(f"Coffee Quality: {quality}\n")
                        f.write(f"Temperature Recommendation: {temperature_recommendation(dht_temperature)}\n")
                        f.write(f"Humidity Recommendation: {humidity_recommendation(dht_humidity)}\n")
                        f.write("Count of coffee beans:\n")
                        for class_name, count in bean_counts.items():
                            f.write(f"- {class_name}: {count}\n")
            
# If PiCamera is selected
if source_radio == 'PiCamera':
    if st.sidebar.button('Capture Image'):
        #img_filename = "captured_image.png"
        #img_path = os.path.join("temp_images", img_filename)
        #picam2.capture_file(img_path)
        img_path=capture_image()
        st.success("Image captured successfully!")
        # Read the captured image
        uploaded_image = PIL.Image.open(img_path)
        # Display the captured image
        st.image(uploaded_image, caption="Captured Image", use_column_width=True)
        #if st.sidebar.button('Detect beans'):
        # Read captured image
        captured_image_cv2 = cv2.imread(img_path)

        # Detect beans
        res = model.predict(captured_image_cv2, conf=confidence)
        boxes = res[0].boxes
        res_plotted = res[0].plot()[:, :, ::-1]
        st.image(res_plotted, caption='Detected Image', use_column_width=True)
        
        # Calculate class_names for coffee quality classification
        class_names = [res[0].names[int(box.data[0][-1])] for box in boxes]
        
        # Classify coffee quality
        quality = classify_coffee_quality(class_names)
        
        # Display coffee quality result
        st.write("Coffee Quality:", quality)

        # Display temperature recommendation
        st.write("Temperature Recommendation:", temperature_recommendation(dht_temperature))

        # Display humidity recommendation
        st.write("Humidity Recommendation:", humidity_recommendation(dht_humidity))
        res, detected_classes = detect_objects(uploaded_image, confidence)
        
        
        res_plotted = res[0].plot()[:, :, ::-1]
        t.image(res_plotted, caption='Detected Image', use_column_width=True)
        st.session_state['detected_image'] = res_plotted
        st.session_state['detected_classes'] = detected_classes
        quality_comment, quality_reason, total_count = assess_quality(detected_classes)
        st.session_state['quality_comment'] = quality_comment
        st.session_state['quality_reason'] = quality_reason
        st.session_state['total_count'] = total_count
        st.session_state['dht_temperature'] = dht_temperature
        st.session_state['dht_humidity'] = dht_humidity
        st.session_state['temperature_recommendation'] = temperature_recommendation
        st.session_state['humidity_recommendation'] = humidity_recommendation
        try:
            with st.expander("Detection Results"):
                for box in boxes:
                    for r in res:
                        class_index = int(box.data[0][-1])
                        class_name = r.names[class_index]
                        score = float(box.data[0][-2])
                        st.write(f"Class: {class_name.upper()} Confidence: {score*100:.1f}%")
        except Exception as ex:
            st.write("No image is captured yet!")
        
        # Count of coffee beans for each class
        st.write("Count of coffee beans:")
        bean_counts = {}
        for class_name in set(class_names):
            count = class_names.count(class_name)
            bean_counts[class_name] = count
        for class_name, count in bean_counts.items():
            st.write(f"- {class_name}: {count}")
         # Unique identifier for each detected image
            if not os.path.exists("results"):
                        os.makedirs("results")
            unique_id = f"Sample{len(os.listdir('results')) + 1}"
                    
                    # Save detected image
            detected_image_path = os.path.join("results", f"{unique_id}.png")
            try:
                        PIL.Image.fromarray(res_plotted).save(detected_image_path)
            except Exception as e:
                        st.error(f"Error saving image: {e}")
                    
                    # Save results to text file
            with open(os.path.join("results", f"{unique_id}.txt"), "w") as f:
                        f.write(f"Detected Image: {unique_id}\n")
                        f.write(f"Coffee Quality: {quality}\n")
                        f.write(f"Temperature Recommendation: {temperature_recommendation(dht_temperature)}\n")
                        f.write(f"Humidity Recommendation: {humidity_recommendation(dht_humidity)}\n")
                        f.write("Count of coffee beans:\n")
                        for class_name, count in bean_counts.items():
                            f.write(f"- {class_name}: {count}\n")  


# Create "HISTORY" button
import os

if st.button("HISTORY"):
    # Display history page
    st.title("History of Detected Images")
    st.write("This is the history page. Here, you can see the results of all detected images.")

    # List all image files from the "results" directory
    results_files = os.listdir("results")
    image_files = [file for file in results_files if file.endswith(".png")]

    # Iterate over each image file
    for image_file in image_files:
        image_path = os.path.join("results", image_file)
        # Display the image
        st.image(image_path, caption=f"Detected Image: {image_file}", width=200)

        # Find the corresponding text result file
        result_file = image_file.replace(".png", ".txt")
        result_path = os.path.join("results", result_file)

        # Display the text result if it exists
        if os.path.exists(result_path):
            with open(result_path, "r") as f:
                result_content = f.read().strip()
                # Wrap each line of the result in a <pre> tag to maintain formatting
                formatted_result = "\n".join([f"<pre>{line}</pre>" for line in result_content.split("\n")])
                # Display the formatted result
                st.write(formatted_result, unsafe_allow_html=True)
        else:
            st.error(f"No result file found for image: {image_file}")
            
            
# Email Sending
st.sidebar.header("Send Quality Report")
companies = {
    "KAWAcom": "juukojuniorfrancis@gmail.com",
    "Qualicoff": "mulungidestinysanyu@gmail.com",
    "ECG": "statesmanhardwell@gmail.com",
    # Add more companies as needed
}
selected_company = st.sidebar.selectbox("Select Company:", list(companies.keys()))
receiver_email = companies[selected_company]



# Button to send email and generate PDF
if st.sidebar.button("Send Report") and st.session_state['detected_image'] is not None:
#    try:
    temp_image_path = save_temp_image(PIL.Image.fromarray(st.session_state['detected_image']))
    pdf_filename = generate_pdf_report(st.session_state['quality_comment'], st.session_state['quality_reason'],
                                       st.session_state['detected_classes'], st.session_state['total_count'], 
                                       st.session_state['dht_humidity'], st.session_state['dht_temperature'], st.session_state['humidity_recommendation'], 
                                       st.session_state['temperature_recommendation'], image_path=temp_image_path)
    send_report(receiver_email, st.session_state['quality_comment'], st.session_state['quality_reason'], pdf_filename, temp_image_path)
#    except Exception as e:
#        st.error(f"Error generating report: {e}")
else:
    st.sidebar.error("No detection results available. Please detect objects first.")
            
            
            
            
            
            
            

