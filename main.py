import tkinter as tk
from tkinter import ttk
from tkinter import *
import customtkinter  as ctk
import numpy
import cv2
from PIL import Image, ImageTk
from pygame import mixer
import torch
import numpy as np
import time

# create a tkinter window
root = tk.Tk()

# define center root function
def center_window():
    # Receive the dimensions of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width / 2) - (root.winfo_reqwidth() / 2)
    y = (screen_height / 2) - (root.winfo_reqheight() / 2)

    # Set the window position
    root.geometry(f"+{int(x)}+{int(y)}")

root.geometry("700x500")
# set the window size and title
root.title("Study Buddy")
center_window()

# variables
# timer variables
selected_timer = tk.StringVar()
timer_rounds = tk.IntVar()
custom_study_hours = tk.IntVar()
custom_study_minutes = tk.IntVar()
custom_rest_hours = tk.IntVar()
custom_rest_minutes = tk.IntVar()

timer_hours = tk.StringVar()
timer_hours.set("00")
timer_minutes = tk.StringVar()
timer_minutes.set("00")
timer_label = tk.StringVar()
round_label = tk.StringVar()

current_round = tk.IntVar()
activity = tk.StringVar()
status = tk.StringVar()

counting = tk.BooleanVar()

# define frames
# define menu frame
def menu():
    menu_frame = tk.Frame(root, height=500, width=700, bg = "white")
    menu_frame.place(x=0, y=0)
    menu_frame.pack_propagate(False)

    bg = PhotoImage(file="styling/bg1.png")
    background_lbl = tk.Label(menu_frame, image=bg)
    background_lbl.image = bg
    background_lbl.place(x=0, y=0, relwidth=1, relheight=1)

    namelbl = tk.Label(menu_frame, text="STUDDY BUDDY", font=("Chalkduster", 32, "bold"), foreground="#e785de", background="white")
    namelbl.place(relx=0.5, rely=0.2, anchor="center")

    menu_instructionslbl = tk.Label(menu_frame, text="SELECT A STUDY TIMER", font=("Arial", 16, "bold"), foreground="#e5e784", background="white")
    menu_instructionslbl.place(relx=0.5, rely=0.4, anchor="center")

    pomodoro_btn = ttk.Button(menu_frame, text="Pomodoro", command=lambda: select_timer("pomodoro"))
    ultradian_btn = ttk.Button(menu_frame, text="Ultradian", command=lambda: select_timer("ultradian"))
    procrastination_btn = ttk.Button(menu_frame, text="Procrastination SOS", command=lambda: select_timer("procrastination"))
    custom_btn = ttk.Button(menu_frame, text="Custom Study Schedule", command=lambda: select_timer("custom"))

    # Use place to center the buttons vertically
    pomodoro_btn.place(relx=0.5, rely=0.5, anchor="center")
    ultradian_btn.place(relx=0.5, rely=0.55, anchor="center")
    procrastination_btn.place(relx=0.5, rely=0.6, anchor="center")
    custom_btn.place(relx=0.5, rely=0.65, anchor="center")



