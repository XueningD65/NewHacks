import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import sql_login as sl
import cv2
import face_confirm as fc
import io
from PIL import Image, ImageTk

image_prefix = "./images/"
image_suffix = ".jpg"

#create a database for the app
sl.new_data()

def call_back():
    validify()
    #login.destroy()

def validify():
    #test if the entries are valid
    #will connect to database soon
    e_name = name.get()
    e_pwd = pwd.get()
    if(sl.validify_name(e_name)):
        if(sl.validify_password(e_name, e_pwd)):
            tkinter.messagebox.showinfo(parent = login,title='Login info', message='Succesful')
            name.delete(0, tk.END)
            pwd.delete(0,tk.END)

            fc.create(e_name,login)
        else:
            tkinter.messagebox.showwarning(parent = login,title='Login info', message='Invalid password')
            pwd.delete(0, tk.END)

    else:
        tkinter.messagebox.showwarning(parent = login,title='Login info', message='Username does not exist\nPlease register first!')
        name.delete(0, tk.END)
        pwd.delete(0, tk.END)

def register():

    def upload_image():
        path = tk.filedialog.askopenfilename()
        if(len(path)>0):
            global image
            image = cv2.imread(path)
            image = cv2.resize(image, (512,256+128))

    def take_picture():
        def confirm_photo():
            _,pic = cap.read()
            cap.release()
            global image
            image = pic
            image = cv2.resize(image, (512, 256 + 128))

            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            run = 0
            for (x, y, w, h) in faces:
                run = run+1
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Display the output
            cv2.imshow('Press any key to confirm', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            photo_window.destroy()

            if run==0:
                print("Error! No human face recognized!")
                tkinter.messagebox.showwarning(parent=reg_window, title='Photo warning', message='No human face detected! Please retake a photo!')


        def show_frame():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (512, 256 + 128))
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(5, show_frame)

        photo_window = tk.Toplevel(reg_window)
        width, height = 80, 60
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        lmain = tk.Label(photo_window)
        lmain.grid(row=0, column=0, padx=10, pady=5)
        show_frame()
        confirm__photo = tk.Button(photo_window,text="Confirm",width=10,command=confirm_photo)
        confirm__photo.grid(row=1, column=0, padx=10, pady=5)


    def info_check():
        e_name = entry_name.get()
        e_pwd = entry_pwd.get()
        e_confirm = entry_confirm.get()
        if(e_pwd != e_confirm):
            tkinter.messagebox.showwarning(title='Register info', message='Password does not match\nPlease enter again')
        else:
            img_path = image_prefix + e_name + image_suffix
            cv2.imwrite(img_path, image)

            if(sl.registration(e_name, e_pwd, img_path)):
                tkinter.messagebox.showinfo(title='Register info', message='Succesfully registered.\nPlease login')
                reg_window.destroy()
                return
            else:
                tkinter.messagebox.showwarning(title='Register info',
                                               message='Username already exists\nPlease enter again')

        reset()

    def reset():
        entry_name.delete(0,tk.END)
        entry_pwd.delete(0,tk.END)
        entry_confirm.delete(0,tk.END)

    reg_window = tk.Toplevel(login)
    reg_window.title("Registration Center")

    new_name = tk.StringVar()
    new_name.set("example@gmail.com")
    label_name = tk.Label(reg_window, text="New Name").grid(row=0, column=0)
    entry_name = tk.Entry(reg_window, textvariable=new_name)
    entry_name.grid(row=0,column=1,padx=10,pady=5)

    new_pwd = tk.StringVar()
    label_pwd = tk.Label(reg_window, text="New password").grid(row=1, column =0)
    entry_pwd = tk.Entry(reg_window, show = "*")
    entry_pwd.grid(row=1, column=1, padx=10, pady=5)

    confirm_pwd = tk.StringVar()
    label_confirm = tk.Label(reg_window, text="Confirm Password").grid(row=2, column=0)
    entry_confirm = tk.Entry(reg_window, show="*")
    entry_confirm.grid(row=2, column=1, padx=10, pady=5)

    new_photo = tk.StringVar()
    label_photo = tk.Label(reg_window, text="Add a photo").grid(row=3, column=0)
    button_upload = tk.Button(reg_window, text = "Upload a photo", width = 10, command = upload_image)
    button_upload.grid(row=3,column=1, padx=10,pady=5)
    button_take = tk.Button(reg_window, text = "Take now", width = 10, command = take_picture)
    button_take.grid(row=3, column=2, padx=10, pady=5)

    b_1 = tk.Button(reg_window, text="Sign Up", width=10, command=info_check).grid(row=4, column=0, sticky=tk.W, padx=10,
                                                                                 pady=5)
    b_2 = tk.Button(reg_window, text="Reset", width=10, command=reset).grid(row=4, column=1, sticky=tk.E, padx=10,
                                                                                  pady=5)



#The login interface
login = tk.Tk()
login.title("Log In")
label1 = tk.Label(login,text="Name").grid(row=0,column=0)
label2 = tk.Label(login,text="Password").grid(row=1,column=0)

password = tk.StringVar()
name = tk.Entry(login)
pwd = tk.Entry(login,show="*")
name.grid(row=0,column=1,padx=10,pady=5)
pwd.grid(row=1,column=1,padx=10,pady=5)

button_1 = tk.Button(login,text="Log in",width=10,command=call_back).grid(row=3,column=0,sticky=tk.W,padx=10,pady=5)
button_2 = tk.Button(login,text="Register",width=10,command=register).grid(row=3,column=1,sticky=tk.E,padx=10,pady=5)

tk.mainloop()