# Importing all required libraaries
try:
    import sys
    import tkinter as tk
    from tkinter import *
    from tkinter import messagebox
    import numpy as np
    import PIL

    from PIL import Image , ImageTk
    from tkinter import ttk

    import argparse
    import datetime
    import cv2
    import os
except:
    print("Error in importing libraries. Kindly check whether libraries are properly installed!")
    sys.exit()    
    
dir = os.getcwd()
global sampleNum #creating global variable
sampleNum = 0
global last_frame                                      #creating global variable
last_frame = np.zeros((480, 640, 3), dtype=np.uint8)
global cap #creating global variable
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
face_cascade = cv2.CascadeClassifier(dir+"\\"+"haarcascades\\haarcascade_frontalface_default.xml")
imgs_folder = dir+"\\"+"train_images\\"


def video_loop():
    global name_, roll_ , cap
    sampleNum = 0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)
    name_ = name.get()
    roll_ = roll_num.get()
    name.delete(0, END)
    roll_num.delete(0,END)
    if roll_ != '':
        show_vid()
    else:
        messagebox.showinfo("Error!!!","Please Enter Name and Roll number")

# Defining a function which will open the folder where images are saved, to check and delete unwanted photos manually.
def open_folder():
    try:
        path=os.getcwd()+"\\train_images"
    except:
        os.mkdir('train_images')
        path=os.getcwd()+"\\train_images"
    path=os.path.realpath(path)
    os.startfile(path)

def show_vid():    #creating a function
    id_name = roll_
    if not cap.isOpened():                             #checks for the opening of camera
        print("cant open the camera")
    flag, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if flag is None:
        print ("Major error!")
    elif flag:
        global last_frame
        last_frame = frame.copy()

    pic = cv2.cvtColor(last_frame, cv2.COLOR_RGB2BGR) #we can change the display color of the frame gray,black&white here
    faces = face_cascade.detectMultiScale(pic,scaleFactor=1.3,minNeighbors=6,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    for x,y,w,h in faces:
        global sampleNum
        sampleNum += 1
        cv2.imwrite(imgs_folder + "User."+str(id_name)+"." + str(sampleNum) + ".jpg", frame[y:y+h,x:x+w])
        cv2.rectangle(pic, (x, y), (x+w-15, y+h), (0, 255, 0), 2)
    if sampleNum >= 200:
        messagebox.showinfo("Information!!!","Successfully captured images")
        sampleNum = 0
        cap.release()
        cv2.destroyAllWindows()
        return
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img)
    panel.imgtk = imgtk
    panel.configure(image=imgtk)
    panel.after(10, show_vid)

def del_train():
    ans  = messagebox.askyesno(title = 'Confirmation', message ='Are you sure you want to delete all images?')
    if ans:
        train_imgs_path = os.getcwd() + "\\train_images"
        for i in os.listdir(train_imgs_path):
            os.remove(train_imgs_path + "\\" + i)
    else:
        print()
    
    
def train_images():
    os.system("python Cap_Train_images.py")

def destructor():
    """ Destroy the root object and release all resources """
    root.destroy()
    cap.release()
    cv2.destroyAllWindows()  # it is not mandatory in this application

faceCascade = cv2.CascadeClassifier(os.getcwd()+"\\haarcascades\\haarcascade_frontalface_default.xml")


""" Initialize application which uses OpenCV + Tkinter. It displays
    a video stream in a Tkinter window and stores current snapshot on disk """

current_image = None  # current image from the camera

root = tk.Tk()  # initialize root window
root.geometry('1200x600')
root.title("Attendance")  # set window title
#function gets fired when the window is closed
root.protocol('WM_DELETE_WINDOW', destructor)
panel = Label(root, background = 'black', padx = 320, pady = 230)  # initialize image panel

panel.pack(padx=10, pady=10)

root.config(cursor="arrow")
#create a button, that when pressed, will take the current frame and save it to file
global  name
global  roll_num


attdButton = Label(root, text = "ATTENDANCE", font = ("Arial", 20), bg = 'maroon', fg = 'white')
attdButton.place(x = 50, y = 50)

startButton = Button(root, text = "Start", borderwidth = 2, relief = 'raised', font = ("Arial", 20), padx = 50, bg = 'dark blue', fg = 'white', command = video_loop)
startButton.place(x = 970, y = 160)


closeButton = Button(root, text = "Close", font = ("Arial", 20), padx = 43, bg="dark blue",fg='white', command = destructor)
closeButton.place(x = 970, y = 430)

checkButton = Button(root, text = "Check", font = ("Arial", 20), padx = 40, bg="dark blue",fg='white',command = open_folder)
checkButton.place(x = 970, y = 250)

trainButton = Button(root, text = 'Train', font = ("Arial", 20), padx = 47, bg = 'dark blue', fg = 'white',command =  train_images)
trainButton.place(x = 970, y = 340)


deleteallButton = Button(root, text = "Delete Train Images!", font = ("Arial Bold", 10), bg = 'maroon', fg ='white', command = del_train)
deleteallButton.place(x = 50, y = 450)


nameLabel = Label(root, text = "Name", font = ("Arial Bold", 10))
nameLabel.place(x = 50, y = 100)
name = Entry(root)
name.place(x = 50, y = 140)



roll_numLabel = Label(root, text = "Roll Number", font = ("Arial Bold", 10))
roll_numLabel.place(x = 50, y = 160)
roll_num = Entry(root)
roll_num.place(x = 50, y = 200)


datetimeButton = Label(root, borderwidth = 2, relief = 'groove', text = "Date : " + str(datetime.datetime.now().strftime("%d-%m-%Y")), font = ("Arial Bold", 17), padx = 30)
datetimeButton.place(x = 935, y = 50)


# start the app

root.mainloop()


