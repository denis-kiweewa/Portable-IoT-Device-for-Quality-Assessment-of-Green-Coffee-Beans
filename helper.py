from ultralytics import YOLO
import cv2
import os
import uuid
import streamlit as st

import settings


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def capture_image_r():
    """
    Captures an image using the PiCamera.

    Returns:
        str: File path of the captured image.
    """
    try:
        from picamera2 import Picamera2, Preview
        import time
        
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
        picam2.configure(camera_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(2)
        img_filename = f"captured_image_{uuid.uuid4().hex}.jpg"
        img_path = os.path.join("temp_images", img_filename)
        picam2.capture_file(img_path)
        return img_path
    except Exception as e:
        st.sidebar.error("Error capturing image using PiCamera: " + str(e))
        return None


def detect_objects(conf, model, img_path):
    """
    Detects objects in the provided image using the YOLOv8 model.

    Parameters:
        conf: Confidence threshold for object detection.
        model: An instance of the YOLOv8 object detection model.
        img_path (str): File path of the image to detect objects in.

    Returns:
        tuple: A tuple containing the processed image and the bounding boxes.
    """
    try:
        if os.path.exists(img_path):
            captured_image = cv2.imread(img_path)
            res = model.predict(captured_image, conf=conf)
            boxes = res[0].boxes
            res_plotted = res[0].plot()[:, :, ::-1]

            # Unique identifier for each detected image
            if not os.path.exists("results"):
                os.makedirs("results")
            unique_id = f"Sample{len(os.listdir('results')) + 1}"
            
            # Save detected image
            detected_image_path = os.path.join("results", f"{unique_id}.png")
            cv2.imwrite(detected_image_path, res_plotted)

            # Save results to text file
            with open(os.path.join("results", f"{unique_id}.txt"), "w") as f:
                f.write(f"Detected Image: {unique_id}\n")
                for box in boxes:
                    class_index = int(box.data[0][-1])
                    class_name = res[0].names[class_index]
                    score = float(box.data[0][-2])
                    f.write(f"Class: {class_name.upper()} Confidence: {score*100:.1f}%\n")

            return res_plotted, boxes
        else:
            st.sidebar.warning("Please capture an image first.")
            return None, None
    except Exception as e:
        st.sidebar.error("Error detecting objects: " + str(e))
        return None, None


