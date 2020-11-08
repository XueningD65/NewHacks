import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import sql_login as sl
import io
import base64
import json

def create(name,login):
    def confirm():
        print("Confirmed Screen")

    def show_frame():
        global panelA, panelB

        image = sl.get_photo(name)
        image = cv2.imread(image)
        image = cv2.resize(image, (512, 256 + 128))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        #if panelA is None or panelB is None:
            # the first panel will store our original image

        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (512,256+128))

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        if panelA is None or panelB is None:
            panelA = tk.Label(image=image)
            panelA.image = image
            panelA.grid(row=0,column=0,padx=10,pady=5)
            panelB = tk.Label(root)
            panelB.imgtk = imgtk
            panelB.grid(row=0,column=1,padx=10,pady=5)
            panelB.configure(image = imgtk)
            panelB.after(1, show_frame)
        else:
            panelA.configure(image = image)
            panelB.configure(image = imgtk)
            panelA.image = image
            panelB.imgtk = imgtk
            panelB.after(1, show_frame)

    login.destroy()

    root = tk.Tk()
    global panelA, panelB
    panelA = None
    panelB = None

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    width, height = 80, 60
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    show_frame()
    root.title("Test your cam")
    btn = tk.Button(root, text="Confirm Image", command=confirm)
    btn.grid(row=1,column=1,padx=10,pady=5)
    root.mainloop()