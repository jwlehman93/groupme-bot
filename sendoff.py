import bot
import sys


class SendOffBot(bot):

    def __init__(self, name, access_token, callback_url='', avatar_url=''):
        bot.__init__(self, name, access_token, callback_url, avatar_url)
        self.input_file = open(sys.argv[1])
        self.new_group_id = self.create_group('Rugby Seniors 15/16')

    def get_seniors(self, input_file):
        line = input_file.readline()
        senior_names = line.split(',')
        for i in senior_names:
            i.trim()
        users = self.get_users(self, self.group_id)
        name_id = {}
        for i in users:
            if i['name'] in senior_names:
                name_id[i['name']] = i['name']
                name_id['id'] = i['user_id']
                name_id['rugby_id'] = i['group_id']
        return name_id

    def send_off(self):
        for i in self.senior_dict():
            self.add_user(i['name'], i['id'], self.new_group_id)
            self.remove_user(i['rugby_id'], self.group_id)







