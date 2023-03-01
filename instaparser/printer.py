from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client.insta

print('Подписчики пользователя magserg')
magserg_followers = db.followers.find({'linked_username': 'magserg'})
for follower in magserg_followers:
    pprint(f"{follower.get('username')} |:| {follower.get('full_name')}")


print('\n\nПодписки пользователя magserg')
magserg_followings = db.followings.find({'linked_username': 'magserg'})
for following in magserg_followings:
    pprint(f"{following.get('username')} |:| {following.get('full_name')}")


