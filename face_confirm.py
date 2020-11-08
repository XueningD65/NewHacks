import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import sql_login as sl
import io
import base64
import json
from time import localtime,strftime
import dlib
import todolist_page as tp

facerec = dlib.face_recognition_model_v1("model/dlib_face_recognition_resnet_model_v1.dat")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')


def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    print("euclidean distance: ", dist)
    if dist > 0.4:
        return "diff"
    else:
        return "same"

def test_face(img_real, img_db, name):
    dets = detector(img_real, 1)
    dets_fm = detector(img_db, 1)
    shape = predictor(img_real, dets[0])
    features_cap = facerec.compute_face_descriptor(img_real, shape)

    shape = predictor(img_db, dets_fm[0])
    features_formal = facerec.compute_face_descriptor(img_db, shape)

    compare = return_euclidean_distance(features_cap, features_formal)
    if compare == "same":
        tk.messagebox.showinfo(title='face input', message='correct')
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " name " + name + "\r\n")
        return True
    else:
        tk.messagebox.showinfo(title='face input', message='wrong')
        return False

def create(name,login):
    def confirm():
        cap.release()
        tp.create(name, root)

    def draw_login():
        image = sl.get_photo(name)
        image = cv2.imread(image)
        image = cv2.resize(image, (512, 256 + 128))
        db_image = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (512, 256 + 128))

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, name, (x, y), font, 0.8, (255, 0, 255), 1, cv2.LINE_AA)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        #if panelA is None or panelB is None:
        panelA = tk.Label(root,image=image)
        panelA.image = image
        panelA.grid(row=0,column=0,padx=10,pady=5)
        panelB = tk.Label(root)
        panelB.imgtk = imgtk
        panelB.grid(row=0,column=1,padx=10,pady=5)
        panelB.configure(image = imgtk)
        panelB.after(1, draw_login)
        '''else:
            panelA.configure(image = db_image)
            panelB.configure(image = imgtk)
            panelA.image = db_image
            panelB.imgtk = imgtk
            panelB.after(1, show_frame())'''

        proceed = tk.Button(root, text="Confirm and Proceed", width=10, command=confirm)
        proceed.grid(row=1, column=0, padx=10, pady=5)

    def show_frame():
        global panelA, panelB

        global db_image
        image = sl.get_photo(name)
        image = cv2.imread(image)
        image = cv2.resize(image, (512, 256 + 128))
        db_image = image
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
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        real_image = cv2image
        if test_face(real_image, db_image, name) == True:
            print("Confirmed!")
            uname = name
            draw_login()
            return
        else:
            print("Do not cheat!")

    login.destroy()
    root = tk.Tk()

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    width, height = 80, 60
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    show_frame()
    root.title("Test your cam")

    root.mainloop()