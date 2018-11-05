from InstagramAPI import InstagramAPI as IG
from pprint import PrettyPrinter
from getpass import getpass
from random import randint
from datetime import datetime

import time
import yaml
import os

# Auto like user IG post by given list

pp = PrettyPrinter(indent=2)
count = 0

d1 = int(time.time())

print("=================")
print("I N S T A G R A M")
print(" Auto Like Post! ")
print("=================")

yaml_config_file_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'maxigbot.yml')

bot_config = yaml.load(open(yaml_config_file_path))

if len(bot_config) > 0:
    print(">> Configuration file loaded.\n")

list_user = bot_config['maxigbot']['auto-like-post']['account']
print(">> Total IG user to process: {0}".format(len(list_user)))

fin_user = 0

for user in list_user:

    api = IG(user['username'], user['password'])
    api.login()
    print(">> IG user '{0}' logged!".format(user['username']))
    print(">> Total target user: {0}".format(len(user['target-user'])))

    tot_target = len(user['target-user'])
    fin_target = 0

    for t_user in user['target-user']:
        print(">> Now targeting user '{0}'.".format(t_user))
        TARGET = {
            'username': '',
            'media': '',
            'media_like': [],
        }

        TARGET['username'] = t_user

        api.searchUsername(TARGET['username'])

        TARGET['user_data'] = api.LastJson['user']

        print(">> Checking '{0}' posts.".format(
            TARGET['username']
        ))

        print(">> Fetch '{1}' feed at {0}".format(
            time.strftime("%d-%m-%Y %H:%M", time.localtime()),
            t_user))
        api.getUserFeed(str(TARGET['user_data']['pk']))

        media = TARGET['media'] = api.LastJson['items']

        print(">> Total '{0}' post: {1} posts.".format(
            TARGET['username'],
            len(TARGET['media'])
        ))

        for item in media:
            # print all payload from new feeds
            # pp.pprint(item)
            print("===========================================================")
            if item['has_liked']:
                print("User {1} with Post ID {0} has been liked.".format(
                    item['id'], t_user))
            else:
                ts = int(int(item['device_timestamp'])/1000000)
                local_time = time.localtime(ts)
                print("User ID           : {0}".format(t_user))
                print("Post ID           : {0}".format(item['id']))
                print("Post Time (Local) : {0}".format(
                    time.strftime("%d-%m-%Y %H:%M", local_time)))
                print("Like Post         : {0}".format(item['has_liked']))
                print("Total like count  : {0}".format(item['like_count']))

                if 'carousel_media' in item:
                    list_img = item['carousel_media']
                    print("Carousel Img URL  :")
                    for img in list_img:
                        print(
                            "\t*  {0}".format(img['image_versions2']['candidates'][1]['url']))
                else:
                    print(
                        "Sample Image URL  :\n\t*  {0}".format(item['image_versions2']['candidates'][1]['url']))

                if item['caption'] != None:
                    print("Post caption      : {0}".format(
                        item['caption']['text'] or 'No caption!'))

                hasLiked = api.like(item['id'])
                if hasLiked:
                    print(">> You just liked this post at {0}".format(
                        time.strftime("%d-%m-%Y %H:%M", time.localtime())))
                    TARGET['media_like'].append(item['id'])
                    count = count + 1
                    print(">> Total auto post like : {0}".format(count))
                    rnd = randint(10, 20)
                    print(
                        ">> Delay {0} secs for next post to like.".format(rnd))
                    time.sleep(rnd)

        print(">> Process '{1}' to target user '{0}' done!".format(
            t_user, user['username']))
        fin_target = fin_target + 1

        if fin_target < tot_target:
            wait_next_target = randint(20, 30)
            print(">> Wait {0} secs for next target user.\n".format(
                wait_next_target))
            time.sleep(wait_next_target)
        else:
            print(">> Done all target user for '{0}'.".format(
                user['username']))

    fin_user = fin_user + 1

    if fin_user < len(list_user):
        api.logout()
        wait_next_user = randint(30, 45)
        print(">> Wait {0} secs for next IG user process.\n".format(
            wait_next_user))
        time.sleep(wait_next_user)
    else:
        print("======================================================= END")

d2 = int(time.time())
print("All done in {0} secs".format(d2-d1))
