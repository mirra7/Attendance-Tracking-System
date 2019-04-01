# Attendance-Tracking-System
Attendance Tracking System using Computer Vision



- Capstone				// Main Project Folder
+---Attendance_Tracker                            // Folder containing subject-vise attendance sheets
|       Attendance_Machine_Learning.csv
|       Attendance_Python.csv
|       
+---group_images       			// Folder that contains the images clicked by faculty
+---Haarcascades			// Folder containing Haar Cascades xml files
|       haarcascade_frontalface_default.xml    
+---history				// Folder containing history of images clicked by faculty
|       2019-03-20_12-16-05.jpg
|       2019-03-20_12-16-10.jpg       
+---models				// Folder containing the facial landmarks of face
|       landmarks.dat      
+---test_images			// Temporary Folder to keep faces extracted from group image       
+---train_images			// Folder to keep labelled training images of students
|       User.01.1.jpg
|       User.01.10.jpg
|       
+---weights				// Folder containing weights of pre-trained model
|       nn4.small2.v1.h5



Download the models folder from the link given below and place it in the same directory as above. Run the cap_login python file.

-- https://drive.google.com/open?id=13-fgfmL7cfE3gU7uXTQFpCcwdGmLZM45
