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

list_stock = ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL',
'BHARTIARTL', 'INFRATEL', 'CIPLA', 'COALINDIA', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GRASIM',
'HCLTECH', 'HDFCBANK', 'HEROMOTOCO', 'HINDALCO', 'HINDPETRO', 'HINDUNILVR', 'HDFC', 'ITC',
'ICICIBANK', 'IBULHSGFIN', 'IOC', 'INDUSINDBK', 'INFY', 'KOTAKBANK', 'LT', 'LUPIN', 'M&M',
'MARUTI', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATAMOTORS',
'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'VEDL', 'WIPRO', 'YESBANK', 'ZEEL']


def on_buy_util(a, b, c, d):
    unit = int(b.get())

    #Balance update
    a.balance = a.balance - (unit * c)

    #Portfolio update
    a.stock_list[d] = unit

    filename = 'user_data/' + a.username + '.pkl'
    file = open(filename, 'wb')

    #Storing updated values in pickled database.
    pickle.dump(a, file)
    file.close()

    success_text = 'Congratulations! You have bought ' + str(unit) + ' of ' + d
    messagebox.showinfo(success_text)


def on_buy_func(user, y):
    my_stock = y.get()

    temp = Portfolio('', 0)
    filename = 'user_data/' + user + '.pkl'
    file = open(filename, 'rb')
    temp = pickle.load(file)

    print(temp.balance)

    try:
        url = 'https://www.screener.in/company/' + my_stock
        response = requests.get(url)
        data = response.text

    except requests.exceptions.RequestException as exp:
        print(exp)

    soup = BeautifulSoup(data, 'lxml')

    data_items = soup.findAll('b')[0:4]
    stock_data = [item.text for item in data_items]

    current_price = stock_data[1]
    current_price = current_price.replace(',','')

    current_price = int(float(current_price))

    if current_price > temp.balance:
        messagebox.showinfo("You cannot buy this stock due to low balance.")

    else:
        quantity = temp.balance // current_price
        msg = 'You can buy ' + str(quantity) + ' of this stock.'

        #So far so good. Now call the on_buy_util function, pass quantity, user
        on_buy_window = tk.Tk()
        on_buy_window.geometry('400x200')
        on_buy_window.title('Confirmation for buying ' + my_stock)

        t1 = 'The current price of ' + my_stock + ' is ' + str(current_price)
        l1 = tk.Label(on_buy_window, text=t1)
        l1.pack(side='top')

        t2 = 'Your current balance is ' + str(temp.balance)
        l2 = tk.Label(on_buy_window, text=t2)
        l2.pack(side='top')

        l3 = tk.Label(on_buy_window, text=msg)
        l3.pack(side='top')

        on_buy_frame = tk.Frame(on_buy_window)
        quantity_label = tk.Label(on_buy_frame, text='Select quantity')
        quantity_label.pack(side='left')

        on_buy_entry = tk.Entry(on_buy_frame)
        on_buy_entry.pack(side='left')

        on_buy_frame.pack(side='top')

        on_buy_button = tk.Button(on_buy_window, text='Buy now',
                                  command=lambda a=temp, b=on_buy_entry, c=current_price, d=my_stock: on_buy_util(a, b, c, d))
        on_buy_button.pack(side='bottom')

        on_buy_window.mainloop()


def start(user):
    buy_window = tk.Tk()
    buy_window.title('Buy a stock!')
    buy_window.geometry('450x200')

    buy_frame = tk.Frame(buy_window)
    buy_label = tk.Label(buy_frame, text='Enter a stock to buy')
    buy_label.pack(side='left')

    buy_entry = tk.Entry(buy_frame)
    buy_entry.pack(side='left')

    buy_frame.pack(side='top')

    buy_button = tk.Button(buy_window, text='Buy this stock', command=lambda x=user, y=buy_entry: on_buy_func(x, y))
    buy_button.pack(side='bottom')

    buy_window.mainloop()

