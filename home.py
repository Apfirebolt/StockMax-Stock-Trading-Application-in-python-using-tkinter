from tkinter import *
import tkinter as tk
from tkinter import ttk
import csv
import sqlite3 as db
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import balance
import buy
import portfolio
import sell

help_font = ('Verdana', 11)
msg_font = ('Courier', 10, 'bold')


def query_stock_graph(x):
    driver = webdriver.Chrome('C:\\Users\\Amit\\Downloads\\chromedriver_win32\\chromedriver.exe')
    my_stock = x.get()

    try:
        url = 'https://chartink.com/stocks/' + str(my_stock) + '.html'
        driver.get(url)

    except requests.exceptions.RequestException as exp:
        print(exp)


def query_stock_info(x):
    my_stock = x.get()
    try:
        url = 'https://www.screener.in/company/' + my_stock
        response = requests.get(url)

    except requests.exceptions.RequestException as exp:
        print(exp)

    # print(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    data_items = soup.findAll('b')[0:4]
    stock_data = [item.text for item in data_items]

    market_cap = stock_data[0]
    current_price = stock_data[1]
    year_high = stock_data[2]
    year_low = stock_data[3]

    mar_cap = 'The market capitalization of ' + my_stock + ' is ' + market_cap
    price = 'The current price of ' + my_stock + ' is ' + current_price
    high = 'The year high price of ' + my_stock + ' is ' + year_high
    low = 'The year low price of ' + my_stock + ' is ' + year_low

    stock_info_window = Tk()
    stock_info_window.title('Current Statistics for ' + my_stock)
    stock_info_window.geometry('400x150')

    l1 = Label(stock_info_window, text=mar_cap)
    l1.pack()

    l2 = Label(stock_info_window, text=price)
    l2.pack()

    l3 = Label(stock_info_window, text=high)
    l3.pack()

    l4 = Label(stock_info_window, text=low)
    l4.pack()

    ok_button = Button(stock_info_window, text='Ok', command=stock_info_window.destroy, bg='azure')
    ok_button.pack(fill='x', side='bottom')
    stock_info_window.mainloop()


def query_stocks():
    query_window = Tk()
    query_window.geometry('800x100')
    query_window.title('Query for a given Stock for current price, market cap, year end high and low')
    query_label = ttk.Label(query_window, text='Enter the Symbol of the stock ')
    query_label.pack(side='left')

    query_text = ttk.Entry(query_window)
    query_text.pack(side='left')

    query_button = ttk.Button(query_window, text='Get Details',
                              command=lambda x=query_text: query_stock_info(x))
    query_button.pack(side='left')

    query_button = ttk.Button(query_window, text='Get Stock Graph',
                              command=lambda x=query_text: query_stock_graph(x))
    query_button.pack(side='left')

    query_window.mainloop()


