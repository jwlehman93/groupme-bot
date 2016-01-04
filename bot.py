import urllib.request as req
import json
import urllib.error

#jeremy's token: 0lpCQwlI3phYqgpj3uosPSdAmzSmFQjeKMXWvejT


class Bot:
    """class used for creating and registering new bots on groupme as well as generally useful functions"""
    def __init__(self, name, access_token, callback_url="", avatar_url=""):
        self.name = name
        self.access_token = access_token
        self.callback_url = callback_url
        self.avatar_url = avatar_url
        self.bot_id = ''
        self.group_id = self.get_group_id()
        self.register()

    def register(self):
        obj = {
            'bot': {
                "name": self.name,
                "group_id": self.group_id,
                "callback_url": self.avatar_url,
                "avatar_url": self.avatar_url
            }
        }
        try:
            request = req.Request('https://api.groupme.com/v3/bots?token=' + self.access_token)
            request.add_header('Content-Type', 'application/json')
            response = req.urlopen(request, json.dumps(obj).encode('utf-8'))
            res_obj = json.loads(response.read().decode('utf-8'))
            self.bot_id = res_obj['response']['bot']['bot_id']
            print("Bot Id: " + self.bot_id)
            self.say_hello()
        except urllib.error.HTTPError as e:
            print(e.reason)

    def send_message(self, msg):
        obj = {
            "bot_id": self.bot_id,
            "text": msg
        }
        try:
            request = req.Request('https://api.groupme.com/v3/bots/post?')
            request.add_header('Content-Type', 'application/json')
            req.urlopen(request, json.dumps(obj).encode('utf-8'))
        except urllib.error.HTTPError as e:
            print(e.reason)

    def get_group_id(self):
        dev = input('Dev Mode?(y/n) ')
        if dev == 'y':
            return '17065393'
        else:
            try:
                request = req.Request('https://api.groupme.com/v3/groups?token=' + self.access_token)
                response = req.urlopen(request)
            except urllib.error.HTTPError as e:
                print(e.reason)
                exit(0)
            res_obj = json.loads(response.read().decode('utf-8'))
            name_id_dict = {}
            for i in res_obj['response']:
                print(i['name'])
                name_id_dict[i['name']] = i['group_id']
            group = input('select group from list above for bot')
            return name_id_dict[group]

    def remove_user(self, group_user_id, group_id):
        try:
            request = req.Request('https://api.groupme.com/v3/groups/' + group_id + '/members/' + group_user_id +
                                  '/remove?token=' + self.access_token, method='POST')
            req.urlopen(request)
        except urllib.error.HTTPError as e:
            print("User ID: " + group_user_id)
            print("group_id: " + group_id)
            print(e.reason)

    def add_user(self, name, user_id, group_id):
        try:
            request = req.Request('https://api.groupme.com/v3/groups/' + group_id + '/members/add?token=' +
                                  self.access_token, method='POST')
            request.add_header('Content-Type', 'application/json')
            obj = {
                'members': [
                    {
                        'nickname': name,
                        'user_id': user_id,
                    }
                ]
            }
            req.urlopen(request, json.dumps(obj).encode('utf-8'))
        except urllib.error.HTTPError as e:
            print(e.reason)

    def get_users(self, group_id):
        users = []
        try:
            request = req.Request('https://api.groupme.com/v3/groups/' + group_id + '?token=' + self.access_token,
                                  method='GET')
            response = req.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e.reason)
            return users
        res_obj = json.loads(response.read().decode('utf-8'))
        print(res_obj)
        for i in res_obj['response']['members']:
            users.append({
                'name': i['nickname'],
                'group_id': i['id'],
                'user_id': i['user_id']
            })
        return users

    def say_hello(self):
        self.send_message("Created bot: " + self.name)

    def say_goodbye(self):
        self.send_message(self.name + " says goodbye")

    def create_group(self, name):
        try:
            request = req.Request('https://api.groupme.com/v3/groups?token=' + self.access_token, method='POST')
            request.add_header('Content-Type', 'application/json')
            response = req.urlopen(request, json.dumps({'name': name}).encode('utf-8'))
            res_obj = json.loads(response.read().decode('utf-8'))
            return res_obj['response']['id']
        except urllib.error.HTTPError as e:
            print(e.reason)

    def delete_group(self, group_id):
        try:
            request = req.Request('https://api.groupme.com/v3/groups/' + group_id + '/destroy?token=' +
                                  self.access_token, method='POST')
            req.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e.reason)

    def __del__(self):
        obj = {
            'bot_id': self.bot_id
        }
        self.say_goodbye()
        try:
            request = req.Request('https://api.groupme.com/v3/bots/destroy?token='+self.access_token, method='POST')
            request.add_header('Content-Type', 'application/json')
            req.urlopen(request, json.dumps(obj).encode('utf-8'))
        except urllib.error.HTTPError as e:
            print(e.reason)


bot = Bot('Test Bot', '0lpCQwlI3phYqgpj3uosPSdAmzSmFQjeKMXWvejT')
bot.send_message("You do not stand a chance against my superior technology")
users = bot.get_users(bot.group_id)
for i in users:
    print(i['name'] + ': ' + i['group_id'])
#bot.remove_user(users[3]['group_id'], bot.group_id)
#bot.add_user('Bryce', users[3]['user_id'],bot.group_id)
del bot
