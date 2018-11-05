from InstagramAPI import InstagramAPI as IG
from random import randint
from pprint import PrettyPrinter
from operator import itemgetter

import time
import yaml
import os

# This Python script is to list down all your following's followers
# The result will generated into tmp/ folder

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
print("Total following: {0}".format(len(foll['users'])))

total_following = len(foll['users'])
processed = 0

following = []
for foll_user in foll['users']:

    uname = foll_user['username']
    u = {}
    api.searchUsername(uname)

    result = api.LastJson

    if result != None and 'user' in result:
        tuser = result['user']

        if tuser['is_verified']:
            u['pk'] = tuser['pk']                         # primary key
            u['username'] = uname                           # username
            u['follower'] = tuser['follower_count']         # follower total
            # u['following'] = tuser['following_count']     # following total
            # u['verified'] = tuser['is_verified']          # is verified
            following.append(u)

    processed = processed + 1
    complete = (processed/total_following) * 100
    print("Processed '{0}'\n\t\t\t\t\t\tComplete: {1}% ({2}/{3})".format(
        uname,
        round(complete, 2),
        processed,
        total_following))

    # delay for next user inquiry
    # to prevent from being blocked or banned.
    time.sleep(randint(1, 2))  # seconds

# logout account
api.logout()

# # sort by follower Descending
newlist = sorted(following, key=itemgetter('follower'), reverse=True)

with open('tmp/follower.txt', 'w') as f:
    for tuser in newlist:
        f.write("{0},{1},{2}\n"
                .format(tuser['username'],
                        tuser['pk'],
                        tuser['follower']))

# Footer process
d2 = int(time.time())
print("All done in {0} secs".format(d2-d1))
