This program is primarily written in python, and uses a lot of python modules.
Please install the following python libraries:
tkinter 
customtkinter 
numpy 
opencv 
Pillow
pygame 
pytorch 

Please run a verion of python 9 instead of 12 for compatibility with pytorch.

You download tkinter, cv2, nupmy, pygame, and torch and pillow and custom tkinter using pip.

pull yolov5 from github into the main folder:
git clone https://github.com/ultralytics/yolov5
run the following on your device:
pip install -r requirements.txt
drag the folder exp16 (which contains my trained model) into the the yolov5 folder into the folder called runs and then train folder.

run main.py.
If camera is not showing up, change line 241 from cap = cv2.VideoCapture(1) to cap = cv2.VideoCapture(0).

The way this program is configured, minutes were set to be seconds and hours minutes to more easily run. To change this, edit line 359 frame.after(1000, update_countdown, countdown_sec) to frame.after(60000, update_countdown, countdown_sec)

Video URL = https://youtu.be/hM-3leA6fQo