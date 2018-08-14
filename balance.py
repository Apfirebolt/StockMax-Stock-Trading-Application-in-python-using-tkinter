import pickle
import tkinter as tk
from tkinter import messagebox


class Portfolio:
    def __init__(self, username, balance):
        self.username = username
        self.balance = balance
        self.stock_list = {}


def add_balance_util(a, b):
    s = int(b.get())
    a.balance += s

    filename = 'user_data/' + a.username + '.pkl'
    pickle_out = open(filename, 'wb')
    pickle.dump(a, pickle_out)
    pickle_out.close()

    messagebox.showinfo("Confirmation Message", str(s) + " was added to your account.")


def add_balance(x):
    add_balance_window = tk.Tk()
    add_balance_window.title('Adding balance to your account!')
    add_balance_window.geometry('400x200')

    add_balance_frame = tk.Frame(add_balance_window)
    add_balance_frame.pack(side='top', fill='x')

    add_balance_label = tk.Label(add_balance_frame, text='Enter the amount to add ')
    add_balance_label.pack(side='left')

    add_balance_entry = tk.Entry(add_balance_frame)
    add_balance_entry.pack(side='left')

    add_balance_button = tk.Button(add_balance_window, text='Ok',
                                   command=lambda a=x, b=add_balance_entry: add_balance_util(a, b))
    add_balance_button.pack(side='bottom', fill='x')


#Main function of this module starts from here hence the name start LOL. Username passed as user from home function
def start(user):
    temp = Portfolio('', 0)
    filename = 'user_data/' + user + '.pkl'
    file = open(filename, 'rb')
    temp = pickle.load(file)

    #closed the original loaded pickle user file.
    file.close()

    # temp has temporary variables extracted from pickled files. Successfully printed values.
    # print(temp.username)
    # print(temp.balance)
    # print(temp.stock_list)

    #Opening a new window layout
    balance_window = tk.Tk()
    balance_window.title('Your Account information!')
    balance_window.geometry('300x300')

    exit_button = tk.Button(balance_window, text='Exit', command=balance_window.destroy)
    exit_button.pack(side='bottom', fill='x')

    #Passing temp object as an argument (x) to permanently modify and write new balance value.
    balance_button = tk.Button(balance_window, text='Add Balance', command=lambda x=temp: add_balance(x))
    balance_button.pack(side='bottom', fill='x')

    balance_label = tk.Label(balance_window, text='Your current balance is Rs ' + str(temp.balance))
    balance_label.pack(side='bottom', fill='x')

    balance_window.mainloop()


