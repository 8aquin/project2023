import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time
import mysql.connector
import re

# create main window
win = tk.Tk()
win.iconbitmap('fd.ico')
win.title("Login")
win.geometry('640x360')
win.configure(background='#D3D3D3')


def homepage():
    global txt, txt2
    window = tk.Tk()
    window.geometry('1280x720')
    window.configure(background='#D3D3D3')
    window.title('Main-proj-2023')
    
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.iconbitmap('fd.ico')

    message = tk.Label(window, text="Student Enrollment", bg="#D3D3D3",fg="black", width=50,
                height=3, font=('times', 30, 'italic bold '))
    message.place(x=80, y=20)

    #taking images for dataset
    def take_img():
        global txt, txt2, Notification
        l1 = txt.get()
        l2 = txt2.get()
        if l1 == '':
            err_screen()
        elif l2 == '':
            err_screen()
        else:
            try:
                cam = cv2.VideoCapture(0)
                detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                Enrollment = txt.get()
                Name = txt2.get()
                sampleNum = 0
                while (True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        # incrementing sample number
                        sampleNum = sampleNum + 1
                        # saving the captu#fb6944 face in the dataset folder
                        cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                    gray[y:y + h, x:x + w])
                        cv2.imshow('Frame', img)
                    # wait for 100 miliseconds
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 100
                    elif sampleNum > 70:
                        break
                cam.release()
                cv2.destroyAllWindows()
                ts = time.time()
                Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                row = [Enrollment, Name, Date, Time]
                with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(row)
                    csvFile.close()
                res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
                Notification.configure(text=res, bg="#4fa234", width=50, font=('times', 18, 'bold'))
                Notification.place(x=250, y=400)
                Notification = tk.Label(window, text="Safely terminating.", bg="Green", fg="white", width=15,
                        height=3, font=('times', 17, 'bold'))
            except FileExistsError as F:
                f = 'Student Data already exists'
                Notification.configure(text=f, bg="#fb6944", width=21)
                Notification.place(x=450, y=400)
                Notification = tk.Label(window, text="Safely terminating.", bg="Green", fg="white", width=15,
                        height=3, font=('times', 17, 'bold'))
    
    #Training model
    def trainimg():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        global detector
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        global faces,Id
        faces, Id = getImagesAndLabels("TrainingImage")

        res = "Model Trained"  
        Notification.configure(text=res, bg="#4fa234", width=50, font=('times', 18, 'bold'))
        Notification.place(x=290, y=400)
        Notification = tk.Label(window, text="Safely terminating.", bg="Green", fg="white", width=15,
            height=3, font=('times', 17, 'bold'))
        
    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        Ids = []
        # Loop through all the image paths and load the Ids and images
        for imagePath in imagePaths:
            # Load the image and convert it to grayscale
            pilImage = Image.open(imagePath).convert('L')
            # Convert the PIL image into a numpy array
            imageNp = np.array(pilImage, dtype=np.uint8)
            # Get the Id from the image filename
            Id = os.path.split(imagePath)[-1].split(".")[1]
            # Extract the face from the training image sample
            faces = detector.detectMultiScale(imageNp)
            # If a face is detected, append it to the list of face samples along with its Id
            for (x, y, w, h) in faces:
                faceSamples.append(imageNp[y:y + h, x:x + w])
                Ids.append(Id)
        return faceSamples, Ids
    def clear():
        txt.delete(first=0, last=22)

    def clear1():
        txt2.delete(first=0, last=22)

    lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="white", bg="#00539C", font=('times', 15, ' bold '))
    lbl.place(x=200, y=200)

    lbl2 = tk.Label(window, text="Enter Name", width=20, fg="white", bg="#00539C", height=2, font=('times', 15, ' bold '))
    lbl2.place(x=200, y=300)

    clearButton = tk.Button(window, text="Clear",command=clear,fg="black"  ,bg="#E1455F"  ,width=10  ,height=1 ,activebackground = "#fb6944" ,font=('times', 15, ' bold '))
    clearButton.place(x=950, y=210)

    clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="black"  ,bg="#E1455F"  ,width=10 ,height=1, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
    clearButton1.place(x=950, y=310)

    takeImg = tk.Button(window, text="Take Images",command=take_img,fg="black"  ,bg="#C62D42"  ,width=20  ,height=2, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
    takeImg.place(x=125, y=500)

    trainImg = tk.Button(window, text="Train Images",fg="black",command=trainimg ,bg="#C62D42"  ,width=20  ,height=2, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
    trainImg.place(x=425, y=500)

    quitWindow = tk.Button(window, text="Manually Fill Attendance" ,fg="black"  ,bg="#C62D42"  ,width=20  ,height=2, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
    quitWindow.place(x=725, y=500)
    
    # Create registry button
    AP = tk.Button(window, text="Display CSV", command=manually_fill, fg="black", bg="#C62D42", width=20, height=2, activebackground="#fb6944", font=('times', 15, 'bold'))
    AP.place(x=1000, y=500)


    ####GUI for manually fill attendance

    def manually_fill():
        global sb
        sb = tk.Tk()
        sb.iconbitmap('AMS.ico')
        sb.title("Enter subject name...")
        sb.geometry('580x320')
        sb.configure(background='snow')

        def err_screen_for_subject():
            print('Check')
            
        def fill_attendance():
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            ####Creatting csv of attendance

            ##Create table for Attendance
            date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
            global subb
            subb=SUB_ENTRY.get()
            DB_table_name = str(subb + "_" + Date + "_Time_" + Hour + "_" + Minute + "_" + Second)

            import pymysql.connections

            ###Connect to the database
            try:
                global cursor
                connection = pymysql.connect(host='localhost', user='root', password='', db='manually_fill_attendance')
                cursor = connection.cursor()
            except Exception as e:
                print(e)

            sql = "CREATE TABLE " + DB_table_name + """
                            (ID INT NOT NULL AUTO_INCREMENT,
                            ENROLLMENT varchar(100) NOT NULL,
                            NAME VARCHAR(50) NOT NULL,
                            DATE VARCHAR(20) NOT NULL,
                            TIME VARCHAR(20) NOT NULL,
                                PRIMARY KEY (ID)
                                );
                            """


            try:
                cursor.execute(sql)  ##for create a table
            except Exception as ex:
                print(ex)  #

            if subb=='':
                err_screen_for_subject()
            else:
                sb.destroy()
                MFW = tk.Tk()
                MFW.iconbitmap('AMS.ico')
                MFW.title("Manually attendance of "+ str(subb))
                MFW.geometry('880x470')
                MFW.configure(background='snow')

                def del_errsc2():
                    print('Check again')

                def testVal(inStr, acttyp):
                    if acttyp == '1':  # insert
                        if not inStr.isdigit():
                            return False
                    return True

                ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="white", bg="blue2",
                            font=('times', 15, ' bold '))
                ENR.place(x=30, y=100)

                STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="white", bg="blue2",
                                    font=('times', 15, ' bold '))
                STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20,validate='key', bg="yellow", fg="red", font=('times', 23, ' bold '))
            ENR_ENTRY['validatecommand'] = (ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

                ####get important variable
                def enter_data_DB():
                    ENROLLMENT = ENR_ENTRY.get()
                    STUDENT = STUDENT_ENTRY.get()
                    
                    time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + DB_table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLLMENT), str(STUDENT), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

                def create_csv():
                    import csv
                    cursor.execute("select * from " + DB_table_name + ";")
                    csv_name='E:/projs/face-detect/project2023/Attendance/'+DB_table_name+'.csv'
                    with open(csv_name, "w") as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([i[0] for i in cursor.description])  # write headers
                        csv_writer.writerows(cursor)
                        O="CSV created Successfully"
                        Notifi.configure(text=O, bg="Green", fg="white", width=33, font=('times', 19, 'bold'))
                        Notifi.place(x=180, y=380)
                    import csv
                    import tkinter
                    root = tkinter.Tk()
                    root.title("Attendance of " + subb)
                    root.configure(background='snow')
                    with open(csv_name, newline="") as file:
                        reader = csv.reader(file)
                        r = 0

                        for col in reader:
                            c = 0
                            for row in col:
                                # i've added some styling
                                label = tkinter.Label(root, width=13, height=1, fg="black", font=('times', 13, ' bold '),
                                                    bg="lawn green", text=row, relief=tkinter.RIDGE)
                                label.grid(row=r, column=c)
                                c += 1
                            r += 1
                    root.mainloop()

                Notifi = tk.Label(MFW, text="CSV created Successfully", bg="Green", fg="white", width=33,
                                    height=2, font=('times', 19, 'bold'))


                c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="black", bg="deep pink", width=10,
                                        height=1,
                                        activebackground="Red", font=('times', 15, ' bold '))
                c1ear_enroll.place(x=690, y=100)

                c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="black", bg="deep pink", width=10,
                                        height=1,
                                        activebackground="Red", font=('times', 15, ' bold '))
                c1ear_student.place(x=690, y=200)

                DATA_SUB = tk.Button(MFW, text="Enter Data",command=enter_data_DB, fg="black", bg="lime green", width=20,
                                    height=2,
                                    activebackground="Red", font=('times', 15, ' bold '))
                DATA_SUB.place(x=170, y=300)

                MAKE_CSV = tk.Button(MFW, text="Convert to CSV",command=create_csv, fg="black", bg="red", width=20,
                                    height=2,
                                    activebackground="Red", font=('times', 15, ' bold '))
                MAKE_CSV.place(x=570, y=300)

                def attf():
                    import subprocess
                    subprocess.Popen(r'explorer /select,"E:/projs/face-detect/project2023/Attendance/-------Check atttendance-------"')

                attf = tk.Button(MFW,  text="Check Sheets",command=attf,fg="black"  ,bg="lawn green"  ,width=12  ,height=1 ,activebackground = "Red" ,font=('times', 14, ' bold '))
                attf.place(x=730, y=410)

                MFW.mainloop()


        SUB = tk.Label(sb, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
        SUB.place(x=30, y=100)

        global SUB_ENTRY

        SUB_ENTRY = tk.Entry(sb, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
        SUB_ENTRY.place(x=250, y=105)

        fill_manual_attendance = tk.Button(sb, text="Fill Attendance",command=fill_attendance, fg="white", bg="deep pink", width=20, height=2,
                        activebackground="Red", font=('times', 15, ' bold '))
        fill_manual_attendance.place(x=250, y=160)
        sb.mainloop()

    window.mainloop()


def show_homepage():
    username = un_entr.get()
    password = pw_entr.get()

    if username == 'admin':
        if password == 'admin123':
            win.destroy()
            homepage()
        else:
            Nt.configure(text='Incorrect Password')
            Nt.place(x=290, y=200)
    else:
        if password == 'admin123':
            Nt.configure(text='Incorrect Username')
            Nt.place(x=290, y=100)
        else:
            Nt.configure(text='Incorrect Username and Password')
            Nt.place(x=290, y=200)


Nt = tk.Label(win,bg="#D3D3D3",fg="#e74c3c", font=('times', 9, 'bold'))

un = tk.Label(win, text="Enter username", width=15, height=2, fg="white", bg="#00539C",
                font=('times', 15, ' bold '))
un.place(x=30, y=50)

pw = tk.Label(win, text="Enter password", width=15, height=2, fg="white", bg="#00539C",
                font=('times', 15, ' bold '))
pw.place(x=30, y=150)


def c00():
    un_entr.delete(first=0, last=22)

un_entr = tk.Entry(win, width=20, bg="#fdfac0", fg="black", font=('times', 23, ' bold '))
un_entr.place(x=290, y=55)

def c11():
    pw_entr.delete(first=0, last=22)

pw_entr = tk.Entry(win, width=20,show="*", bg="#fdfac0", fg="black", font=('times', 23, ' bold '))
pw_entr.place(x=290, y=155)

c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="#E1455F", width=10, height=1,
                        activebackground="#fb6944", font=('times', 15, ' bold '))
c0.place(x=690, y=55)

c1 = tk.Button(win, text="Clear", command=c11, fg="black", bg="#E1455F", width=10, height=1,
                activebackground="#fb6944", font=('times', 15, ' bold '))
c1.place(x=690, y=155)

Login = tk.Button(win, text="Login", fg="black", bg="#76c2b5", width=20,
                    height=2,
                    activebackground="#b2e8e2",command=show_homepage, font=('times', 15, ' bold '))
Login.place(x=300, y=250)
win.mainloop()

def del_sc():
    sc.destroy()
def err_screen():
    global sc
    sc = tk.Tk()
    sc.geometry('300x100')
    sc.iconbitmap('fd.ico')
    sc.title('Warning!!')
    sc.configure(background='#D3D3D3')
    tk.Label(sc,text='Enrollment & Name required!!!',fg='#fb6944',bg='white',font=('times', 14, ' bold ')).pack()
    tk.Button(sc,text='OK',command=del_sc,fg="black",bg="#76c2b5",width=9,height=1, activebackground="#b2e8e2",font=('times', 15, ' bold ')).place(x=90,y=50)
