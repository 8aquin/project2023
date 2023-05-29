import tkinter as tk
import pandas as pd

def display_student_details():
    # Read the student details from the CSV file
    df = pd.read_csv('StudentDetails/StudentDetails.csv')

    # Create a Tkinter window
    window = tk.Tk()

    # Create a text widget to display the student details
    text_widget = tk.Text(window)
    text_widget.pack()

    # Insert the student details into the text widget
    text_widget.insert(tk.END, df.to_string())

    # Disable text widget editing
    text_widget.configure(state='disabled')

    # Run the Tkinter event loop
    window.mainloop()


