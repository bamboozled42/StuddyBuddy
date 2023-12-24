import torch 
from matplotlib import pyplot as plt
import numpy as np
import cv2
import ssl
import uuid
import os
import time

ssl._create_default_https_context = ssl._create_unverified_context
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
if model:
        print("Model loaded successfully.")
else:
        print("Error loading the model.")
cap = cv2.VideoCapture(1)
while cap.isOpened():
    ret, frame = cap.read()
    
    # Make detections 
    results = model(frame)
    
    cv2.imshow('YOLO', np.squeeze(results.render()))
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
