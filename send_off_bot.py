import Bot
import sys

class SendOffBot(Bot):

    def __init__(self, name, access_token, callback_url='', avatar_url=''):
        Bot.__init__(self,name,access_token,callback_url,avatar_url)
        self.input_file = sys.argv[1]

