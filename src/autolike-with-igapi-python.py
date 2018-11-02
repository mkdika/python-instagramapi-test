from InstagramAPI import InstagramAPI as IG
from pprint import PrettyPrinter
from getpass import getpass
from random import randint
from datetime import datetime
import time

count = 0

print("=================")
print("I N S T A G R A M")
print("  Auto Like Bot  ")
print("=================")

pp = PrettyPrinter(indent=2)

print("Please input your IG Account:")
api = IG(
    input('Username: '),
    getpass('Password: ')
)

api.login()

TARGET = {
    'username': '',
    'media': '',
    'media_like': [],
}

TARGET['username'] = input('Target IG Username: ')

api.searchUsername(TARGET['username'])

TARGET['user_data'] = api.LastJson['user']

# pp.pprint(TARGET['user_data'])
print('Okay! Checking {0} posts.'.format(
    TARGET['username']
))

print(">> Fetch user feed at {0}".format(
    time.strftime("%d-%m-%Y %H:%M", time.localtime())))
api.getUserFeed(str(TARGET['user_data']['pk']))

media = TARGET['media'] = api.LastJson['items']

print('Total Post @{0}: {1} posts.'.format(
    TARGET['username'],
    len(TARGET['media'])
))

for item in media:
    # print all payload from new feeds
    # pp.pprint(item)
    print("======================================================")
    if item['has_liked']:
        print("Post ID {0} has been liked.".format(item['id']))
    else:
        ts = int(int(item['device_timestamp'])/1000000)
        local_time = time.localtime(ts)
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

        print("Post caption      : {0}".format(
            item['caption']['text'] or 'No caption!'))
        hasLiked = api.like(item['id'])
        if hasLiked:
            print(">> You just liked this post at {0}".format(
                time.strftime("%d-%m-%Y %H:%M", time.localtime())))
            TARGET['media_like'].append(item['id'])
            count = count + 1
            print(">> Total auto post like : {0}".format(count))
            rnd = randint(10, 25)
            print(">> Delay {0} secs for next post to like.".format(rnd))
            time.sleep(rnd)

print("================================================== END")
