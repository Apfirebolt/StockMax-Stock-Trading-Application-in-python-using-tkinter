from tkinter import *
import sqlite3 as db
import tkinter as tk
import tkinter.messagebox as tm
from sqlite3 import OperationalError
import pickle
import home


#Accounts class is created to manage portfolio for each user.
class Portfolio:
    def __init__(self, username, balance):
        self.username = username
        self.balance = balance
        self.stock_list = {}


root = tk.Tk()
root.title('User Login Window')
root.geometry('500x500')

#Username is all it is required to pass in login success function which would be interface between 2 modules.


def login_success(user):
    home.main(user)


def login_fail(x):
    x.destroy()


def login_clicked(e):
    #First we would perform some validation tests and then call the main function in home.py.
    #Pass the necessary database arguments effectively to perform all desired operations

    conn = db.connect('datastore.db')
    cursor = conn.cursor()
    current_user = e[0].get()
    current_password = e[1].get()

    query = cursor.execute('select Password from Stocks WHERE Username=?', (current_user,))
    result = query.fetchone()

    if result and current_password == result[0]:
        login_confirm = Tk()
        login_confirm.geometry('600x90')
        login_confirm.title('Login was a success XD')
        text = 'You are successfully logged in as ' + current_user + '.'
        text += '\nYou would now be directed to your StockMax account on pressing OK button.'

        success_button = Button(login_confirm, text='Ok', fg='black',
                                bg='bisque2', command=lambda user=current_user: login_success(user))
        success_button.pack(side='bottom', fill='x')

        lb = Label(login_confirm, text=text, fg='tomato')
        lb.pack(side='bottom')

    else:
        login_not_confirm = Tk()
        login_not_confirm.title('Login Failed!')
        login_not_confirm.geometry('600x90')
        text = 'Either username or password entered was wrong.'
        text += '\nPlease give it another try.'

        fail_button = Button(login_not_confirm, text='Ok', fg='black', bg='bisque2')
        fail_button.pack(side='bottom', fill='x')

        lb = Label(login_not_confirm, text=text, fg='red')
        lb.pack()

        login_not_confirm.mainloop()


def show_register_info(username, balance):
    top_level = Toplevel()
    top_level.title('Confirmation for successful registration.')

    text = 'Welcome ' + username + ' ,' + 'You have been successfully registered with balance ' + str(balance)
    text += ' \n You can now login to continue using StockMax Virtual Trading Platform.'
    label1 = Label(top_level, text=text, height=0, width=100, fg='sienna1')
    label1.pack()
    ok_button = Button(top_level, text='OK', height=2, width=20, command=top_level.destroy)
    ok_button.pack(side='bottom', fill='none', expand=True)


def register_clicked(e):
    user = e[0].get()
    password = e[1].get()
    confirm_password = e[2].get()
    balance = int(e[3].get())
    status = True

    #Successfully performed the username exiting check.

    conn = db.connect('datastore.db')
    table_exists = conn.execute("select * from sqlite_master where type='table' and name='Stocks'")

    #Table already exists then perform the required checks.
    flag = table_exists.fetchone

    if table_exists.fetchone():

        result = conn.execute('select * from Stocks WHERE Username=?',(user,))

        if result.fetchone():
            text = 'That username already exists, please pick another one and continue.'
            status = False
            conn.close()

        if balance <= 1000:
            text = 'Your balance is very low, please enter an amount greater than 1000 to use this application.'
            status = False

        if password != confirm_password:
            text = 'Your passwords dont match, please enter matching passwords and try again.'
            status = False

        if len(user) > 15:
            text = 'The username you choose was too long, please enter a shorter username and try again.'
            status = False

        if len(password) <= 8:
            text = 'Your password was too short, please enter a password of greater than 8 characters.'
            status = False

        if not status:
            tm.showinfo(text)

        #Validation of entries done till here. If program reached here means now insert user details in table
        else:
            #Connection was already opened before.

            ob = Portfolio(user, balance)

            # Created pickle name based on username which pickle belongs to
            pickle_name = user + ".pkl"
            pickle_out = open('user_data/' + pickle_name, "wb")
            pickle.dump(ob, pickle_out)
            pickle_out.close()

            #Data getting inserted in the database
            params = (user, password, balance, pickle_name)
            conn.execute("INSERT INTO Stocks VALUES (?, ?, ?, ?)", params)

            conn.commit()

            show_register_info(user, balance)

    # This is the condition for the very first entry when table stocks did not exist. So create table 'Stocks'
    # insert the data for first user and close the connection.
    else:
        query = "CREATE TABLE Stocks (Username TEXT PRIMARY KEY, Password TEXT, Balance INT, Stock_list BLOB)"

        #Table created here
        conn.execute(query)
        conn.commit()

        conn = db.connect('datastore.db')

        ob = Portfolio(user, balance)

        # Created pickle name based on username which pickle belongs to
        pickle_name = user + ".pkl"
        pickle_out = open('user_data/' + pickle_name, "wb")
        pickle.dump(ob, pickle_out)
        pickle_out.close()

        # Data getting inserted in the database
        params = (user, password, balance, pickle_name)
        conn.execute("INSERT INTO Stocks VALUES (?, ?, ?, ?)", params)

        conn.commit()

        show_register_info(user, balance)


