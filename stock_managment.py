##
# stock_management.py

# MR-Spagetty
# 21/6/2021

import os
import json
import tkinter.filedialog as filedialogue
from difflib import SequenceMatcher


def did_you_mean(stock, item):
    """guesses what the user was trying to input

    Args:
        stock (dict): the current stock sheet
        item (str): what the program is trying to
        find the closest match in the stock sheet to

    Returns:
        str: if match confirmed corrected item otherwise
        the user's origonal input
    """
    probabilities = {'': 0}
    highest_prob = ''
    for item_name in stock.keys():
        # using Sequnce matcher to get a decimal value of how similar
        # the item is to the item in the stock sheet
        probabilities[item_name] = SequenceMatcher(
            None, item_name, item).ratio()
    for item_name in probabilities:
        if probabilities[item_name] > probabilities[highest_prob]:
            highest_prob = item_name
    match = input(f'Did you mean {highest_prob}; '
                  f'{probabilities[highest_prob] * 100:.2f}% '
                  'match (Y|N)').lower()
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
        item_info = input('what is the name, price, and stock(kg) of '
                          'the item you would like to add to the stock '
                          'sheet(format N,P,S(kg)): ').lower()
        if item_info.count(',') != 2:
            print('please format the name, price and stock to the format: '
                  'N,P,S(kg)')
        else:
            item_name, item_price, item_stock = item_info.split(',')
    stock[item_name] = {'price': item_price, 'amount': 0.0}
    stock = update_stock(stock, item_name, item_stock)
    return stock


def sell(stock, TAX=0.15):
    """selling stock

    Args:
        stock (dict): teh stock sheet
        TAX (float, optional): the amount of tax that will be added to teh price. Defaults to 0.15.

    Returns:
        dict: the update stock sheet
    """
    item_to_sell = input('what is the item you would like to sell')
    if item_to_sell not in stock:
        item_to_sell = did_you_mean(stock, item_to_sell)

    if item_to_sell in stock:
        valid = False
        amount_to_sell = -1
        while not valid:
            valid = True
            try:
                amount_to_sell = float(input('How mnay kgs of '
                                             f'{item_to_sell} do '
                                             'you want to sell: '))
            except ValueError:
                valid = False
            if amount_to_sell < 0:
                print('that is not a valid input\nvalid inputs are '
                      'numbers >= 0')
                valid = False
        if stock[item_to_sell]['amount'] - amount_to_sell < 0:
            print('not enough stock to make transaction')
        else:
            price = stock[item_to_sell]['price'] * amount_to_sell
            print(f'item: {item_to_sell}, amount: {amount_to_sell}kg, '
                  f'price(inc G.S.T): ${price * (1 + TAX)}, total '
                  f'G.S.T.: ${price  * TAX}')
            confirm = input('would you like to sell (Y|N)').lower()
            if confirm == 'y':
                stock = update_stock(stock, item_to_sell, amount_to_sell)
    return stock


def print_all(stock):
    for item in stock:
        print(f'{item}; price (exc G.S.T.):${stock[item]["price"]:.2f}, '
              f'stock:{stock[item]["amount"]}')


def update_stock(stock, item_to_change, change_amount, max_stock_kg=50.0):
    """update the amount of stock of an item already on the stock sheet

    Args:
        stock (dict): current stock sheet
        item_to_change (str): the item to change the stock level of
        change_amount ([type]): the amount to change the stock level by
        max_stock_kg (float, optional): the maximum amount of the iteem that
        can be stored. Defaults to 50.

    Returns:
        dict: the updated stock sheet
    """
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


def import_stock(stock) -> dict:
    """imports a previosly exported stock sheet

    Args:
        stock (dict): teh current stock sheet for if the import fails

    Returns:
        dict: the new stock sheet
    """
    path = filedialogue.askopenfilename(
        filetypes=(('JSON files', '*.json'), ('All files', '*.*'))
    )
    if os.path.isfile(path):
        with open(path, 'r') as file:
            stock = json.load(file)
    return stock


def menu():
    """menu function for the program
    """
    stock = {'red kumara': {'price': 3.0, 'amount': 0},
             'gold kumara': {'price': 3.5, 'amount': 0},
             'orange kumara': {'price': 3.9, 'amount': 0},
             'purple kumara': {'price': 5.0, 'amount': 0}}
    POSS_CHOICES = ['a', 's', 'r', 'p', 'i', 'e', 'q']
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
        choice = input().lower().strip()
        cont = False
        # interpreting the user's choice
        if choice not in POSS_CHOICES:
            print('that is not a valid choice')
        elif choice == 'a':
            stock = new_item(stock)
        elif choice == 's':
            stock = sell(stock)
        elif choice == 'r':
            # restocking the stock
            item = input('what would you like to update the stock of')
            item = did_you_mean(stock, item)
            valid = False
            amount_update = 0
            while not valid:
                valid = True
                try:
                    amount_update = float(input('What is the amount you '
                                                'would like to change the '
                                                f'stock level of {item} by'))
                except ValueError:
                    valid = False
                    print('that is not a valid number')
            if item in stock:
                stock = update_stock(stock, item, amount_update)
        elif choice == 'p':
            print_all(stock)
        elif choice == 'e':
            export(stock)
        elif choice == 'i':
            stock = import_stock(stock)
        elif choice == 'q':
            cont = False
            print('have a nice day')

if __name__ == "__main__":
    menu()
