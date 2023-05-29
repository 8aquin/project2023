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
import teacher
import mysql.connector
import pandas as pd
# import pymysql.connections

# create main window
win = tk.Tk()
win.iconbitmap('fd.ico')
win.title("Admin Login")
win.geometry('860x430')
win.configure(background='#D3D3D3')

def del_sc():
    sc.destroy()
def err_screen():
    global sc
    sc = tk.Tk()
    sc.geometry('300x100')
    sc.iconbitmap('fd.ico')
    sc.title('Warning!!')
    sc.configure(background='#D3D3D3')
    tk.Label(sc,text='Enrollment & Name required!!!',fg='#fb6944', bg="#76c2b5",font=('times', 14, ' bold ')).pack()
    tk.Button(sc,text='OK',command=del_sc,fg="black", bg="#76c2b5", activebackground="#b2e8e2",width=9,height=1, font=('times', 15, ' bold ')).place(x=90,y=50)


def homepage():
    global txt, txt2
    window = tk.Tk()
    window.geometry('1280x720')
    window.configure(background='#1c6e8c')
    window.title('Main-proj-2023')

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.iconbitmap('fd.ico')

    message = tk.Label(window, text="Student Enrollment", bg="#1c6e8c",fg="black", width=50,
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
                    elif sampleNum > 500:
                        break
                cam.release()
                cv2.destroyAllWindows()
                ts = time.time()
                Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                # establish database connection
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="frams"
                )

                # get cursor
                mycursor = mydb.cursor()

                # insert values into student table
                sql = "INSERT INTO student (s_name, s_enroll) VALUES (%s, %s)"
                val = (Name, Enrollment)
                mycursor.execute(sql, val)
                mydb.commit()

                # Get the ID of the newly inserted row
                inserted_id = mycursor.lastrowid
                row = [inserted_id,Enrollment, Name, Date, Time]

                df = pd.read_csv('StudentDetails\StudentDetails.csv')
                columns = df.columns

                newdf = pd.DataFrame([row], columns = columns)

                df = pd.concat([df, newdf])

                df.to_csv('StudentDetails\StudentDetails.csv',  index = False)

                Notification = tk.Label(window, text="", bg="#4fa234", width=50, font=('times', 18, 'bold'))
                Notification.place(x=290, y=400)

                # with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                #     writer = csv.writer(csvFile, delimiter=',')
                #     writer.writerow(row)
                #     csvFile.close()
                res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
                Notification.configure(text=res, bg="#4fa234", width=50, font=('times', 18, 'bold'))
                Notification.place(x=250, y=400)
            except FileExistsError as F:
                f = 'Student Data already exists'
                Notification.configure(text=f, bg="#fb6944", width=21)
                Notification.place(x=450, y=400)




    #Training model
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

    def trainimg():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        global detector
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        global faces,Id



        faces, Id = getImagesAndLabels("TrainingImage")
        Id = np.array(Id, dtype=np.int32)
        recognizer.train(faces, Id)
        recognizer.save('TrainingImageLabel/trainner.yml')
        Notification = tk.Label(window, text="", bg="#4fa234", width=50, font=('times', 18, 'bold'))
        Notification.place(x=290, y=400)

        res = "Model Trained"  
        Notification.configure(text=res, bg="#4fa234", width=50, font=('times', 18, 'bold'))

    def clear():
        txt.delete(first=0, last=22)

    def clear1():
        txt2.delete(first=0, last=22)

    lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="black", bg="#76c2b5", font=('times', 15, ' bold '))
    lbl.place(x=200, y=200)

    lbl2 = tk.Label(window, text="Enter Name", width=20, fg="black",  bg="#76c2b5", height=2, font=('times', 15, ' bold '))
    lbl2.place(x=200, y=300)

    def testVal(inStr,acttyp):
        if acttyp == '1': #insert
            if not inStr.isdigit():
                return False
        return True

    txt = tk.Entry(window, validate="key", width=20, bg="white", fg="black", font=('times', 25, ' bold '))
    txt['validatecommand'] = (txt.register(testVal),'%P','%d')
    txt.place(x=550, y=210)

    txt2 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 25, ' bold '))
    txt2.place(x=550, y=310)

    clearButton = tk.Button(window, text="Clear",command=clear,fg="black"  ,bg="#76c2b5", activebackground="#b2e8e2",width=10  ,height=1 ,font=('times', 15, ' bold '))
    clearButton.place(x=950, y=210)

    clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="black"  ,bg="#76c2b5", activebackground="#b2e8e2",width=10 ,height=1, font=('times', 15, ' bold '))
    clearButton1.place(x=950, y=310)

    takeImg = tk.Button(window, text="Take Images",command=take_img,fg="black"  ,bg="#76c2b5", activebackground="#b2e8e2",width=20  ,height=2,font=('times', 15, ' bold '))
    takeImg.place(x=350, y=500)

    trainImg = tk.Button(window, text="Train Images",fg="black",command=trainimg ,bg="#76c2b5", activebackground="#b2e8e2",width=20  ,height=2,font=('times', 15, ' bold '))
    trainImg.place(x=650, y=500)

    logoutButton = tk.Button(window, text="Logout", command=window.destroy, fg="black", bg="#E1455F", width=10, height=1,
                             activebackground="#fb6944", font=('times', 15, ' bold '))
    logoutButton.place(x=950, y=20)


def show_homepage():
    username = un_entr.get()
    password = pw_entr.get()

    if username == 'admin':
        if password == 'admin123':
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
Login.place(x=150, y=250)

teacher_button = tk.Button(win, text="Teacher", fg="black", bg="#76c2b5", width=20,
                           height=2, activebackground="#b2e8e2",
                           command=teacher.teacher_window, font=('times', 15, ' bold '))
teacher_button.place(x=550, y=250)

win.mainloop()


