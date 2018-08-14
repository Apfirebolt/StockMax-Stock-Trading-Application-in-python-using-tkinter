import pickle
import tkinter as tk
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox


class Portfolio:
    def __init__(self, username, balance):
        self.username = username
        self.balance = balance
        self.stock_list = {}


def on_sell_util(a, b, c, d):
    unit = int(b.get())

    #Unit must be less than the quantity available in the portpolio
    if unit > a.stock_list[d]:
        messagebox.showinfo('Cannot sell, since you \nquantity entered was more \nthan what you have!')

    else:
        # Balance update
        a.balance = a.balance + (unit * c)

        # Portfolio update
        a.stock_list[d] -= unit

        # Deleting the stock if it's quantity falls to 0
        if a.stock_list[d] == 0:
            del a.stock_list[d]

        filename = 'user_data/' + a.username + '.pkl'
        file = open(filename, 'wb')

        # Storing updated values in pickled database.
        pickle.dump(a, file)
        file.close()

        success_text = 'Congratulations! \nYou have sold ' + str(unit) + ' of ' + d
        messagebox.showinfo(success_text)


def on_sell_func(user, y):
    #Gets the stock entered
    my_stock = y.get()

    #Loads the current user portfolio
    temp = Portfolio('', 0)
    filename = 'user_data/' + user + '.pkl'
    file = open(filename, 'rb')
    temp = pickle.load(file)

    if my_stock not in temp.stock_list:
        messagebox.showinfo('You do not own any units of ' + my_stock)

    else:
        #print('You do have this stock then. Let us sell it.')
        try:
            url = 'https://www.screener.in/company/' + my_stock
            response = requests.get(url)
            data = response.text

        except requests.exceptions.RequestException as exp:
            print(exp)

        soup = BeautifulSoup(data, 'lxml')

        data_items = soup.findAll('b')[1:2]
        stock_data = [item.text for item in data_items]

        current_price = stock_data[0]
        current_price = current_price.replace(',', '')

        #sanitazied current price value in readable format.
        current_price = int(float(current_price))

        #Created main window for selling function
        on_sell_window = tk.Tk()
        on_sell_window.geometry('400x200')
        on_sell_window.title('Confirmation for selling ' + my_stock)

        on_sell_frame = tk.Frame(on_sell_window)
        on_sell_frame.pack(side='top')

        quantity_label = tk.Label(on_sell_frame, text='Select quantity to sell ')
        quantity_label.pack(side='left')

        on_sell_entry = tk.Entry(on_sell_frame)
        on_sell_entry.pack(side='left')

        on_sell_frame.pack(side='top')

        on_sell_button = tk.Button(on_sell_window, text='Sell now',
                                  command=lambda a=temp, b=on_sell_entry, c=current_price, d=my_stock: on_sell_util(a, b,
                                                                                                                  c, d))
        on_sell_button.pack(side='bottom')

        on_sell_window.mainloop()


def start(user):
    sell_window = tk.Tk()
    sell_window.title('Sell a stock!')
    sell_window.geometry('450x200')

    sell_frame = tk.Frame(sell_window)
    sell_label = tk.Label(sell_frame, text='Enter a stock to sell')
    sell_label.pack(side='left')

    sell_entry = tk.Entry(sell_frame)
    sell_entry.pack(side='left')

    sell_frame.pack(side='top')

    sell_button = tk.Button(sell_window, text='Sell this stock', command=lambda x=user, y=sell_entry: on_sell_func(x, y))
    sell_button.pack(side='bottom')

    sell_window.mainloop()

