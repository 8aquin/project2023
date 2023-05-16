import tkinter as tk
import mysql.connector
import attendance
import getcsv

teacher_win = None

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

                message = tk.Label(teacher_window, text="Welcome", fg="black",bg = "#1c6e8c", width=40,
                   height=3, font=('times', 30, 'italic bold '))
                message.place(x=40,y=20)

                # Add Attendance Button
                attendance_button = tk.Button(teacher_window, text="Attendance", command=attendance.FillAttendances, fg="black", bg="#76c2b5", width=10, height=1,
                                        activebackground="#b2e8e2", font=('times', 15, ' bold '))
                attendance_button.place(x=300, y=350)

                # Add Student File Button
                student_file_button = tk.Button(teacher_window, text="Student File", command=getcsv.view_attendance_csv, fg="black", bg="#76c2b5", width=10, height=1,
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
        login_button.grid(row=3, column=1,padx=5, pady=5)

def on_teacher_window_close():
    global teacher_win
    teacher_win.destroy()
    teacher_win = None