#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pydantic import FilePath
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
    # root = tk.Tk()
    # root.withdraw()
    # file_path = filedialog.askopenfilename()

    # Load the selected image file
    image = Image.open(file_path)

    # Convert the image to a numpy array
    image = np.asarray(image)

    # Use the YOLOv8 model to predict objects in the image
    results = model.predict(image,save=True)
    
    my_list= os.listdir('runs/detect')
    max_value = max(map(int, [s.replace('predict', '') for s in my_list if s != 'predict']))
    
    image_path=f"runs/detect/predict"+str(max_value)+"/image0.jpg"
    class_names=[]
    for r in results:
        for c in r.boxes.cls:
            if model.names[int(c)] not in class_names:
                class_names.append(model.names[int(c)])
            else:
                pass
    return image_path,class_names

cv2.waitKey(0)
cv2.destroyAllWindows()