def show_stocks():
    stock_window = Tk()
    stock_window.geometry('600x600')
    stock_window.title('List of Stocks available in Nifty 50 charts')
    scrollbar = Scrollbar(stock_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(stock_window, height=100, width=200, bg='snow', fg='black', font=('Courier', 10, 'bold'))
    listbox.pack()

    # Get data from excel file and insert into listbox.
    file = open('stocklist.csv', 'r')
    reader = csv.reader(file)

    for line in reader:
        text = (line[0] + '  ' + line[1])
        listbox.insert(END, text)

    # attach listbox to scrollbar
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    stock_window.mainloop()


def logout(root):
    root.destroy()


# Help functions for menu items
def help_nifty():
    text = """
    As of now, this application is only designed to perform virtual trades on stocks listed on NIFTY 50 stock
    exchange of NSE India. We do hope to extend it further to cover other stocks in future.

    You can see the list of Stocks available by clicking on 'list of stocks' options. Keep in mind that these
    listed stocks on NIFTY index keep on changing and might not be the same by the time you might be using this 
    application.
    """
    nifty_window = tk.Tk()
    nifty_window.title('What are NIFTY 50 Stocks ?')
    # nifty_window.geometry('800x200')

    nifty_label = tk.Label(nifty_window, text=text, fg='black', bg='thistle1', font=help_font)
    nifty_label.pack(side='top', fill='x')

    ok_button = tk.Button(nifty_window, text='Ok', fg='black', bg='spring green', height=2,
                          command=nifty_window.destroy)
    ok_button.pack(side='bottom', fill='x')

    nifty_window.mainloop()


def help_buy():
    text = """
        How to buy a stock ? Very simple, just check the symbol of the stock you want to buy from the
        'List of Stocks' option. Click on the buy button and enter this in the text field and boom! you're done.

        Keep in mind that only the stocks listed on Nifty 50 exchange can be bought.
        """
    nifty_window = tk.Tk()
    nifty_window.title('How to buy a stock ?')
    # nifty_window.geometry('800x200')

    nifty_label = tk.Label(nifty_window, text=text, fg='black', bg='thistle1', font=help_font)
    nifty_label.pack(side='top', fill='x')

    ok_button = tk.Button(nifty_window, text='Ok', fg='black', bg='spring green', height=2,
                          command=nifty_window.destroy)
    ok_button.pack(side='bottom', fill='x')

    nifty_window.mainloop()


def help_sell():
    text = """
            How to sell a stock ? Incredibly simple, just check the symbol of the stock you want to sell from your
            portfolio. Click on the sell button and enter the quantity you want to sell and boom roasted! you're done.

            Of course you gotta buy a stock before you sell it. So, better check your portfolio in case you forgotten
            what stocks you own XD
            """
    nifty_window = tk.Tk()
    nifty_window.title('How to sell a stock ?')
    # nifty_window.geometry('800x200')

    nifty_label = tk.Label(nifty_window, text=text, fg='black', bg='thistle1', font=help_font)
    nifty_label.pack(side='top', fill='x')

    ok_button = tk.Button(nifty_window, text='Ok', fg='black', bg='spring green', height=2,
                          command=nifty_window.destroy)
    ok_button.pack(side='bottom', fill='x')

    nifty_window.mainloop()


def help_balance(x):
    conn = db.connect('datastore.db')
    result = conn.execute('select Balance from Stocks WHERE Username=?', (x,))
    b = result.fetchone()

    conn.close()
    text = "Hello %s, your initial balance was %d." % (x, int(b[0])) + """
            Need account balance related help ? Simply click on 'My Account' option of the main screen. 
            You can see your current balance over there and also add some balance if you're running out of funds. 

            Easy folks! isn't it ?
            """
    nifty_window = tk.Tk()
    nifty_window.title('How to view or add into account balance ?')
    # nifty_window.geometry('800x200')

    nifty_label = tk.Label(nifty_window, text=text, fg='black', bg='thistle1', font=help_font)
    nifty_label.pack(side='top', fill='x')

    ok_button = tk.Button(nifty_window, text='Ok', fg='black', bg='spring green', height=2,
                          command=nifty_window.destroy)
    ok_button.pack(side='bottom', fill='x')

    nifty_window.mainloop()


def help_query():
    text = """
                How to query for statistics for a given stock ? Click on 'Query for a stock' option and enter
                the stock symbol you want to query for. 

                This option provides statistics pertaining to the stock in question like the current price, 
                market capitalisation, year around high and low values of this stock.

                Note that this works for all the stocks, even for the ones not listed on NIFTY 50 stock. Great!

                Also, you would be directed to chartink.com website for the live graph for the given stock
                when you click 'show graph' option for the given stock in consideration.
            """

    nifty_window = tk.Tk()
    nifty_window.title('How to view or add into account balance ?')
    # nifty_window.geometry('800x200')

    nifty_label = tk.Label(nifty_window, text=text, fg='black', bg='thistle1', font=help_font)
    nifty_label.pack(side='top', fill='x')

    ok_button = tk.Button(nifty_window, text='Ok', fg='black', bg='spring green', height=2,
                          command=nifty_window.destroy)
    ok_button.pack(side='bottom', fill='x')

    nifty_window.mainloop()


def main(user):
    root = tk.Tk()
    root.geometry('700x700')
    root.title('StockMax Virtual Online Trading Platform')
    # print(user)

    button_logout = tk.Button(root, bg='floral white', fg='black', relief='flat', text='Logout', height=2,
                              command=lambda x=root: logout(x))
    button_logout.pack(side='bottom', fill='x')

    button_balance = tk.Button(root, bg='tan2', fg='black', relief='flat',
                               text='My Account', height=2, command=lambda x=user: balance.start(x))
    button_balance.pack(side='bottom', fill='x')

    button_portfolio = tk.Button(root, bg='pale green', fg='black', relief='flat',
                                 text='View Your Portfolio', height=2, command=lambda x=user: portfolio.start(x))
    button_portfolio.pack(side='bottom', fill='x')

    button_sell = tk.Button(root, bg='LightGoldenrod1', fg='black', relief='flat',
                            text='Sell a Stock', height=2, command=lambda x=user: sell.start(x))
    button_sell.pack(side='bottom', fill='x')

    button_buy = tk.Button(root, bg='misty rose', fg='black', relief='flat',
                           text='Buy a Stock', height=2, command=lambda x=user: buy.start(x))
    button_buy.pack(side='bottom', fill='x')

    button_stocks = tk.Button(root, bg='khaki', fg='black', relief='flat', text='View List of Stocks in Nifty 50',
                              height=2, command=show_stocks)
    button_stocks.pack(side='bottom', fill='x')

    button_query = tk.Button(root, bg='light cyan', fg='black', relief='flat', text='Query for a Stock',
                             height=2, command=query_stocks)
    button_query.pack(side='bottom', fill='x')

    welcome_text = 'Welcome dear ' + user + ' ,' + 'We hope that you would enjoy using StockMax.'
    welcome_label = tk.Label(root, fg='blue', text=welcome_text, height=200, width=400, font=msg_font)
    welcome_label.pack(side='bottom', fill='x')

    menu_bar = Menu(root)
    menu_bar.add_command(label="NIFTY 50 Stocks", command=help_nifty)
    menu_bar.add_command(label="How to buy ?", command=help_buy)
    menu_bar.add_command(label="How to sell ?", command=help_sell)
    menu_bar.add_command(label="How to add balance ?", command=lambda x=user: help_balance(x))
    menu_bar.add_command(label="How to query for a stock ?", command=help_query)

    # display the menu
    root.config(menu=menu_bar)

    root.mainloop()

