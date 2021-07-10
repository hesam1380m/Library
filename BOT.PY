from flask import Response
from flask import request
from flask import Flask
import json
import flask
import requests
import os
import pickle

url = "https://api.telegram.org/bot1803471003:AAGdjhk2vxKp9tE5rKscR2YytbdxKTfbE8g/"

def get_chat_id(update):
    return update['message']['chat']['id']


def sendMessage(chat_id, text):
    sendData = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url + 'sendMessage', sendData)
    return response






PATH = "C:/Users/ASUS\Desktop/Mabani/TAMRIN SERI 7"

def check_file_exist():
    import os
    if not os.path.exists(PATH+"users.dat") :
        f = open(PATH+"users.dat", 'wb')
        users_dict = {}
        pickle.dump(users_dict, f)
    
    if not os.path.exists(PATH+"books.dat") :
        f = open(PATH+"books.dat", 'wb')
        books_dict = {}
        pickle.dump(books_dict, f)

    if not os.path.exists(PATH+"borrows.dat") :
        f = open(PATH+"borrows.dat", 'wb')
        borrows_dict = {}
        pickle.dump(borrows_dict, f)

        

def add_user(name, family, code, birthday):
    check_file_exist()

    f = open(PATH+'users.dat', 'rb')
    users_dict = pickle.load(f)
    f.close()
    user_id = code[0:4]
    users_dict[user_id] = [name, family, code, birthday]

    f = open(PATH+'users.dat', 'wb')
    pickle.dump(users_dict, f)
    f.close()



def add_book(title, author, subject, year):
    check_file_exist()
    f = open(PATH+'books.dat', 'rb')
    book_dict = pickle.load(f)
    f.close()
    book_dict[title] = [author, subject, year]

    f = open(PATH+'books.dat', 'wb')
    pickle.dump(book_dict, f)
    f.close()


def search_book(title):
    f = open(PATH+'books.dat', 'rb')
    book_dict = pickle.load(f)
    f.close()
    print(book_dict[title])


def borrow(user_id, title):
    check_file_exist()
    f = open(PATH+'borrows.dat', 'rb')
    borrows_dict = pickle.load(f)
    f.close()
    borrows_dict[user_id] = title

    f = open(PATH+'borrows.dat', 'wb')
    pickle.dump(borrows_dict, f)
    f.close()

def show_all_info():
    f = open(PATH+'users.dat', 'rb')
    users_dict = pickle.load(f)
    f.close()
    f = open(PATH+'books.dat', 'rb')
    books_dict = pickle.load(f)
    f.close()
    f = open(PATH+'borrows.dat', 'rb')
    borrows_dict = pickle.load(f)
    f.close()

    print(users_dict)
    print("-------------------------------------------------")
    print(books_dict)
    print("-------------------------------------------------")
    print(borrows_dict)
    print("-------------------------------------------------")



#ch = 1
# while ch != 0:
#     print("1-Add User\n2-Add new Book\n3-Search book\n4-Borrow\n5-Show All info\n0-Exit")
#     ch = int(input())
    
#     if ch == 1:
#         name = input()
#         family = input()
#         code = input()
#         birthday = input()
#         add_user(name, family, code, birthday)

#     elif ch == 2:
#         title = input()
#         author = input()
#         subject = input()
#         year = input()
#         add_book(title, author, subject, year)

#     elif ch == 3:
#         book_title = input()
#         search_book(book_title)

#     elif ch == 4:
#         user_id = input()
#         title = input()
#         borrow(user_id, title)

#     elif ch == 5:
#         show_all_info()



app= Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text', '')
        if text == '/start':
            sendMessage(chat_id, " be ketabkhane ma khosh amadid ")
        else:
            pass
    else:
        return "<h2>myBot</h2>"


def write_json(data, filename="contactList.json"):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)


def read_json(filename="contactList.json"):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data

try:
    read_json()
except:
    write_json({})
app.run(debug=True)
