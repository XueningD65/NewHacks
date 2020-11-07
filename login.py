import tkinter as tk
import tkinter.messagebox
import sql_login as sl
import face_confirm as fc

#create a database for the app
sl.new_data()

def call_back():
    validify()
    login.destroy()

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
    def info_check():
        e_name = entry_name.get()
        e_pwd = entry_pwd.get()
        e_confirm = entry_confirm.get()
        if(e_pwd != e_confirm):
            tkinter.messagebox.showwarning(title='Register info', message='Password does not match\nPlease enter again')
        else:
            if(sl.registration(e_name, e_pwd)):
                tkinter.messagebox.showinfo(title='Register info', message='Succesfully registered.\nPlease login')
                reg_window.destroy()
                return
            else:
                tkinter.messagebox.showwarning(title='Register info',
                                               message='Username already exists\nPlease enter again')

        entry_name.delete(0, tk.END)
        entry_pwd.delete(0, tk.END)
        entry_confirm.delete(0, tk.END)

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