# define transition frames
def options():
    options_frame = tk.Frame(root, height=500, width=700, bg = "white")
    options_frame.place(x=0, y=0)
    options_frame.pack_propagate(False)

    bg = PhotoImage(file="styling/bg1.png")
    background_lbl = tk.Label(options_frame, image=bg)
    background_lbl.image = bg
    background_lbl.place(x=0, y=0, relwidth=1, relheight=1)

    selected_timerlbl = tk.Label(options_frame, textvariable=selected_timer, font=("Chalkduster", 32, "bold"), foreground="#e785de", background="white")
    selected_timerlbl.place(relx=0.5, rely=0.2, anchor="center")
    if selected_timer.get()=="pomodoro":
        timer_descriptionlbl = tk.Label(options_frame, text="The Pomodoro Technique, created by Francesco Cirillo, enhances productivity through focused work intervals lasting 25 minutes, followed by short breaks. After four Pomodoros, take a longer break of 15-30 minutes. This method combats procrastination, prevents burnout, and fosters a sense of accomplishment.", font=("Arial", 12, "italic"), foreground="#e5e784", background="white", wraplength=200)
    elif selected_timer.get()=="ultradian":
        timer_descriptionlbl = tk.Label(options_frame, text="The Ultradian Rhythm Technique optimizes productivity by leveraging natural body cycles. Work in focused intervals, or Ultradians, typically lasting 90 minutes, followed by a 20-minute break. The longer break after each Ultradian session promotes sustained focus, efficient task completion, and overall well-being. Adopt the Ultradian Rhythm Technique for improved time management and heightened productivity.", font=("Arial", 12, "italic"), foreground="#e5e784", background="white" , wraplength=200)
    else:
        timer_descriptionlbl = tk.Label(options_frame, text="The procrastination-busting method involves completing 12 rounds of 5-minute increments with 2-minute breaks in between. This approach is particularly effective when you find it challenging to initiate work or maintain focus. In total, you achieve one hour of focused work during these cycles.", font=("Arial", 12, "italic"), foreground="#e5e784", background="white", wraplength=200)
    timer_descriptionlbl.place(relx=0.5, rely=0.4, anchor="center")

    # create internal grid frame
    form_frame = tk.Frame(options_frame, bg = "white")
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=1)
    form_frame.place(relx=0.5, rely=0.6, anchor="center")

    # implement form
    if selected_timer.get() != "procrastination":
        round_lbl = tk.Label(form_frame, text="Select Number of Rounds: ")
        round_lbl.grid(row=0, column=0)
        round_response = tk.Entry(form_frame)
        round_response.grid(row=0, column=1)
    else:
        round_response = 12
    # return to menu
    back_btn = ttk.Button(form_frame, text="Cancel", command=menu)
    back_btn.grid(row=2, column=0)
    submit_btn = ttk.Button(form_frame, text="Start", command=lambda: options_next(round_response))
    submit_btn.grid(row=2, column=1)

def counter_screen():
    counter_frame = tk.Frame(root, height=500, width=700, bg = "white")
    counter_frame.place(x=0, y=0)
    counter_frame.pack_propagate(False)
    
    bg = PhotoImage(file="styling/bg1.png")
    background_lbl = tk.Label(counter_frame, image=bg)
    background_lbl.image = bg
    background_lbl.place(x=0, y=0, relwidth=1, relheight=1)
    countdown(counter_frame)



def custom():
    custom_frame = tk.Frame(root, height=500, width=700, bg = "white")
    custom_frame.place(x=0, y=0)
    custom_frame.pack_propagate(False)

    bg = PhotoImage(file="styling/bg1.png")
    background_lbl = tk.Label(custom_frame, image=bg)
    background_lbl.image = bg
    background_lbl.place(x=0, y=0, relwidth=1, relheight=1)

    selected_timerlbl = tk.Label(custom_frame, textvariable = selected_timer, font=("Chalkduster", 32, "bold"), foreground="#e785de", background="white")
    selected_timerlbl.place(relx=0.5, rely=0.2, anchor="center")
    # create internal grid frame
    form_frame = tk.Frame(custom_frame)
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=1)
    form_frame.place(relx=0.5, rely=0.6, anchor="center")
    # implement form
    study_time_lbl = tk.Label(form_frame, text="Select Time for Study Session: ")
    study_time_lbl.grid(row=0, column=0)
    study_time_hour_lbl = tk.Label(form_frame, text="Hour: ")
    study_time_hour_lbl.grid(row=1, column=0)
    study_hour_select = tk.Spinbox(form_frame, from_=0, to=23)
    study_hour_select.grid(row=1, column=1)
    study_time_minute_lbl = tk.Label(form_frame, text="Minute: ")
    study_time_minute_lbl.grid(row=2, column=0)
    study_minute_select = tk.Spinbox(form_frame, from_=0, to=59)
    study_minute_select.grid(row=2, column=1)

    rest_time_lbl = tk.Label(form_frame, text="Select Time for Break Period: ")
    rest_time_lbl.grid(row=3, column=0)
    rest_time_hour_lbl = tk.Label(form_frame, text="Hour: ")
    rest_time_hour_lbl.grid(row=4, column=0)
    rest_hour_select = tk.Spinbox(form_frame, from_=0, to=23)
    rest_hour_select.grid(row=4, column=1)
    rest_time_minute_lbl = tk.Label(form_frame, text="Minute: ")
    rest_time_minute_lbl.grid(row=5, column=0)
    rest_minute_select = tk.Spinbox(form_frame, from_=0, to=59)
    rest_minute_select.grid(row=5, column=1)

    round_lbl = tk.Label(form_frame, text="Select Number of Rounds: ")
    round_lbl.grid(row=6, column=0)
    round_response = tk.Entry(form_frame)
    round_response.grid(row=6, column=1)

    # return to menu
    back_btn = ttk.Button(form_frame, text="Cancel", command=menu)
    back_btn.grid(row=7, column=0)
    submit_btn = ttk.Button(form_frame, text="Next",
                            command=lambda: custom_next(study_minute_select, study_hour_select, rest_minute_select,
                                                        rest_hour_select, round_response))
    submit_btn.grid(row=7, column=1)

