#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from ultralytics import YOLO
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import cv2
from IPython.display import display

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Prompt the user to select an image file
root = tk.Tk()
root.withdraw()

# ask user to select a video file
file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])

num_classes = int(input("How many classes do you want to create? "))

class_names = []
for i in range(num_classes):
    class_name = int(input(f"Enter the name of class {i+1}: "))
    class_names.append(class_name)


# Use the YOLOv8 model to predict objects in the image
results = model.predict(source=file_path,save=True,classes=class_names)


cv2.waitKey(0)
cv2.destroyAllWindows()


