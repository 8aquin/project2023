# import os
# import cv2
# import time
# import pandas as pd
# import datetime
# import tkinter as tk


# ###for choose subject and fill attendance
# def FillAttendances():
#     sub = tx.get()
#     now = time.time()  ###For calculate seconds of video
#     future = now + 20
#     if time.time() < future:
#         if sub != '':
#             recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
#             try:
#                 recognizer.read("TrainingImageLabel\Trainner.yml")
#             except:
#                 e = 'Model not found,Please train model'
#                 Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
#                 Notifica.place(x=20, y=250)

#             harcascadePath = "haarcascade_frontalface_default.xml"
#             faceCascade = cv2.CascadeClassifier(harcascadePath)
#             df = pd.read_csv("StudentDetails\StudentDetails.csv")
#             cam = cv2.VideoCapture(0)
#             font = cv2.FONT_HERSHEY_SIMPLEX
#             col_names = ['Enrollment', 'Name', 'Date', 'Time' ]
#             attendance = pd.DataFrame(columns=col_names)
#             global Subject
#             Subject = tx.get()
#             print(Subject,'IIIIIIIIIIIIIIIIIIIIIII')
#             while True:
#                 ret, im = cam.read()
#                 gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#                 faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                
#                 for (x, y, w, h) in faces:
#                     global Id

#                     Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
#                     if (conf <70):
#                         print(conf)
                        
#                         global aa
#                         global date
#                         global timeStamp
#                         Subject = tx.get()
#                         ts = time.time()
#                         date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#                         timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#                         aa = df.loc[df['Enrollment'] == Id]['Name'].values
#                         global tt
#                         tt = str(Id) + "-" + aa
#                         En = '15624031' + str(Id)
#                         attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
#                         cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
#                         cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

#                     else:
                        
#                         Subject = tx.get()
#                         Id = 'Unknown'
#                         tt = str(Id)
#                         cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
#                         cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
#                 if time.time() > future:
#                     break

#                 attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
#                 cv2.imshow('Filling attedance..', im)
#                 key = cv2.waitKey(30) & 0xff
#                 if key == 27:
#                     break

#             ts = time.time()
#             date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#             timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#             Hour, Minute, Second = timeStamp.split(":")
#             fileName = "Attendance/" + Subject +'_' + date +".csv"
#             # fileName = "Attendance/attendance.csv" 
#             if os.path.isfile(fileName):
#                 existing_data = pd.read_csv(fileName)
#                 attendance = pd.concat([existing_data, attendance], ignore_index=True)
#             else:
#                 attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
#             attendance.to_csv(fileName, index=False)



#             ##Create table for Attendance
#             date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
#             attendance = str( Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)

#             import mysql.connector

#             # Connect to the database
#             conn = mysql.connector.connect(
#                 host='localhost',
#                 user='root',
#                 password='',
#                 database='frams'
#             )
#             cursor = conn.cursor()

#             # Define the table name
#             attendance = 'attendance'

#             # Now enter attendance in the database
#             insert_data_query = "INSERT INTO {} (ENROLLMENT,NAME , DATE, TIME) VALUES (%s, %s, %s, %s)".format(attendance)
#             values = (str(aa), str(), str(date), str(timeStamp))

#             try:
#                 cursor.execute(insert_data_query, values)  # Insert the attendance data into the table
#                 conn.commit()  # Commit the changes to the database
#             except mysql.connector.Error as e:
#                 conn.rollback()  # Rollback the transaction in case of error
#                 print("Error inserting data into MySQL database:", e)

#             # Close the database connection
#             cursor.close()
#             conn.close()


#             M = 'Attendance filled Successfully'
#             Notifica.configure(text=M, bg="Green", fg="white", width=33, font=('times', 15, 'bold'))
#             Notifica.place(x=20, y=250)

#             cam.release()
#             cv2.destroyAllWindows()

#             import csv
#             import tkinter
#             root = tk.Tk()
#             root.title("Attendance of " + Subject)
#             root.configure(background='snow')
#             cs = 'C:/Users/krgan/Desktop/project2023/' + fileName
#             with open(cs, newline="") as file:
#                 reader = csv.reader(file)
#                 r = 0
#                 for col in reader:
#                     c = 0
#                     for row in col:
#                         # I've added some styling
#                         label = tk.Label(root, width=20, height=2, fg="black", font=('times', 15, 'bold'),
#                                          bg="#76c2b5", text=row, relief=tkinter.RIDGE)
#                         label.grid(row=r, column=c)
#                         c += 1
#                     r += 1
#             root.mainloop()

# ###windo is frame for subject chooser

# # windo = tk.Tk()
# # windo.iconbitmap('fd.ico')
# # windo.title("Enter subject name...")
# # windo.geometry('750x550')
# # windo.configure(background='#1c6e8c')
# # Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
# #                         height=2, font=('times', 15, 'bold'))
# # Notifica.place(x=175,y=400)
# # message = tk.Label(windo,text="Attendance", fg="white",bg="#1c6e8c"
# #                    ,width=30, height=3, font=('times',30,'italic bold'))
# # message.place(x=10, y=10)

# def Attf():
#     import subprocess
#     subprocess.Popen(r'explorer /select,"C:\Users\krgan\Desktop\project2023\Attendance\attendance.csv"')

# # attf = tk.Button(windo,  text="Student File",command=Attf,fg="black"  ,bg="#76c2b5"  ,width=12  ,height=1 ,activebackground = "Red" ,font=('times', 14, ' bold '))
# # attf.place(x=450, y=300)
# #
# # sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="black", bg="sky blue", font=('times', 15, ' bold '))
# # sub.place(x=70, y=200)
# #
# # tx = tk.Entry(windo, width=20, bg="snow", fg="black", font=('times', 23, ' bold '))
# # tx.place(x=300, y=205)
# #
# # fill_a = tk.Button(windo, text="Attendance", fg="black",command=FillAttendances, bg="#76c2b5", width=20, height=1,
# #                     activebackground="Red", font=('times', 15, ' bold '))
# # fill_a.place(x=150, y=300)
# #
# # logoutButton = tk.Button(windo, text="Logout",  fg="black", bg="#E1455F", width=10, height=1,
# #                                         activebackground="#fb6944", font=('times', 15, ' bold '))
# # logoutButton.place(x=50, y=20)
# # windo.mainloop()