# define countdown frames

# define the home frame
def home():
    root.geometry("1200x1000")
    center_window()

    home_frame = tk.Frame(root, height=1000, width=1200, bg = "white")
    home_frame.place(x=0, y=0)
    home_frame.pack_propagate(False)
    
    bg = PhotoImage(file="styling/bg4.png")
    background_lbl = tk.Label(home_frame, image=bg)
    background_lbl.image = bg
    background_lbl.place(x=0, y=0, relwidth=1, relheight=1)

    typelbl = tk.Label(home_frame, textvariable = selected_timer, font=("Chalkduster", 32, "bold"), foreground="#e785de", background="white")
    typelbl.place(relx=0.5, rely=0.05, anchor="center")
    # create control center
    form_frame = tk.Frame(home_frame)
    form_frame.place(relx=0.5, rely=0.15, anchor="center")
    round_lbl = tk.Label(form_frame, text="Round: ")
    round_lbl.grid(row=0, column=0)
    current_round_lbl = tk.Label(form_frame, textvariable= round_label)
    current_round_lbl.grid(row=0, column=1)
    exit_btn = ttk.Button(form_frame, text="Exit", command= lambda: exit(home_frame))
    exit_btn.grid(row=1, column=0)

    #timer
    activity_lbl = tk.Label(home_frame, textvariable = activity, font=("Chalkduster", 24, "bold"), foreground="#e5e784", background="white")
    activity_lbl.place(relx=0.5, rely=0.1, anchor="center")
    timer_lbl = tk.Label(home_frame, textvariable = timer_label, font=("Courier New", 24, "bold"), foreground="white", background="#e785de")
    timer_lbl.place(relx=0.5, rely=0.2, anchor="center")

    #create frame for camera view
    vidFrame = tk.Frame(home_frame, width = 1000, height = 700)
    vidFrame.place(relx=0.5, rely=0.6, anchor="center")
    home_frame.pack_propagate(False)
    #populate camera view
    vid_lbl = ctk.CTkLabel(vidFrame, text = "")
    vid_lbl.place(relx=0.5, rely=0.5, anchor="center")

    # declare the models
    modelsleep_path = 'yolov5/runs/train/exp16/weights/last.pt'
    model_sleep = torch.hub.load('ultralytics/yolov5', 'custom', path=modelsleep_path)
    global last_played_time
    last_played_time = 0
    cap = cv2.VideoCapture(1)
    mixer.init()
    mixer.music.load("styling/sound-of-the-police.mp3")




    def record_video(vid_lbl):
        global last_played_time
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_sleeping = model_sleep(frame)
        img = np.squeeze(results_sleeping.render())
        singular = results_sleeping.xywh[0]
        if (len(singular) > 0.8 and singular.size(0) == 1) and (activity.get() == 'study' and status.get()=="playing"):
            dconf = singular[:, 4]
            dclass = singular[:, 5]
            current_time = time.time()
            time_since_last_play = current_time - last_played_time
            if (dconf.item() > 0.4 and (dclass == 15).any()) and (time_since_last_play > 5):
                print("at the mixer")
                mixer.music.play()
                last_played_time = current_time
        #results_phone = model_phone(frame)
        img_array = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(img_array)
        vid_lbl.imgtk = imgtk
        vid_lbl.configure(image = imgtk)
        vid_lbl.after(10, record_video, vid_lbl)
    record_video(vid_lbl)



    #start timer
    activity.set("study")
    status.set("playing")
    print("status set " + status.get())
    pause_btn = ttk.Button(form_frame, text= "Pause", command = lambda: pp_func (pause_btn, home_frame))
    pause_btn.grid(row=1, column=1)
    print(selected_timer.get())

    # start timer
    if (selected_timer.get() == "pomodoro"):
        print("in pomodoro function")
        start_pomodoro_timer(home_frame)
    elif (selected_timer.get() == "ultradian"):
        start_ultradian_timer(home_frame)
    elif (selected_timer.get() == "procrastination"):
        start_procrastination_timer(home_frame)
    else:
        start_custom_timer(home_frame)

