from flask import Response
from flask import request
from flask import Flask
import json
import requests
import os


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


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        try:
            text = msg['message'].get('text', '')
            if text == '/start':
                sendMessage(chat_id, "Welcome To Our Library")
            else:
                id_dict = read_json()
                username = msg['message']['from']['id']
                username = str(username)
                if 'user' in text:
                    try:
                        if str(username) not in id_dict.keys():
                            id_dict[username] = {}
                        if 'user' not in id_dict[username].keys():
                            id_dict[username]['user'] = []
                        user = text.split('-')
                        id_dict[username]['user'].append({
                            'code': user[3],
                            'name': user[1],
                            'family': user[2]
                        })
                        write_json(id_dict)
                        sendMessage(chat_id, 'User add')
                    except:
                        sendMessage(chat_id, 'invalid data')
                elif 'book' in text:
                    try:
                        if str(username) not in id_dict.keys():
                            id_dict[username] = {}
                        if 'book' not in id_dict[username].keys():
                            id_dict[username]['book'] = []
                        user = text.split('-')
                        id_dict[username]['book'].append({
                            'title': user[1],
                            'author': user[2],
                            'subject': user[3]
                        })
                        write_json(id_dict)
                        sendMessage(chat_id, 'Book add')
                    except:
                        sendMessage(chat_id, 'invalid data')
                elif 'borrow' in text:
                    try:
                        if str(username) not in id_dict.keys():
                            id_dict[username] = {}
                        if 'borrow' not in id_dict[username].keys():
                            id_dict[username]['borrow'] = []
                        user = text.split('-')
                        id_dict[username]['borrow'].append({
                            'PersonID': user[1],
                            'title': user[2]
                        })
                        write_json(id_dict)
                        sendMessage(chat_id, 'User Borrow Book')
                    except:
                        sendMessage(chat_id, 'invalid data')
                elif text == '/command1':
                    sendMessage(
                        chat_id, '1-Add User : Write Your Requsest With This Method --> adduser-Name-Family-ID\n2-Add new Book : Write Your Requsest With This Method --> addbook-Title-Author-Subject\n3-Borrow Book: Write Your Requsest With This Method --> borrow-PersonID-Title')
                elif text == '/command2':
                    try:
                        usersList = id_dict[str(username)]['user']
                        st = ''
                        for i in usersList:
                            st += i['name'] + ' ' + i['family'] + \
                                ' --> ID : ' + i['code'] + '\n'
                        sendMessage(chat_id, st)
                    except:
                        sendMessage(chat_id, 'An error occured')
                elif text == '/command3':
                    try:
                        bookList = id_dict[str(username)]['book']
                        st = ''
                        for i in bookList:
                            st += i['title'] + ' --> Author : ' + i['author'] + \
                                ' --> Subject : ' + i['subject'] + '\n'
                        sendMessage(chat_id, st)
                    except:
                        sendMessage(chat_id, 'An error occured')
                elif text == '/command4':
                    try:
                        borrowList = id_dict[str(username)]['borrow']
                        st = ''
                        for i in borrowList:
                            st += i['PersonID'] + \
                                ' borrow ' + i['title'] + '\n'
                        sendMessage(chat_id, st)
                    except:
                        sendMessage(chat_id, 'An error occured')
        except:
            pass
        return Response('ok', status=200)
    else:
        return "<h2>Library</h2>"


def write_json(data, filename="id_list.json"):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)


def read_json(filename="id_list.json"):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data


try:
    read_json()
except:
    write_json({})

#last_code
app.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))
