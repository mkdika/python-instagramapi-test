from InstagramAPI import InstagramAPI as IG
from random import randint
from pprint import PrettyPrinter
from operator import itemgetter

import time
import yaml
import os

pp = PrettyPrinter(indent=2)

d1 = int(time.time())

print("==============================")
print("      I N S T A G R A M       ")
print(" Get Most Following Followers ")
print("==============================")

yaml_config_file_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'maxigbot.yml')

bot_config = yaml.load(open(yaml_config_file_path))

if len(bot_config) > 0:
    print(">> Configuration file loaded.\n")

ig_account = bot_config['maxigbot']['most-follower']

api = IG(ig_account['username'], ig_account['password'])
api.login()
print(">> IG user '{0}' logged!".format(ig_account['username']))

print(">> Processing follower data at {0}".format(
    time.strftime("%d-%m-%Y %H:%M", time.localtime())))
api.searchUsername(ig_account['username'])
USERX = {}
USERX['user_data'] = api.LastJson['user']

api.getUserFollowings(str(USERX['user_data']['pk']))
foll = api.LastJson

following = []
for foll_user in foll['users']:
    uname = foll_user['username']
    u = {}

    api.searchUsername(uname)
    tuser = api.LastJson['user']

    if tuser['is_verified']:
        u['pk'] = tuser['pk']
        u['username'] = uname
        u['follower'] = tuser['follower_count']
        u['following'] = tuser['following_count']
        u['verified'] = tuser['is_verified']
        following.append(u)

print("Total count: {0}".format(len(following)))
# sort by follower Descending
newlist = sorted(following, key=itemgetter('follower'), reverse=True)
pp.pprint(newlist)

# Footer process
d2 = int(time.time())
print("All done in {0} secs".format(d2-d1))
