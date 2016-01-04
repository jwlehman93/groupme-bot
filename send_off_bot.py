import Bot
import sys


class SendOffBot(Bot):

    def __init__(self, name, access_token, callback_url='', avatar_url=''):
        Bot.__init__(self, name, access_token, callback_url, avatar_url)
        self.input_file = open(sys.argv[1])

    def get_seniors(self, input_file):
        line = input_file.readline()
        senior_names = line.split(',')
        for i in senior_names:
            i.trim()
        users = self.get_users(self, self.group_id)
        name_id = {}
        for i in users:
            if i['name'] in senior_names:




