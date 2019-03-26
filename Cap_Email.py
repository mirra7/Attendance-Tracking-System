# Importing all required libraries
try:
    import sys
    import smtplib 
    from email.mime.multipart import MIMEMultipart 
    from email.mime.text import MIMEText 
    from email.mime.base import MIMEBase 
    from email import encoders 
    from datetime import datetime 
except:
    print("Error in importing libraries. Kindly check whether libraries are properly installed!")
    sys.exit()
try:
    
    fromaddr = "attendance.praxis@gmail.com"
    toaddr = sys.argv[3]
    ccaddr = sys.argv[4]


    sub = sys.argv[1] # reading the email  address from user
    fac = sys.argv[2] # reading the email address from the user
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address   
    msg['From'] = fromaddr 

    # storing the receivers email address  
    msg['To'] = toaddr 

    # storing the subject  
    msg['Subject'] = str(fac) + " " + str(sub)

    # string to store the body of the mail 
    body = "PFA attendance for " + str(sub) + " taken by " + str(fac)

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # Get the current date
    dte = str(datetime.now().strftime("%d-%m-%Y"))


    # open the file to be sent  
    filename = "Attendance" + "_" + str(sub) + ".xlsx"
    attachment = open("C:\\Users\\Mirra\\Desktop\\Capstone\\Attendance_Tracker\\Attendance"+ "_" +str(sub) + ".csv", "rb") 

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 

    # encode into base64 
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(fromaddr, password = 'praxis@att') 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 

    # sending the mail 
    s.sendmail(fromaddr, [toaddr, ccaddr], text) 

    # terminating the session 
    s.quit() 
except:
    print("An error occured while sending the mail.")
