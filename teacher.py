import tkinter as tk
import mysql.connector
import getcsv
import time
teacher_win = None
import pandas as pd
import datetime
import os
import cv2


def FillAttendances():
    global Subject
    global aa

    aa = ''

    Subject = tx.get()

    sub = tx.get()
    now = time.time()  ###For calculate seconds of video
    future = now + 20
    if time.time() < future:
        if sub != '':
            recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
            try:
                recognizer.read("TrainingImageLabel\Trainner.yml")
            except:
                e = 'Model not found,Please train model'
                Notifica = tk.Label(text=e, bg="red",fg="black", width=33, font=('times', 15, 'bold'))
                Notifica.place(x=20, y=250)

            harcascadePath = "haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(harcascadePath)
            df = pd.read_csv("StudentDetails\StudentDetails.csv")
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ['Enrollment', 'Name', 'Date', 'Time']
            attendance = pd.DataFrame(columns=col_names)
            while True:
                ret, im = cam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    global Id

                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if (conf < 70):
                        print(conf)
                        global date
                        global timeStamp
                        Subject = tx.get()
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        aa = df.loc[df['Enrollment'] == Id]['Name'].values
                        global tt
                        tt = str(Id) + "-" + aa
                        En = '15624031' + str(Id)
                        attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                    else:
                        Id = 'Unknown'
                        Id = 'Unknown'
                        tt = str(Id)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                if time.time() > future:
                    break

                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                cv2.imshow('Filling attedance..', im)
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    break

            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance/" + Subject + '_' + date + ".csv"
            # fileName = "Attendance/attendance.csv"
            if os.path.isfile(fileName):
                existing_data = pd.read_csv(fileName)
                attendance = pd.concat([existing_data, attendance], ignore_index=True)
            else:
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
            attendance.to_csv(fileName, index=False)

            ##Create table for Attendance
            date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
            attendance = str(Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)

            import mysql.connector

            # Connect to the database
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='frams'
            )
            cursor = conn.cursor()

            # Define the table name
            attendance = 'attendance'

            # Now enter attendance in the database
            insert_data_query = "INSERT INTO {} (ENROLLMENT,NAME , DATE, TIME) VALUES (%s, %s, %s, %s)".format(
                attendance)
            values = (str(aa), str(), str(date), str(timeStamp))

            try:
                cursor.execute(insert_data_query, values)  # Insert the attendance data into the table
                conn.commit()  # Commit the changes to the database
            except mysql.connector.Error as e:
                conn.rollback()  # Rollback the transaction in case of error
                print("Error inserting data into MySQL database:", e)

            # Close the database connection
            cursor.close()
            conn.close()

            # M = 'Attendance filled Successfully'
            # Notifica = tk.Label(teacher_window, text="Attendence filled Succesfully", bg="Green", fg="white", width=33,
            #                     height=2, font=('times', 15, 'bold'))
            # Notifica.place(x=175, y=400)

            cam.release()
            cv2.destroyAllWindows()

            import csv
            root = tk.Tk()
            root.title("Attendance of " + Subject)
            root.configure(background='snow')
            cs = fileName
            with open(cs, newline="") as file:
                reader = csv.reader(file)
                r = 0
                for col in reader:
                    c = 0
                    for row in col:
                        # I've added some styling
                        label = tk.Label(root, width=20, height=2, fg="black", font=('times', 15, 'bold'),
                                         bg="#76c2b5", text=row, relief=tk.RIDGE)
                        label.grid(row=r, column=c)
                        c += 1
                    r += 1
            root.mainloop()


