##
# stock_management.py

# MR-Spagetty
# 21/6/2021

import os, json
import tkinter.filedialog as filedialogue
from difflib import SequenceMatcher


def did_you_mean(stock, item):
    """guesses what teh user was trying to input

    Args:
        stock (dict): the current stock sheet
        item (str): what the program is trying to
        find the closest match in the stock sheet to

    Returns:
        str: if match confirmed corrected item otherwise the user's origonal input
    """
    probabilities = {'': 0}
    highest_prob = ''
    for item_name in stock.keys():
        probabilities[item_name] = SequenceMatcher(None, item_name, item).ratio()
    for item_name in probabilities:
        if probabilities[item_name] > probabilities[highest_prob]:
            highest_prob = item_name
    match = input(f'Did you mean {highest_prob}; '
                  f'{probabilities[highest_prob] * 100:.2f}% match (Y|N)').lower()
    if match == 'y':
        return highest_prob
    else:
        return item


def new_item(stock):
    """adds a new item to the stock managment system

    Args:
        stock (dict): the current stock sheet
        item_name (str): [description]
        item_price (float): [description]
        item_stock (float): [description]
    """
    valid = False
    while not valid:
        valid = True
        item_info = input('what is the name, price, and stock of the item you '
                        'would like to add to the stock sheet(format N,P,S): ').lower()
        if item_info.count(',')
    stock[item_name] = {'price': item_price, 'amount': 0.0}
    stock = update_stock(stock, item_name, item_stock)


def sell(stock):
    pass


def update_stock(stock, item_to_change, change_amount, max_stock_kg=50.0):
    if stock[item_to_change]['amount'] + change_amount > max_stock_kg:
        print(f'The stock can not go over {max_stock_kg}kg')
    else:
        updated_stock = stock[item_to_change]['amount'] + change_amount
        print(f'the stock of {item_to_change} has been updated from '
              f'{stock[item_to_change]["amount"]} to {updated_stock}')
        stock[item_to_change]['amount'] = updated_stock

    return stock


def export(stock):
    """exports the current sock information to a json file

    Args:
        stock (dict): the current stock ssheet
    """
    path = filedialogue.asksaveasfilename(
        filetypes=(('JSON files', '*.json'), ('All files', '*.*'))
        )
    if not path.endswith('.json'):
        path = f'{path}.json'

    with open(path, 'w') as file:
        json.dump(stock, file, indent=4)



def menu():
    TAX_DECI = 0.15
    stock = {'red kumara': {'price': 3.0, 'amount': 0},
             'gold kumara': {'price': 3.5, 'amount': 0},
             'orange kumara': {'price': 3.9, 'amount': 0},
             'purple kumara': {'price': 5.0, 'amount': 0}}
    cont = True
    while cont:
        print("""
Please enter:

(A)dd an item, price, and stock

(S)ell an item (include 15% GST)

(R)estock an item

(P)rint out all the items along with their prices and stock

(I)mport stock sheet

(E)xport stock sheet

(Q)uit
            """)
        cont = False
        did_you_mean(stock, 'red')

if __name__ == "__main__":
    menu()