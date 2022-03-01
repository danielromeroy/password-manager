import tkinter as tk
from tkinter import messagebox as mb
import random as rd
import pyperclip
import json

DEFAULT_EMAIL = "default_email@web.com"


# -------------- PASSWORD GENERATOR ------------#

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [rd.choice(letters) for _ in range(rd.randint(6, 10))] + \
                    [rd.choice(symbols) for _ in range(rd.randint(1, 6))] + \
                    [rd.choice(numbers) for _ in range(rd.randint(1, 6))]

    rd.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# --------------   SAVE PASSWORD    ------------#

def validate_data():
    if len(website_entry.get()) == 0 or len(username_entry.get()) == 0 or len(password_entry.get()) == 0:
        mb.showinfo(message="Please fill all data")
    else:
        save_data()


def save_data():
    ws = website_entry.get()
    eu = username_entry.get()
    pw = password_entry.get()

    ok = mb.askokcancel(title=f"{ws} password", message=f"Details entered:\n\nWebsite: {ws}\nUsername: {eu}\n"
                                                        f"Password:{pw}\n\nAre they correct?")

    if ok:
        save_dict = {
            ws.lower(): {
                "email": eu,
                "password": pw
            }
        }
        try:
            with open("./data/data.json", "r") as data_file:
                saved_data = json.load(data_file)
        except FileNotFoundError:
            with open("./data/data.json", "w") as data_file:
                json.dump(save_dict, data_file, indent=4)
        else:
            saved_data.update(save_dict)
            with open("./data/data.json", "w") as data_file:
                json.dump(saved_data, data_file, indent=4)

        website_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)


# --------------  PASSWORD SEARCH   ------------#

def search_password():
    try:
        with open("./data/data.json", "r") as data_file:
            saved_data = json.load(data_file)
    except FileNotFoundError:
        mb.showinfo(title="Error", message="No data file. Please create a password first.")
    else:
        if website_entry.get().lower() in saved_data:
            search_result = saved_data[website_entry.get().lower()]
            eu = search_result["email"]
            pw = search_result["password"]
            mb.showinfo(message=f"{website_entry.get()} data:\n\nUsername/E-mail: {eu}\nPassword: {pw}")
        else:
            mb.showinfo(message=f"No such website ({website_entry.get()}) in current database")


# --------------     UI SETUP       ------------#

window = tk.Tk()
window.title("MyPass")
window.config(padx=80, pady=40)

logo = tk.PhotoImage(file="./images/logo.png")
logo_canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
logo_canvas.create_image(100, 100, image=logo)
logo_canvas.grid(row=1, column=1, columnspan=3)

website_label = tk.Label()
website_label.config(text="Website:")
website_label.grid(row=2, column=1)

website_entry = tk.Entry()
website_entry.config(width=21)
website_entry.focus()
website_entry.grid(row=2, column=2)

search_button = tk.Button()
search_button.config(text="Search", command=search_password, width=17)
search_button.grid(row=2, column=3)

username_label = tk.Label()
username_label.config(text="E-mail/Username:")
username_label.grid(row=3, column=1)

username_entry = tk.Entry()
username_entry.config(width=42)
username_entry.insert(0, DEFAULT_EMAIL)
username_entry.grid(row=3, column=2, columnspan=2)

password_label = tk.Label()
password_label.config(text="Password:")
password_label.grid(row=4, column=1)

password_entry = tk.Entry()
password_entry.config(width=21)
password_entry.grid(row=4, column=2)

password_button = tk.Button()
password_button.config(text="Generate password", command=generate_password, width=17)
password_button.grid(row=4, column=3)

add_button = tk.Button()
add_button.config(text="Add password", width=36, command=validate_data)
add_button.grid(row=5, column=2, columnspan=2)

window.mainloop()
