import json
import requests
from tkinter import *
from tkmacosx import Button


def get_bitcoin_rate(currency_code):
    request = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    request = json.loads(request.text)
    return request["bpi"][currency_code]["rate"]


def update_price():
    global currency, price, current_rate
    current_rate = get_bitcoin_rate(currency)
    price.set(f"1 BTC (₿) = {current_rate} {currency} ({currency_symbols[currency]})")


def change_currency(currency_code):
    global currency
    currency = currency_code


def update_converter():
    global bitcoin_entry, other_entry, other_currency_code

    if other_currency_code.get() != "":

        bitcoin_value = bitcoin_entry.get()
        other_value = other_entry.get()

        rate = float(get_bitcoin_rate(other_currency_code.get()).replace(",", ""))

        if any((bitcoin_value, other_value)):
            bitcoin_value = 0.0 if bitcoin_value == "" else float(bitcoin_value)
            other_value = 0.0 if other_value == "" else float(other_value)

            if bitcoin_value * rate != other_value:
                bitcoin_entry.delete(0, END)
                other_entry.delete(0, END)

                bitcoin_entry.insert(0, f"{bitcoin_value}")
                other_entry.insert(0, f"{bitcoin_value * rate}")


currency = "USD"
currency_symbols = {"USD": "$", "GBP": "£", "EUR": "€"}

current_rate = 0

root = Tk()
root.geometry("800x450")
root.title("Live Bitcoin Price Tracker")

price = StringVar()


TITLE_FONT = ("Avenir", 48, "bold")
RATE_FONT = ("Avenir", 36, "bold")
BUTTON_FONT = ("Avenir", 20, "bold")
ENTRY_FONT = ("Avenir", 20)

button_frame = Frame(root)
converter_frame = Frame(root)

heading_1 = Label(root, text="Live Bitcoin Price Tracker", font=TITLE_FONT)
rate = Label(root, textvariable=price, font=RATE_FONT)

us_dollar_button = Button(button_frame, text="U.S. Dollar 🇺🇸", command=lambda: change_currency("USD"), fg="white", bg="#FF0040", font=BUTTON_FONT)
british_pound_button = Button(button_frame, text="British Pound 🇬🇧", command=lambda: change_currency("GBP"), fg="white", bg="#0070FF", font=BUTTON_FONT)
euro_button = Button(button_frame, text="Euro 🇪🇺", command=lambda: change_currency("EUR"), fg="white", bg="#1F00FF", font=BUTTON_FONT)

heading_1.pack(pady=10)
rate.pack()
button_frame.pack()
us_dollar_button.grid(row=0, column=0, padx=5)
british_pound_button.grid(row=0, column=1, padx=5)
euro_button.grid(row=0, column=2, padx=5)

heading_2 = Label(root, text="Bitcoin Rate Converter", font=TITLE_FONT)

bitcoin_entry = Entry(converter_frame, font=ENTRY_FONT, width=10)
other_entry = Entry(converter_frame, font=ENTRY_FONT, width=10)

other_currency_code = StringVar()
other_currency = OptionMenu(converter_frame, other_currency_code, "USD", "GBP", "EUR")
other_currency.config(font=ENTRY_FONT)

heading_2.pack(pady=10)
converter_frame.pack()
bitcoin_entry.grid(row=0, column=0)
Label(converter_frame, text=" BTC (₿) = ", font=BUTTON_FONT).grid(row=0, column=1)
other_entry.grid(row=0, column=2)
other_currency.grid(row=0, column=3)

while True:
    update_price()
    update_converter()
    root.update()