def login_func():
    login_frame = tk.Frame(root, width=300, height=220)
    login_frame.pack(fill='none', expand=True)

    #Inside this frame use grid layout
    label_username = tk.Label(login_frame, text="Username")
    label_password = tk.Label(login_frame, text="Password")

    entry_username = tk.Entry(login_frame)
    entry_password = tk.Entry(login_frame, show="*")

    label_username.grid(row=0, sticky=E)
    label_password.grid(row=1, sticky=E)
    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    credentials = [entry_username, entry_password]

    ok_button = tk.Button(login_frame, text="Login", command=lambda e=credentials: login_clicked(e))
    ok_button.grid(columnspan=4)


def register_func():

    register_frame = tk.Frame(root, width=300, height=220)
    register_frame.pack(fill='none', expand=True)

    # Inside this frame use grid layout
    label_username = tk.Label(register_frame, text="Username")
    label_password = tk.Label(register_frame, text="Password")

    entry_username = tk.Entry(register_frame)
    entry_password = tk.Entry(register_frame, show="*")

    confirm_password_label = tk.Label(register_frame, text="Password Again")
    confirm_password = tk.Entry(register_frame, show="*")

    balance_label = tk.Label(register_frame, text="Starting Fund")
    balance = tk.Entry(register_frame)

    label_username.grid(row=0, sticky=E)
    label_password.grid(row=1, sticky=E)
    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    confirm_password_label.grid(row=2, sticky=E)
    confirm_password.grid(row=2, column=1)

    balance_label.grid(row=3, sticky=E)
    balance.grid(row=3, column=1)

    data = [entry_username, entry_password, confirm_password, balance]

    ok_button = tk.Button(register_frame, text="Register", command=lambda e=data: register_clicked(e))
    ok_button.grid(columnspan=4)


def exit_app():
    root.destroy()

login_text = """
            Welcome to the StockMax Trading Application, use this at your own risks because Market is risky.
            Please Login if you already have an account. Else, start by registering with a username and a starting balance. 
            We hope you have a great time using this application. Make a lot of VIRTUAL Money XD.

"""
msg = tk.Message(root,text=login_text)
msg.config(bg='light green', font=('helvetica', 10, 'bold italic'), width=400, padx=5, pady=5)
msg.pack(side='top')

exit_button = tk.Button(root, text='Exit', fg='red', bg='yellow', command=exit_app, height=2, width=15)
exit_button.pack(side='bottom', fill='x')

login_button = tk.Button(root, text='Login', fg='grey', bg='tan', command=login_func, height=2, width=15)
login_button.pack(side='bottom', fill='x')

register_button = tk.Button(root, text='Register', fg='powder blue', bg='crimson',
                            command=register_func, height=2, width=15, padx=20)
register_button.pack(side='bottom', fill='x')

root.mainloop()