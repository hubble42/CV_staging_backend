import os
from ultralytics import YOLO
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import cv2
from IPython.display import display


def check(file_path, filename, class_list):
    # Load the YOLOv8 model
    model = YOLO("yolov8n.pt")

    # Prompt the user to select an image file
    # root = tk.Tk()
    # root.withdraw()
    # file_path = filedialog.askopenfilename()

    # Load the selected image file

    # Use the YOLOv8 model to predict objects in the image
    results = model.predict(
        source=file_path, save=True, classes=class_list)

    my_list = os.listdir('runs/detect')
    max_value = max(map(int, [s.replace('predict', '')
                              for s in my_list if s != 'predict']))

    video_path = f"runs/detect/predict"+str(max_value)+"/"+str(filename)

    return video_path
