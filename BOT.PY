from flask import Response
from flask import  request
from flask import Flask
import json
import flask
import requests
import pickle




def check_file_exist():
    import os

    if not os.path.exists("users.dat") :
        f = open("users.dat", 'wb')
        users_dict = {}
        pickle.dump(users_dict, f)
    
    if not os.path.exists("books.dat") :
        f = open("books.dat", 'wb')
        books_dict = {}
        pickle.dump(books_dict, f)

    if not os.path.exists("borrows.dat") :
        f = open("borrows.dat", 'wb')
        borrows_dict = {}
        pickle.dump(borrows_dict, f)

def add_user(name, family, code):
    check_file_exist()

    f = open('users.dat', 'rb')
    users_dict = pickle.load(f)
    f.close()
    user_id = code
    users_dict[user_id] = [name, family]

    f = open('users.dat', 'wb')
    pickle.dump(users_dict, f)
    f.close()



def add_book(title, author, subject):
    check_file_exist()
    f = open('books.dat', 'rb')
    book_dict = pickle.load(f)
    f.close()
    book_dict[title] = [author, subject]

    f = open('books.dat', 'wb')
    pickle.dump(book_dict, f)
    f.close()


def search_book(title):
    f = open('books.dat', 'rb')
    book_dict = pickle.load(f)
    f.close()
    print(book_dict[title])


def borrow(user_id, title):
    check_file_exist()
    f = open('borrows.dat', 'rb')
    borrows_dict = pickle.load(f)
    f.close()
    borrows_dict[user_id] = title

    f = open('borrows.dat', 'wb')
    pickle.dump(borrows_dict, f)
    f.close()

def show_user_info():
    f = open('users.dat', 'rb')
    users_dict = pickle.load(f)
    f.close()
    return users_dict

def show_book_info():
    f = open('books.dat', 'rb')
    books_dict = pickle.load(f)
    f.close()
    return books_dict

def show_borrow_info():
    f = open('borrows.dat', 'rb')
    borrows_dict = pickle.load(f)
    f.close()
    return borrows_dict

#ch = 1
# while ch != 0:
#     print("1-Add User\n2-Add new Book\n3-Borrow\n0-Exit")
#     ch = int(input())
    
#     if ch == 1:
#         name = input()
#         family = input()
#         code = input()
#         add_user(name, family, code)

#     elif ch == 2:
#         title = input()
#         author = input()
#         subject = input()
#         add_book(title, author, subject)

#     elif ch == 3:
#         user_id = input()
#         title = input()
#         borrow(user_id, title)


url = "https://api.telegram.org/bot1803471003:AAGdjhk2vxKp9tE5rKscR2YytbdxKTfbE8g/"

def get_chat_id(update):
    try:
        return update['message']['chat']['id']
    except:
        pass


def sendMessage(chat_id, text):
    sendData = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url + 'sendMessage', sendData)
    return response

app= Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        try:
            text = msg['message'].get('text', '')
        except:
            pass
        if text == '/start':
            sendMessage(chat_id,"be ketabkhane ma khosh amadid")
        elif 'add user' in text:
            sendMessage(chat_id,'User add')
            user=text.split('-')
            add_user(user[1],user[2],user[3])
        elif 'add book' in text:
            sendMessage(chat_id,'Book add')
            book=text.split('-')
            add_book(book[1],book[2],book[3])
        elif 'borrow' in text:
            sendMessage(chat_id,'User borrow Book')
            borrows=text.split('-')
            borrow(borrows[1],borrows[2])
        elif text == '/command1':
            sendMessage(chat_id,'"1-Add User\n2-Add new Book\n3-Borrow')
        elif text =='/command2':
            for i in show_user_info():
                sendMessage(chat_id,show_user_info()[i][1])
        elif text =='/command3':
            for i in show_book_info():
                sendMessage(chat_id,show_book_info()[i])
        elif text =='/command4':
            for i in show_borrow_info():
                sendMessage(chat_id,show_borrow_info()[i])
        return Response('ok', status=200)
    else:
        return "<h2>Library</h2>"




app.run(debug=True)