def teacher_window():
    global teacher_win
    if teacher_win is None:
        teacher_win = tk.Toplevel()
        teacher_win.geometry("1280x720")
        teacher_win.title("Teacher Registration Page and Login")
        teacher_win.configure(background='#1c6e8c')
        teacher_win.protocol("WM_DELETE_WINDOW", on_teacher_window_close)

        # Registration GUI elements
        reg_frame = tk.Frame(teacher_win, bg='#1c6e8c')
        reg_frame.pack(pady=20)

        def clear(*entries):
            for entry in entries:
                entry.delete(0, tk.END)

        name_label = tk.Label(reg_frame, text="Name:",width=20, height=1, fg="black", bg="#76c2b5", font=('times', 15, ' bold '))
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = tk.Entry(reg_frame, width=40, font=('times', 15))
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        subject_label = tk.Label(reg_frame, text="Subject:",width=20, height=1, fg="black", bg="#76c2b5", font=('times', 15, ' bold '))
        subject_label.grid(row=1, column=0, padx=5, pady=5)

        subject_entry = tk.Entry(reg_frame, width=40, font=('times', 15))
        subject_entry.grid(row=1, column=1, padx=5, pady=5)

        email_label_reg = tk.Label(reg_frame, text="Email:",width=20, height=1, fg="black", bg="#76c2b5", font=('times', 15, ' bold '))
        email_label_reg.grid(row=2, column=0, padx=5, pady=5)

        email_entry_reg = tk.Entry(reg_frame, width=40, font=('times', 15))
        email_entry_reg.grid(row=2, column=1, padx=5, pady=5)

        password_label_reg = tk.Label(reg_frame, text="Password:", width=20, height=1,fg="black", bg="#76c2b5", font=('times', 15, ' bold '))
        password_label_reg.grid(row=3, column=0, padx=5, pady=5)

        password_entry_reg = tk.Entry(reg_frame, show="*", width=40, font=('times', 15))
        password_entry_reg.grid(row=3, column=1, padx=5, pady=5)

        clear_button = tk.Button(reg_frame, text="Clear", command=lambda: clear(name_entry, subject_entry, email_entry_reg, password_entry_reg,email_entry_log , password_entry_log ),
                                  fg="black", bg="#76c2b5", width=5,height=1, activebackground="#b2e8e2", font=('times', 15, ' bold '))
        clear_button.grid(row=0, column=3, pady=10)

        def register_teacher():
            # Retrieve user input
            name = name_entry.get()
            subject = subject_entry.get()
            email = email_entry_reg.get()
            password = password_entry_reg.get()

            # Check if all fields are filled
            if not name or not subject or not email or not password:
                error_label_reg = tk.Label(reg_frame, text="Please fill all fields", fg="red", font=('times', 12))
                error_label_reg.grid(row=4, columnspan=2, pady=20)
                return

            # Connect to database
            conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='frams'
            )

            cursor = conn.cursor()

            # Insert new teacher into database
            query = "INSERT INTO teachers (t_name, t_subject, t_email, t_password) VALUES (%s, %s, %s, %s)"
            values = (name,subject, email, password)
            cursor.execute(query, values)
            conn.commit()


            # Commit changes and close database connection
            conn.commit()
            conn.close()

            # Show success message
            success_label_reg = tk.Label(reg_frame, text="Registration successful!", fg="green", font=('times', 12))
            success_label_reg.grid(row=4, columnspan=2, pady=20)

        
        success_label_reg = tk.Label(reg_frame, fg="green",bg='#1c6e8c', font=('times', 12))
        success_label_reg.grid(row=4, column=0, padx=5, pady=5)

        register_btn = tk.Button(reg_frame, text="Register", fg="black", bg="#76c2b5", width=20,
                                height=2, activebackground="#b2e8e2", font=('times', 15, ' bold '),
                                command=register_teacher)
        register_btn.grid(row=5, columnspan=2, padx=5, pady=5)

        # Login GUI elements
        log_frame = tk.Frame(teacher_win, bg='#1c6e8c')
        log_frame.pack(pady=20)

        email_label_log = tk.Label(log_frame, text="Email:", width=20, height=1, bg="#76c2b5", fg="black", font=('times', 15, ' bold '))
        email_label_log.grid(row=0, column=0, padx=5, pady=5)

        email_entry_log = tk.Entry(log_frame, width=40, font=('times', 15))
        email_entry_log.grid(row=0, column=1, padx=5, pady=5)

        password_label_log = tk.Label(log_frame, text="Password:", width=20, height=1, bg="#76c2b5", fg="black", font=('times', 15, ' bold '))
        password_label_log.grid(row=1, column=0, padx=5, pady=5)

        password_entry_log = tk.Entry(log_frame, show="*", width=40, font=('times', 15))
        password_entry_log.grid(row=1, column=1, padx=5, pady=5)
        

        def login_teacher():
            # Retrieve user input
            email = email_entry_log.get()
            password = password_entry_log.get()

            # Check if all fields are filled
            if not email or not password:
                error_label_log = tk.Label(log_frame, text="Please fill in all fields.", fg="red", font=('times', 12))
                error_label_log.grid(row=2, columnspan=2, pady=20)
                return

            # Connect to database
            conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='frams'
            )
            cursor = conn.cursor()


            # Check if teacher exists in database
            query = "SELECT * FROM teachers WHERE t_email = %s AND t_password = %s"
            values = (email, password)
            cursor.execute(query, values)
            teacher = cursor.fetchone()
            if teacher:
                # Show success message, close database connection, and open new window
                success_label_log.config(text="Login successful!", fg="green")
                conn.close()

                # Create new window for teacher to interact with
                teacher_window = tk.Tk()
                teacher_window.title("Teacher Page")
                teacher_window.geometry("960x640")
                teacher_window.configure(background='#1c6e8c')
                # Add widgets and functionality to the new window

                message = tk.Label(teacher_window, text="Attendance", fg="black",bg = "#1c6e8c", width=40,
                   height=3, font=('times', 30, 'italic bold '))
                message.place(x=40,y=20)

                global tx
                tx = tk.Entry(teacher_window, width=20, bg="snow", fg="black", font=('times', 23, ' bold '))
                tx.place(x=300, y=205)

                sub = tk.Label(teacher_window, text="Enter Subject", width=15, height=2, fg="black", bg="sky blue", font=('times', 15, ' bold '))
                sub.place(x=70, y=200)

                # Add Attendance Button
                attendance_button = tk.Button(teacher_window, text="Attendance", command=FillAttendances, fg="black", bg="#76c2b5", width=10, height=1,
                                        activebackground="#b2e8e2", font=('times', 15, ' bold '))
                attendance_button.place(x=250, y=350)

                # Add Student File Button
                student_file_button = tk.Button(teacher_window, text="Student File", command=getcsv.display_student_details, fg="black", bg="#76c2b5", width=10, height=1,
                                        activebackground="#b2e8e2", font=('times', 15, ' bold '))
                student_file_button.place(x=600, y=350)

                # Add Logout Button
                logoutButton = tk.Button(teacher_window, text="Logout", command=teacher_window.destroy, fg="black", bg="#E1455F", width=10, height=1,
                                        activebackground="#fb6944", font=('times', 15, ' bold '))
                logoutButton.place(x=50, y=20)

                # Start the GUI event loop
                teacher_window.mainloop()

            else:
                # Show error message and close database connection
                success_label_log.config(text="Incorrect email or password.", fg="red")
                conn.close()
                
        success_label_log = tk.Label(log_frame, fg="green",bg='#1c6e8c', font=('times', 6))
        success_label_log.grid(row=2, columnspan=2, pady=20)

        login_button = tk.Button(log_frame, text="Login", fg="black", bg="#76c2b5", width=20,
                             height=2,activebackground="#b2e8e2", command=login_teacher, font=('times', 15, ' bold '))
        login_button.grid(row=3, column=0, columnspan=2)

def on_teacher_window_close():
    global teacher_win
    teacher_win.destroy()
    teacher_win = None