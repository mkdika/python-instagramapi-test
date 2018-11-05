from InstagramAPI import InstagramAPI as IG
from random import randint
from pprint import PrettyPrinter
from operator import itemgetter

import time
import yaml
import os

# Follow & Un-follow user IG by given list

pp = PrettyPrinter(indent=2)

d1 = int(time.time())

print("============================")
print("      I N S T A G R A M     ")
print("     Follow and Un-Follow   ")
print("============================")

yaml_config_file_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'maxigbot.yml')

bot_config = yaml.load(open(yaml_config_file_path))

if len(bot_config) > 0:
    print(">> Configuration file loaded.\n")

ig_account = bot_config['maxigbot']['follow-unfollow']

follower_file = open(ig_account['target-path'], 'r')
list_follower = [line.split(',') for line in follower_file.readlines()]

print(">> Read follower list file, total: {0}".format(len(list_follower)))
print(">> Trying login to IG account.")

api = IG(ig_account['username'], ig_account['password'])
api.login()

total_follower = len(list_follower)
total_process = 0

for follower in list_follower:

    # unfollow demo
    response = api.unfollow(follower[1])
    print("Process un-follow '{0}' successful: {1}".format(
        follower[0], response))

    time.sleep(randint(2, 4))

    # Follow demo
    response = api.follow(follower[1])
    print("Process follow '{0}' successful: {1}".format(follower[0], response))

    total_process = total_process + 1
    complete = (total_process/total_follower)*100
    print("\t\t\t\t\t\tComplete: {0}% ({1}/{2})".format(
        round(complete, 2), total_process, total_follower))

    if total_process < total_follower:
        time.sleep(randint(10, 15))

time.sleep(randint(30, 50))
api.logout()

# Footer process
d2 = int(time.time())
print("=========================================================================")
print("\t\t\t\t\t\tAll done in {0} secs".format(d2-d1))