# functions
# selecting timer type in menu frame
def select_timer(timer_type):
    selected_timer.set(timer_type)
    if (timer_type == "pomodoro" or timer_type == "ultradian" or timer_type == "procrastination"):
        options()
    else:
        custom()

# moving onto the main page from the options frame
def options_next(round_entry):
    # validate round_no
    if selected_timer.get() == "procrastination":
        timer_rounds.set(12)
        current_round.set(1)
        counter_screen()
    else:
        round_no = round_entry.get()
        if (round_no.isdigit() and int(round_no) > 0):
            timer_rounds.set(round_no)
            current_round.set(1)
            counter_screen()
        else:
            round_entry.delete(0, tk.END)
        # handle error


def custom_next(study_minute_entry, study_hour_entry, rest_minute_entry, rest_hour_entry, round_entry):
    study_minute = int(study_minute_entry.get())
    study_hour = int(study_hour_entry.get())
    rest_minute = int(rest_minute_entry.get())
    rest_hour = int(rest_hour_entry.get())
    round_value = round_entry.get()
    # validate if round is inputted
    if (round_value and round_value.isdigit() and int(round_value) > 0):
        round_no = int(round_value)
        # check the following exists
        # !!add check for input validation
        if (study_minute != 0 or study_hour != 0) and (rest_minute != 0 or rest_hour != 0):
            custom_study_minutes.set(study_minute)
            custom_study_hours.set(study_hour)
            custom_rest_minutes.set(rest_minute)
            custom_rest_hours.set(rest_hour)
            timer_rounds.set(round_no)
            current_round.set(1)
            home()
        else:
            # !!add error message
            pass
    else:
        round_entry.delete(0, tk.END)
        # !!add error message

#home functions
#time related functions
#count down at start and after pause
def countdown(frame):
    countdown_sec = 4
    countdown_lbl = tk.Label(frame, text = countdown_sec, font=("Chalkduster", 64, "bold"), foreground="#e785de", background="white")
    countdown_lbl.place(relx=0.5, rely=0.5, anchor="center")
    # using recursion update the countdown
    def update_countdown(countdown_sec):
        if countdown_sec > 0:
        # Decrement the countdown and schedule the next update
            countdown_sec -= 1
            countdown_lbl.config(text = countdown_sec)
            frame.after(1000, update_countdown, countdown_sec)
            print("Round")
        else:
            home()    
    update_countdown(countdown_sec)
   

#pause the timer function
def pp_func(pause_btn, home_frame):
    if (status.get() == "playing"):
        pause_btn.config(text = "Play")
        status.set("paused") 
    else:
        pause_btn.config(text = "Pause")
        status.set("playing")
        countdown_minutes_total = int(timer_minutes.get()) * 60 + int(timer_hours.get())  
        print(countdown_minutes_total)
        run_timer(home_frame, countdown_minutes_total)

#timer functions
#pomodoro timer
def start_pomodoro_timer(home_frame):
    if (current_round.get() <= timer_rounds.get() and status.get() == "playing"):
        if (activity.get() == "study"):
            round_label.set(f"{current_round.get()}/{timer_rounds.get()}")
            timer_hours.set("00") 
            timer_minutes.set("25")
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            print(timer_minutes.get())
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
        elif (activity.get() == "break") and (current_round.get() == timer_rounds.get()):
            #!!!condition to finish study session
            print ("Done with study session")
            exit(home_frame)
        elif (activity.get() == "break") and (current_round.get() % 4 == 0):
            timer_hours.set("00") 
            timer_minutes.set("30")
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            current_round.set(current_round.get() + 1)
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
        elif (activity.get() == "break"):
            timer_hours.set("00") 
            timer_minutes.set("05")
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            current_round.set(current_round.get() + 1)
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
    else:
        #!! condition for stopping timer
        pass
            
