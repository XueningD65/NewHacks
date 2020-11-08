import sqlite3
import tkinter as tk
import tkinter.messagebox as tm
import sql_login as sl

conn = sqlite3.connect('app_data.db')
c = conn.cursor()

def new_data():
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='task' ''')
    # if the count is 1, then table exists
    if (c.fetchone()[0] == 1):
        print('Table exists.')
    else:
        c.execute('''CREATE TABLE task(username text, job text, description text, due text, done text)''')
        conn.commit()

def save_data(name, job, desp, due):

    for row in c.execute("SELECT job FROM task WHERE username = ?;", [name]):
        print(row[0])
        if row[0]==job:
            print("Task already exists!")
            return False

    c.execute("INSERT INTO task VALUES (?,?,?,?,'No')", [name, job, desp, due])
    conn.commit()
    print("Successfully saved")
    return True

def get_data(name, src, colour, judge):
    def done_action():
        curr = head.get(head.curselection())
        update_status(curr)
        head.delete(tk.ACTIVE)

    def update_status(task):
        c.execute("UPDATE task SET done='Yes' WHERE username = ? AND job = ?;",[name, task])
        conn.commit()

    def order_action():
        head.delete(0, tk.END)
        f = c.execute("SELECT job,description,due FROM task WHERE username = ? AND done='No' ORDER BY due DESC;", [name])
        for row in f:
            head.insert("end", row[0])

    def share_action():
        def confirm_action():
            print("Accessing the user...")
            new_name = share_entry.get()
            if(sl.validify_name(new_name)==False):
                tm.showwarning(parent=share_box, title='Warning', message='The username does not exist!')
                reset_action()
                return
            else:
                curr_task = head.get(head.curselection())
                for row in c.execute("SELECT job FROM task WHERE username = ?;", [new_name]):
                    print(row[0])
                    if row[0] == curr_task:
                        tm.showwarning(parent=share_box, title='Warning', message='The other user already has the task!')
                        reset_action()
                        return

                f = c.execute("SELECT description, due, done FROM task WHERE username=? AND job=?;",[name, curr_task])

                for row in f:

                    c.execute("INSERT INTO task VALUES (?,?,?,?,?)", [new_name, curr_task, "Shared by "+name+" : "+row[0], row[1], row[2]])

                for row in c.execute("SELECT * FROM task"):
                    print(row)

                print("Task shared with",new_name)
                conn.commit()
                reset_action()

        def reset_action():
            share_entry.delete(0, tk.END)

        share_box = tk.Toplevel(src)
        share_box.title("Share with Other User")
        share_label = tk.Label(share_box, text="User name")
        share_label.grid(row=0, column=0, padx=10, pady=5)

        share_entry = tk.Entry(share_box)
        share_entry.grid(row=0, column=1, padx=10, pady=5)

        confirm_button = tk.Button(share_box, text = "Share", command = confirm_action)
        confirm_button.grid(row=1, column=0, padx=10, pady=5)

        re_button = tk.Button(share_box, text = "Reset", command = reset_action)
        re_button.grid(row=1, column=1, padx=10, pady=5)

    def print_detail():
        curr = head.get(head.curselection())
        info = c.execute("SELECT job, description, due FROM task WHERE username = ? AND job =?;",[name, curr])
        info_window = tk.Toplevel(src)
        info_window.title("Task information")

        for ele in info:
            job_title = tk.Label(info_window, text = "Task Name",font='Helvetica 15 bold')
            job_title.grid(row=0, column=0, padx=10, pady=5)
            job_title_info = tk.Label(info_window, text = ele[0], fg=colour)
            job_title_info.grid(row=0, column=1, padx=10, pady=5)

            job_description = tk.Label(info_window, text="Task description",font='Helvetica 15 bold')
            job_description.grid(row=1, column=0, padx=10, pady=5)
            job_description_info = tk.Label(info_window, text = ele[1], fg=colour)
            job_description_info.grid(row=1, column=1, padx=10, pady=5)

            job_due = tk.Label(info_window, text="Expected Finish Date",font='Helvetica 15 bold')
            job_due.grid(row=2, column=0, padx=10, pady=5)
            job_due_info = tk.Label(info_window, text = ele[2], fg=colour)
            job_due_info.grid(row=2, column=1, padx=10, pady=5)

    judge = True
    all = c.execute("SELECT job,description,due FROM task WHERE username = ? AND done='No';", [name])

    tk.Label(src, text=" Tasks list:").grid(row=2, column=1, padx=10, pady=5)
    head = tk.Listbox(src, fg=colour)
    head.grid(row=3, column=1, padx=10, pady=5)

    for row in all:
        head.insert("end", row[0])

    detail_button = tk.Button(src, text="More Detail", command = print_detail)
    detail_button.grid(row=4, column=1)

    order_button = tk.Button(src, text=" Order By Due ", command=order_action)
    order_button.grid(row=5, column=1)

    done_button = tk.Button(src, text="Done", command=done_action)
    done_button.grid(row=6, column=1)

    share_button = tk.Button(src, text="Share", command = share_action)
    share_button.grid(row=7, column=1)

def get_finished_data(name, src, colour):
    def done_action():
        tm.showwarning(parent = src,title='Warning', message='The task has been finished already!')

    def order_action():
        head.delete(0, tk.END)
        f = c.execute("SELECT job,description,due FROM task WHERE username = ? AND done='Yes' ORDER BY due DESC;", [name])
        for row in f:
            head.insert("end", row[0])


    def share_action():
        def confirm_action():
            print("Accessing the user...")
            new_name = share_entry.get()
            if(sl.validify_name(new_name)==False):
                tm.showwarning(parent=share_box, title='Warning', message='The username does not exist!')
                reset_action()
                return
            else:
                curr_task = head.get(head.curselection())
                for row in c.execute("SELECT job FROM task WHERE username = ?;", [new_name]):
                    print(row[0])
                    if row[0] == curr_task:
                        tm.showwarning(parent=share_box, title='Warning', message='The other user already has the task!')
                        reset_action()
                        return

                f = c.execute("SELECT description, due, done FROM task WHERE username=? AND job=?;",[name, curr_task])

                for row in f:

                    c.execute("INSERT INTO task VALUES (?,?,?,?,?)", [new_name, curr_task, row[0], row[1], row[2]])

                for row in c.execute("SELECT * FROM task"):
                    print(row)

                print("Task shared with",new_name)
                conn.commit()
                reset_action()

        def reset_action():
            share_entry.delete(0, tk.END)

        share_box = tk.Toplevel(src)
        share_box.title("Share with Other User")
        share_label = tk.Label(share_box, text="User name")
        share_label.grid(row=0, column=0, padx=10, pady=5)

        share_entry = tk.Entry(share_box)
        share_entry.grid(row=0, column=1, padx=10, pady=5)

        confirm_button = tk.Button(share_box, text = "Share", command = confirm_action)
        confirm_button.grid(row=1, column=0, padx=10, pady=5)

        re_button = tk.Button(share_box, text = "Reset", command = reset_action)
        re_button.grid(row=1, column=1, padx=10, pady=5)

    def print_detail():
        curr = head.get(head.curselection())
        info = c.execute("SELECT job, description, due FROM task WHERE username = ? AND job =?;",[name, curr])
        info_window = tk.Toplevel(src)
        info_window.title("Task information")

        for ele in info:
            job_title = tk.Label(info_window, text = "Task Name",font='Helvetica 15 bold')
            job_title.grid(row=0, column=0, padx=10, pady=5)
            job_title_info = tk.Label(info_window, text = ele[0], fg=colour)
            job_title_info.grid(row=0, column=1, padx=10, pady=5)

            job_description = tk.Label(info_window, text="Task description",font='Helvetica 15 bold')
            job_description.grid(row=1, column=0, padx=10, pady=5)
            job_description_info = tk.Label(info_window, text = ele[1], fg=colour)
            job_description_info.grid(row=1, column=1, padx=10, pady=5)

            job_due = tk.Label(info_window, text="Expected Finish Date",font='Helvetica 15 bold')
            job_due.grid(row=2, column=0, padx=10, pady=5)
            job_due_info = tk.Label(info_window, text = ele[2], fg=colour)
            job_due_info.grid(row=2, column=1, padx=10, pady=5)

    all = c.execute("SELECT job,description,due FROM task WHERE username = ? AND done='Yes';", [name])

    tk.Label(src, text="Tasks done").grid(row=2, column=1, padx=10, pady=5)
    head = tk.Listbox(src, fg=colour)
    head.grid(row=3, column=1, padx=10, pady=5)

    detail_button = tk.Button(src, text="More Detail", command=print_detail)
    detail_button.grid(row=4, column=1)

    order_button = tk.Button(src, text=" Order By Due ", command=order_action)
    order_button.grid(row=5, column=1)

    done_button = tk.Button(src, text="Done", command=done_action)
    done_button.grid(row=6, column=1)

    share_button = tk.Button(src, text="Share", command = share_action)
    share_button.grid(row=7, column=1)

    for row in all:
        head.insert("end", row[0])

def find_task(name, task,src, colour):
    some = c.execute("SELECT job,description,due,done FROM task WHERE username = ? AND job = ?;", [name, task])

    if(len(some.fetchall())==0):
        print("No such task")
        tm.showwarning(parent=src, title='Warning', message='The task does not exist!')
        return

    info = c.execute("SELECT job, description, due, done FROM task WHERE username = ? AND job =?;", [name, task])
    info_window = tk.Toplevel(src)
    info_window.title("Task information")

    job_title = tk.Label(info_window, text="Task Name", font='Helvetica 15 bold')
    job_title.grid(row=0, column=0, padx=10, pady=5)

    job_description = tk.Label(info_window, text="Task description", font='Helvetica 15 bold')
    job_description.grid(row=1, column=0, padx=10, pady=5)

    job_due = tk.Label(info_window, text="Expected Finish Date", font='Helvetica 15 bold')
    job_due.grid(row=2, column=0, padx=10, pady=5)

    job_status = tk.Label(info_window, text="Task Status", font='Helvetica 15 bold')
    job_status.grid(row=3, column=0, padx=10, pady=5)

    for ele in info:
        job_title_info = tk.Label(info_window, text=ele[0], fg=colour)
        job_title_info.grid(row=0, column=1, padx=10, pady=5)

        job_description_info = tk.Label(info_window, text=ele[1], fg=colour)
        job_description_info.grid(row=1, column=1, padx=10, pady=5)

        job_due_info = tk.Label(info_window, text=ele[2], fg=colour)
        job_due_info.grid(row=2, column=1, padx=10, pady=5)

        job_status_info = tk.Label(info_window, text=ele[3], fg=colour)
        job_status_info.grid(row=3, column=1, padx=10, pady=5)

def find_today(name, date, src, colour):
    def done_action():
        curr = head.get(head.curselection())
        update_status(curr)
        head.delete(tk.ACTIVE)

    def update_status(task):
        c.execute("UPDATE task SET done='Yes' WHERE username = ? AND job = ?;",[name, task])
        conn.commit()

    def order_action():
        head.delete(0, tk.END)
        f = c.execute("SELECT job,description,due FROM task WHERE username = ? AND due = ? AND done='No' ORDER BY job DESC;",[name, date])
        for row in f:
            head.insert("end", row[0])

    def share_action():
        def confirm_action():
            print("Accessing the user...")
            new_name = share_entry.get()
            if(sl.validify_name(new_name)==False):
                tm.showwarning(parent=share_box, title='Warning', message='The username does not exist!')
                reset_action()
                return
            else:
                curr_task = head.get(head.curselection())
                for row in c.execute("SELECT job FROM task WHERE username = ?;", [new_name]):
                    print(row[0])
                    if row[0] == curr_task:
                        tm.showwarning(parent=share_box, title='Warning', message='The other user already has the task!')
                        reset_action()
                        return

                f = c.execute("SELECT description, due, done FROM task WHERE username=? AND job=?;",[name, curr_task])

                for row in f:

                    c.execute("INSERT INTO task VALUES (?,?,?,?,?)", [new_name, curr_task, row[0], row[1], row[2]])

                for row in c.execute("SELECT * FROM task"):
                    print(row)

                print("Task shared with",new_name)
                conn.commit()
                reset_action()

        def reset_action():
            share_entry.delete(0, tk.END)

        share_box = tk.Toplevel(src)
        share_box.title("Share with Other User")
        share_label = tk.Label(share_box, text="User name")
        share_label.grid(row=0, column=0, padx=10, pady=5)

        share_entry = tk.Entry(share_box)
        share_entry.grid(row=0, column=1, padx=10, pady=5)

        confirm_button = tk.Button(share_box, text = "Share", command = confirm_action)
        confirm_button.grid(row=1, column=0, padx=10, pady=5)

        re_button = tk.Button(share_box, text = "Reset", command = reset_action)
        re_button.grid(row=1, column=1, padx=10, pady=5)

    def print_detail():
        curr = head.get(head.curselection())
        info = c.execute("SELECT job, description, due FROM task WHERE username = ? AND job =?;",[name, curr])
        info_window = tk.Toplevel(src)
        info_window.title("Task information")

        for ele in info:
            job_title = tk.Label(info_window, text = "Task Name",font='Helvetica 15 bold')
            job_title.grid(row=0, column=0, padx=10, pady=5)
            job_title_info = tk.Label(info_window, text = ele[0], fg=colour)
            job_title_info.grid(row=0, column=1, padx=10, pady=5)

            job_description = tk.Label(info_window, text="Task description",font='Helvetica 15 bold')
            job_description.grid(row=1, column=0, padx=10, pady=5)
            job_description_info = tk.Label(info_window, text = ele[1], fg=colour)
            job_description_info.grid(row=1, column=1, padx=10, pady=5)

            job_due = tk.Label(info_window, text="Expected Finish Date",font='Helvetica 15 bold')
            job_due.grid(row=2, column=0, padx=10, pady=5)
            job_due_info = tk.Label(info_window, text = ele[2], fg=colour)
            job_due_info.grid(row=2, column=1, padx=10, pady=5)

    judge = True
    all = c.execute("SELECT job,description,due FROM task WHERE username = ? AND due = ? AND done='No';", [name, date])

    tk.Label(src, text="Tasks due :").grid(row=2, column=1, padx=10, pady=5)
    head = tk.Listbox(src, fg=colour)
    head.grid(row=3, column=1, padx=10, pady=5)

    for row in all:
        head.insert("end", row[0])

    detail_button = tk.Button(src, text="More Detail", command = print_detail)
    detail_button.grid(row=4, column=1)

    order_button = tk.Button(src, text="Order By Name", command=order_action)
    order_button.grid(row=5, column=1)

    done_button = tk.Button(src, text="Done", command=done_action)
    done_button.grid(row=6, column=1)

    share_button = tk.Button(src, text="Share", command = share_action)
    share_button.grid(row=7, column=1)