import pickle
from tkinter import ttk
import tkinter as tk
from tkinter import *


class Portfolio:
    def __init__(self, username, balance):
        self.username = username
        self.balance = balance
        self.stock_list = {}


#Main function of this module starts from here hence the name start LOL. Username passed as user from home function
def start(user):

    portfolio_window = tk.Tk()
    portfolio_window.title('Your Stocks and their quantity you hold')
    portfolio_window.geometry('400x400')

    scrollbar = Scrollbar(portfolio_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    data = Portfolio('', 0)
    filename = 'user_data/' + user + '.pkl'
    file = open(filename, 'rb')

    data = pickle.load(file)
    file.close()

    listbox = tk.Listbox(portfolio_window, height=100, width=200, bg='LightYellow2',
                         fg='black', font=('Courier', 10, 'bold'))
    listbox.pack()

    for key, value in data.stock_list.items():
        text = (str(key) + ' ------------------------ ' + str(value))
        listbox.insert(END, text)

    # attach listbox to scrollbar
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)




