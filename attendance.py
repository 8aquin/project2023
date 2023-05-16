import cv2
import pandas as pd
import datetime
import mysql.connector

def FillAttendances():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    df = pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Enrollment', 'Name', 'Date', 'Time']
    data_types = [str, str, str, str]  # Adjust the data types as per your requirements
    attendance = pd.DataFrame(columns=col_names, dtype=data_types)


    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 70:
                Subject = "SubjectName"
                ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                aa = df.loc[df['Enrollment'] == Id]['Name'].values[0]
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, ts.split()[0], ts.split()[1]]
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
            else:
                Id = 'Unknown'
                tt = str(Id)
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

        cv2.imshow('Filling attendance..', im)
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    

    ts = datetime.datetime.now()
    date = ts.strftime('%Y-%m-%d')
    timeStamp = ts.strftime('%H:%M:%S')
    fileName = f"Attendance/{Subject}_{date}_{timeStamp}.csv"
    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
    attendance.to_csv(fileName, index=False)

    date_for_DB = ts.strftime('%Y_%m_%d')
    DB_Table_name = f"{Subject}_{date_for_DB}_Time_{ts.strftime('%H_%M_%S')}"

    try:
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='Face_reco_fill')
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE {DB_Table_name} (ID INT NOT NULL AUTO_INCREMENT, ENROLLMENT varchar(100) NOT NULL, NAME VARCHAR(50) NOT NULL, DATE VARCHAR(20) NOT NULL, TIME VARCHAR(20) NOT NULL, PRIMARY KEY (ID));")
        query = f"INSERT INTO {DB_Table_name} (ID, ENROLLMENT, NAME, DATE, TIME) VALUES (0, %(enrollment)s, %(name)s, %(date)s, %(time)s)"
        data = [{'enrollment': row[0], 'name': row[1], 'date': row[2], 'time': row[3]} for row in attendance.values.tolist()]
        cursor.executemany(query, data)
        connection.commit()
        connection.close()
    except Exception as ex:
        print(ex)

    print("Attendance filled successfully")