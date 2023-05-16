import cv2

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Load the pre-trained face cascade XML file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the trained face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('TrainingImageLabel/Trainner.yml')

# Dictionary to map label numbers to student names
labels_dict = {0: "John", 1: "Alice", 2: "Bob"}  # Update with your labels and names

while True:
    # Read the frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Process each detected face
    for (x, y, w, h) in faces:
        # Extract the face region of interest (ROI)
        face_roi = gray[y:y + h, x:x + w]

        # Recognize the face using the trained recognizer
        label, confidence = recognizer.predict(face_roi)

        # Get the name associated with the predicted label
        name = labels_dict.get(label, "Unknown")

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the name above the rectangle box
        text = f"{name} ({round(confidence, 2)})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame in a window called "Webcam"
    cv2.imshow("Webcam", frame)

    # Check for the 'Esc' key to exit
    if cv2.waitKey(1) == 27:
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
