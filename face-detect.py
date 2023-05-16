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
import re

#Mainframe

window = tk.Tk()
window.geometry('1280x720')
window.configure(background='#D3D3D3')
window.title('Main-proj-2023')

import mysql.connector
def create_database():
    # Connect to the XAMPP MySQL database
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='student')

    # Create a new table called "enrollments" with two columns: "s_id" and "name"
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE enrollments
                     (s_id INTEGER PRIMARY KEY, name TEXT);''')

    # Insert some sample data into the table
    enrollments = [(1, 'John'), (2, 'Jane'), (3, 'Bob')]
    cursor.executemany('INSERT INTO enrollments VALUES (%d, %s)', enrollments)

    # Commit the changes to the database
    conn.commit()

    # Export the data in the "enrollments" table to a CSV file
    with open('StudentDetails.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['s_id', 'name'])
        cursor.execute('SELECT * FROM enrollments')
        for row in cursor:
            writer.writerow(row)

    # Close the database connection
    cursor.close()
    conn.close()


def admin_panel():
    win = tk.Tk()
    win.iconbitmap('fd.ico')
    win.title("Login")
    win.geometry('880x420')
    win.configure(background='#D3D3D3')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'admin':
            if password == 'admin123':
                win.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='#D3D3D3')

                cs = 'E:/projs/face-detect/project2023/StudentDetails/StudentDetails.csv'
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    label = tkinter.Label(root, width=20, height=2, fg="black", font=('times', 15, ' bold '),
                                        bg="lawn green", text='Enrollment Number', relief=tkinter.RIDGE)
                    label.grid(row=r, column=0)
                    label = tkinter.Label(root, width=20, height=2, fg="black", font=('times', 15, ' bold '),
                                        bg="lawn green", text='Name', relief=tkinter.RIDGE)
                    label.grid(row=r, column=1)
                    r += 1

                    for col in reader:
                        c = 0
                        for row in col[0:2]:  
                            label = tkinter.Label(root, width=20, height=1, fg="black", font=('times', 15, ' bold '),
                                                bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
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
                       activebackground="#b2e8e2",command=log_in, font=('times', 15, ' bold '))
    Login.place(x=300, y=250)
    win.mainloop()

def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)

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
import os
import csv
import time
import datetime
import cv2

#taking images for dataset
def take_img():
    def display_notification(msg, bg_color="#4fa234", width=50, font=('times', 18, 'bold')):
        Notification.configure(text=msg, bg=bg_color, width=width, font=font)
        Notification.place(x=250, y=400)

    def err_screen():
        display_notification("Please fill both the details.", bg_color="#fb6944", width=30)

    def save_student_details(enrollment, name):
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        time_ = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        row = [enrollment, name, date, time_]
        file_path = 'StudentDetails/StudentDetails.csv'
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['Enrollment', 'Name', 'Date', 'Time'])
            writer.writerow(row)


    def save_image(enrollment, name, img, sample_num):
        if not os.path.exists("TrainingImage"):
            os.mkdir("TrainingImage")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            sample_num += 1
            file_path = f"TrainingImage/{name}.{enrollment}.{sample_num}.jpg"
            cv2.imwrite(file_path, gray[y:y + h, x:x + w])
        return sample_num

    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '' or l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                display_notification("Camera not available. Please check if it's connected.")
                return
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            enrollment = txt.get()
            name = txt2.get()
            sample_num = 0
            while True:
                ret, img = cam.read()
                if not ret:
                    continue
                sample_num = save_image(enrollment, name, img, sample_num)
                cv2.imshow('Frame', img)
                if cv2.waitKey(1) & 0xFF == ord('q') or sample_num > 250:
                    break
            cam.release()
            cv2.destroyAllWindows()
            save_student_details(enrollment, name)
            display_notification(f"Images Saved for Enrollment: {enrollment} Name: {name}")
        except FileExistsError as F:
            display_notification("Student Data already exists", bg_color="#fb6944", width=21)

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


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('fd.ico')

def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text="Student Enrollment", bg="#D3D3D3",fg="black", width=50,
                   height=3, font=('times', 30, 'italic bold '))

message.place(x=80, y=20)

Notification = tk.Label(window, text="Safely terminating.", bg="Green", fg="white", width=15,
                      height=3, font=('times', 17, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="white", bg="#00539C", font=('times', 15, ' bold '))
lbl.place(x=200, y=200)

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isalnum() and '-' not in inStr:
            return False
    return True

txt = tk.Entry(window, validate="key", width=20, bg="#fdfac0", fg="black", font=('times', 25, ' bold '))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="white", bg="#00539C", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20, bg="#fdfac0", fg="black", font=('times', 25, ' bold '))
txt2.place(x=550, y=310)

clearButton = tk.Button(window, text="Clear",command=clear,fg="black"  ,bg="#E1455F"  ,width=10  ,height=1 ,activebackground = "#fb6944" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=210)

clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="black"  ,bg="#E1455F"  ,width=10 ,height=1, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
clearButton1.place(x=950, y=310)

takeImg = tk.Button(window, text="Take Images",command=take_img,fg="black"  ,bg="#C62D42"  ,width=20  ,height=2, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
takeImg.place(x=250, y=500)

trainImg = tk.Button(window, text="Train Images",fg="black",command=trainimg ,bg="#C62D42"  ,width=20  ,height=2, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
trainImg.place(x=550, y=500)

AP = tk.Button(window, text="Student Registry",command=admin_panel,fg="black"  ,bg="#C62D42"  ,width=20 ,height=2, activebackground = "#fb6944" ,font=('times', 15, ' bold '))
AP.place(x=850, y=500)

window.mainloop()