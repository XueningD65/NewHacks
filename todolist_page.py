import tkinter as tk
from tkinter import colorchooser as cc
import calendar
from datetime import date
import sql_todo as st
import sql_login as sl

st.new_data()
printed_todo = False
bgc = "black"

def create(name,login):
    main_page = tk.Tk()
    date = calendar.datetime.datetime

    def print_todo():
        st.get_data(name, main_page, bgc, printed_todo)

    def print_finished():
        st.get_finished_data(name, main_page, bgc)

    def search_task():
        def search():
            print("loading...")
            st.find_task(name, search_entry.get(), main_page, bgc)

        def clear():
            search_entry.delete(0, tk.END)

        search_window = tk.Toplevel(main_page)
        search_window.title("Search a task")

        search_label = tk.Label(search_window, text="Task name").grid(row=0, column=0, padx=10, pady=5)

        search_entry = tk.Entry(search_window)
        search_entry.grid(row=0, column=1, padx=10, pady=5)

        search_button = tk.Button(search_window, text="Search", command=search)
        search_button.grid(row=1, column=0,padx=10, pady=5)
        search_button = tk.Button(search_window, text="Reset", command=clear)
        search_button.grid(row=1, column=1, padx=10, pady=5)

    def pick_colour():
        colour_name = cc.askcolor(parent = main_page)
        colour_name = colour_name[1]
        global bgc
        bgc = colour_name
        name_label['fg'] = bgc

    def print_due():
        today = date.today()
        date_info = today.strftime("%Y-%m-%d")
        print(date_info)
        st.find_today(name, date_info, main_page, bgc)

    def today_info():
        def paint(event):
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            canvas.create_oval(x1, y1, x2, y2, fill=bgc)

        today = date.today()
        date_info = today.strftime("%d/%b/%Y %H:%M:%S")

        info_page = tk.Toplevel(main_page)
        info_page.title("Something about today")
        tk.Label(info_page, text = "Today is "+date_info).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(info_page, text="Make a draw for yourself").grid(row=1, column=0, padx=10, pady=5)

        canvas = tk.Canvas(info_page,width=400,height=200)
        canvas.grid(row=3, column=0, padx=10, pady=5)
        canvas.bind("<B1-Motion>", paint)


    def add_new():
        def save():
            res = st.save_data(name, todo_title_entry.get(), todo_description_label_entry.get(), todo_time_entry.get())
            if (res):
                todo_window.destroy()
            else:
                reset()

        def reset():
            todo_title_entry.delete(0, tk.END)
            todo_description_label_entry.delete(0, tk.END)
            todo_time_entry.delete(0,tk.END)

        todo_window = tk.Toplevel(main_page)
        todo_window.title("Add new work")

        todo_title_label = tk.Label(todo_window, text="Job name").grid(row=0, column=0)
        todo_title_entry = tk.Entry(todo_window)
        todo_title_entry.grid(row=0, column=1, padx=10, pady=5)

        todo_description_label = tk.Label(todo_window, text="Detailed description").grid(row=1, column=0)
        todo_description_label_entry = tk.Entry(todo_window)
        todo_description_label_entry.grid(row=1, column=1, padx=10, pady=5)

        todo_time_label = tk.Label(todo_window, text="Due Date(YYYY-MM-DD)")
        todo_time_label.grid(row=2,column=0)
        todo_time_entry = tk.Entry(todo_window)
        todo_time_entry.grid(row=2, column=1, padx=10, pady=5)

        b_1 = tk.Button(todo_window, text="Confirm", width=10, command=save)
        b_1.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        b_2 = tk.Button(todo_window, text="Reset", width=10, command=reset)
        b_2.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)

    login.destroy()
    main_page.title("To do list")
    main_page.geometry('512x400')

    sl.get_leader_name()
    sl.get_teammate_name()

    tk.Button(main_page, text="Add new To-Do", command=add_new).grid(row=0, column=0)
    tk.Button(main_page, text="Print all To-Dos", command=print_todo).grid(row=1, column=0)
    tk.Button(main_page, text="Print Finished", command=print_finished).grid(row=2, column=0)
    tk.Button(main_page, text="Due Today", command=print_due).grid(row=3, column=0)
    tk.Button(main_page, text="Search Task", command=search_task).grid(row=4, column=0)
    tk.Button(main_page, text="Change colour", command=pick_colour).grid(row=5, column=0)
    tk.Button(main_page, text="What's Today", command=today_info).grid(row=6, column=0)

    name_label = tk.Label(main_page, text = "Welcome to the To-Doo APP! Dear "+name)
    name_label.grid(row=0, column=1)

    main_page.mainloop()