#ultradian timer
def start_ultradian_timer(home_frame):
    if (current_round.get() <= timer_rounds.get() and status.get() == "playing"):
        if (activity.get() == "study"):
            round_label.set(f"{current_round.get()}/{timer_rounds.get()}")
            timer_hours.set("01") 
            timer_minutes.set("30")
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            print(timer_minutes.get())
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
        elif (activity.get() == "break") and (current_round.get() == timer_rounds.get()):
            #!!!condition to finish study session
            print ("Done with study session")
            exit(home_frame)
        elif (activity.get() == "break"):
            timer_hours.set("00") 
            timer_minutes.set("20")
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            current_round.set(current_round.get() + 1)
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
    else:
        #!! condition for stopping timer
        pass

#procrastination timer
def start_procrastination_timer(home_frame):
    if (current_round.get() <= timer_rounds.get() and status.get() == "playing"):
        if (activity.get() == "study"):
            round_label.set(f"{current_round.get()}/{timer_rounds.get()}")
            timer_hours.set("00") 
            timer_minutes.set("05")
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            print(timer_minutes.get())
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
        elif (activity.get() == "break") and (current_round.get() == timer_rounds.get()):
            #!!!condition to finish study session
            print ("Done with study session")
            exit(home_frame)
        elif (activity.get() == "break"):
            timer_hours.set("00") 
            timer_minutes.set("02")
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            current_round.set(current_round.get() + 1)
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
    else:
        #!! condition for stopping timer
        pass
#custom timer
def start_custom_timer(home_frame):
    if (current_round.get() <= timer_rounds.get() and status.get() == "playing"):
        if (activity.get() == "study"):
            round_label.set(f"{current_round.get()}/{timer_rounds.get()}")
            timer_hours.set(custom_study_hours.get()) 
            timer_minutes.set(custom_study_minutes.get())
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            print(timer_minutes.get())
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
        elif (activity.get() == "break") and (current_round.get() == timer_rounds.get()):
            #!!!condition to finish study session
            print ("Done with study session")
            exit(home_frame)
        elif (activity.get() == "break"):
            timer_hours.set(custom_rest_hours.get()) 
            timer_minutes.set(custom_rest_minutes.get())
            timer_label.set(f"{timer_hours.get()}:{timer_minutes.get()}")
            current_round.set(current_round.get() + 1)
            countdown_minutes_total = int(timer_minutes.get()) + int(timer_hours.get()) * 60
            run_timer(home_frame, countdown_minutes_total)
    else:
        #!! condition for stopping timer
        pass

#run any timer
#apply recursion
def run_timer(home_frame, countdown_minutes_total):
    print("I am here!!")
    # using recursion update the countdown
    def update_timer(countdown_minutes_total):
        if (countdown_minutes_total > 0 and status.get() == "playing"):
            print("Minute down")
        # Decrement the countdown and schedule the next update
            remaining_minutes, remaining_hours = divmod(countdown_minutes_total, 60)
            timer_minutes.set(f"{remaining_minutes:02d}")
            timer_hours.set(f"{remaining_hours:02d}")
            timer_label.set(f"{timer_minutes.get()}:{timer_hours.get()}")
            countdown_minutes_total -= 1
            home_frame.after(1000, update_timer, countdown_minutes_total)
        else:
            if status.get() == "paused":
                pass
            elif activity.get() == "study":
                activity.set("break")
            else:
                activity.set("study")
            if (selected_timer.get() == "pomodoro"):
                start_pomodoro_timer(home_frame)
            elif (selected_timer.get() == "ultradian"):
                start_ultradian_timer(home_frame)
            elif (selected_timer.get() == "procrastination"):
                start_procrastination_timer(home_frame)
            else:
                start_custom_timer(home_frame)
    # Schedule the first update
    update_timer(countdown_minutes_total)               

#function to exit    
def exit(home_frame):
    status.set("exit")
    home_frame.destroy()
    root.geometry("700x500")
    menu()

def detect_distractions(Label):
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img_array = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(img_array)
    Label.configure(image = imgtk)
    Label.after(10, detect_distractions, Label)



menu()

root.mainloop()
