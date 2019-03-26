try:
    import sys
    from tkinter import Label, Button, Tk, StringVar, OptionMenu, Entry, END
    import PIL
    import pygame
    import pandas as pd
    from PIL import Image as Img, ImageTk
    from tkinter.simpledialog import askstring
    from tkinter import ttk
    from tkinter import messagebox
    import shutil
    import argparse
    import datetime
    import cv2
    import os
except:
    print("Error in importing libraries. Kindly check whether libraries are properly installed!")
    sys.exit()

faceCascade = cv2.CascadeClassifier(os.getcwd()+"\\haarcascades\\haarcascade_frontalface_default.xml")



class Application:
    def __init__(self, output_path = "./"):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera
 
        self.root = Tk()  # initialize root window
        self.root.geometry('1200x600')
        self.root.title("Attendance")  # set window title
        self.destructor #function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.panel = Label(self.root, background = 'maroon', padx = 320, pady = 230)  # initialize image panel
        
        self.panel.pack(padx=10, pady=10)
        
        self.root.config(cursor="arrow")
        global cam, period, faculty, subject
        period = StringVar(self.root)
        faculty = StringVar(self.root)
        subject = StringVar(self.root)
        cam = StringVar(self.root)
        #create a button, that when pressed, will take the current frame and save it to file
 
        attdButton = Label(self.root, text = "ATTENDANCE", font = ("Arial", 20), bg = 'maroon', fg = 'white')
        attdButton.place(x = 50, y = 50)
        
        startButton = Button(self.root, text = "Start", borderwidth = 2, relief = 'raised', font = ("Arial", 20), padx = 50, bg = 'dark blue', fg = 'white', command = self.start_cam)
        startButton.place(x = 970, y = 160)
        
        
        closeButton = Button(self.root, text = "Close", font = ("Arial", 20), padx = 45, bg="dark blue",fg='white', command = self.destructor)
        closeButton.place(x = 970, y = 430)
        
        updateButton = Button(self.root, text = "Update", font = ("Arial", 20), padx = 35, bg="dark blue",fg='white', command = self.update)
        updateButton.place(x = 970, y = 250)
        
        emailButton = Button(self.root, text = 'Email', font = ("Arial", 20), padx = 45, bg = 'dark blue', fg = 'white', command = self.email)
        emailButton.place(x = 970, y = 340)
        
        cam = " "
        global camMenu
        camMenu = Entry(self.root)
        camMenu.place(x = 50, y = 410)
        
        camLabel = Label(self.root, text = 'Choose Camera', font = ("Arial Bold", 10))
        camLabel.place(x = 50, y = 390)
        
        global lst_subject, lst_faculty
        facsub = pd.read_csv('Sub_fac.csv')
        subject_name  = facsub['Subject']
        faculty_name  = facsub['Faculty']
        lst_subject = subject_name.tolist()
        lst_faculty = faculty_name.tolist()

 
        
        
        periodLabel = Label(self.root, text = 'Choose Period', font = ("Arial Bold", 10))
        periodLabel.place(x = 50, y = 180)
        
        choices_period = ["1"+" "*30,"2"+" "*30,"3"+" "*30,"4"+" "*30,"5"+" "*30,"6"+" "*30,"7"+" "*30,"8"+" "*30]
        period.set("Period")
        popupMenu = OptionMenu(self.root, period, *choices_period)
        popupMenu.place(x = 50, y = 200)

        def change_period(*args):
            global selected_period
            selected_period = period.get()
 
        # link function to change dropdown
        period.trace('w', change_period)

        facultyLabel = Label(self.root, text = 'Choose Faculty', font = ("Arial Bold", 10))
        facultyLabel.place(x = 50, y = 250)
        
        length = 25
        lst_faculty = [i + " "*(length - len(i)) for i in lst_faculty]
        choices_faculty = lst_faculty
        faculty.set("Faculty")
        popupMenu_f = OptionMenu(self.root, faculty, *choices_faculty)
        popupMenu_f.place(x = 50, y = 270)

        def change_faculty(*args):
            global selected_faculty
            selected_faculty = faculty.get()
        
        faculty.trace('w', change_faculty)
        
        
        subjectLabel = Label(self.root, text = 'Choose Subject', font = ("Arial Bold", 10))
        subjectLabel.place(x = 50, y = 320)
        
        lst_subject = [i + " "*(length - len(i)) for i in lst_subject]
        choices_subject = lst_subject
        subject.set("Subject")
        popupMenu_s = OptionMenu(self.root, subject, *choices_subject)
        popupMenu_s.place(x = 50, y = 340)

        def change_subject(*args):
            global selected_subject
            selected_subject = subject.get()
        
        subject.trace('w', change_subject)
        
        
        datetimeButton = Label(self.root, borderwidth = 2, relief = 'groove', text = "Date : " + str(datetime.datetime.now().strftime("%d-%m-%Y")), font = ("Arial Bold", 17), padx = 30)
        datetimeButton.place(x = 935, y = 50)
        
      
        
        snapbtn = Button(self.root, text="Snapshot!",
            command=self.take_snapshot, padx = 50, pady = 10, bg = 'dark blue', font = ("Arial Bold", 10), fg = 'white')
        snapbtn.place(x = 500, y = 500 )
        



    def start_cam(self):
        global camMenu
        global period, faculty, subject
        selected_period = period.get()
        selected_faculty = faculty.get()
        selected_subject = subject.get()
        if (selected_period == 'Period' or selected_faculty == 'Faculty' or selected_subject == 'Subject'):
            messagebox.showinfo("Error!!!","Please select period, faculty and subject")
        else:
            cam = camMenu.get()
            camMenu.delete(0, END)
            if not cam.startswith('http'):
                self.vs = cv2.VideoCapture(0)
            else:
                self.vs = cv2.VideoCapture(cam + "/video")
            self.video_loop()
        

    
    def email(self):
        toaddr = askstring("Email ID","Enter Receiver email : ") 
        ccaddr = askstring("Email ID","Enter CC email : ") 
        try:
            os.system("python Cap_Email.py" + " " + selected_subject + " " + selected_faculty + " " + toaddr + " " + ccaddr)
        except:
            messagebox.showinfo("Error!!!","Please follow the User Manual")
    
    def update(self):
        try:
            os.system('python Cap_Recognize_images.py' + " " + selected_subject + " " + selected_faculty + " " + selected_period)
        except:
            messagebox.showinfo("Error!!!","Please follow the User Manual")
    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, self.frame = self.vs.read()# read frame from video stream
        if not ok:
            self.vs = cv2.VideoCapture(0)
            ok, self.frame = self.vs.read()
            
        if ok:  # frame captured without any errors
            key = cv2.waitKey(1000)
            
            faces = faceCascade.detectMultiScale(self.frame,scaleFactor=1.3,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
            for f,(x, y, w, h) in enumerate(faces):
                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Img.fromarray(cv2image)  # convert image for PIL

            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter 
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector  
            self.panel.config(image=imgtk)  # show the image

        self.root.after(1, self.video_loop)  # call the same function after 30 milliseconds
        
       
 
    def take_snapshot(self):
        pygame.init()
        pygame.mixer.music.load("click_sound.mp3") #Loading File Into Mixer
        pygame.mixer.music.play() 
        #Playing It In The Whole Device
        """ Take snapshot and save it to the file """
        ts = datetime.datetime.now() # grab the current timestamp
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        p = os.path.join(self.output_path, filename)  # construct output path
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))
    
    
    
    def destructor(self):
        try:
            files = os.listdir(os.getcwd() + "/" + 'group_images/')
        except:
            os.mkdir('group_images')
            files = os.listdir(os.getcwd() + "/" + 'group_images/')
        for f in files:
            try:
                os.mkdir('history')
                history_path = os.getcwd() + '/history'
            except:
                history_path = os.getcwd() + '/history'
            
            
            shutil.move(os.getcwd() + "/" + 'group_images/' + f, history_path)

        
        
        """ Destroy the root object and release all resources """
        
        self.root.destroy()
        try:
            self.vs.release()  # release web camera
        except:
            print()
        
        cv2.destroyAllWindows()  # it is not mandatory in this application


# start the app

pba = Application(os.getcwd() + '\\group_images\\')
pba.root.mainloop()



