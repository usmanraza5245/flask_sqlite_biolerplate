from bson.objectid import ObjectId
import snscrape.modules.twitter as sntwitter
from config.db import db


class Scrapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def scrapKeywords(target):
        if (target['targetType'] == 'keywords'):

            for keyword in eval(target['targets']):
                tweets = []
                snsScrapper = sntwitter.TwitterSearchScraper(keyword)
                for counter, tweet in enumerate(snsScrapper.get_items()):
                    if counter > target['limit  ']:
                        break
                    tweets.append({
                        'keyword': keyword,
                        'date': tweet.date,
                        'id': tweet.id,
                        'rawContent': tweet.rawContent,
                        'username': tweet.user.username})
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
            result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
            print(f"Matched {result.matched_count} documents.")
            print(f"Modified {result.modified_count} documents.")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        elif (target['targetType'] == 'twitter-hashtag'):
            for keyword in eval(target['targets']):
                tweets = []
                snsScrapper = sntwitter.TwitterHashtagScraper('#'+keyword)
                for counter, tweet in enumerate(snsScrapper.get_items()):
                    if counter > 10:
                        break
                    tweets.append({
                        'keyword': keyword,
                        'date': tweet.date,
                        'id': tweet.id,
                        'rawContent': tweet.rawContent,
                        'username': tweet.user.username})
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
            result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
            print(f"Matched {result.matched_count} documents.")
            print(f"Modified {result.modified_count} documents.")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        elif (target['targetType'] == 'twitter-user'):
            for username in eval(target['targets']):
                tweets = []
                snsScrapper = sntwitter.TwitterUserScraper(username)
                for counter, tweet in enumerate(snsScrapper.get_items()):
                    if counter > 10:
                        break
                    tweets.append({
                        'username': username,
                        'date': tweet.date,
                        'id': tweet.id,
                        'rawContent': tweet.rawContent,
                        'username': tweet.user.username})
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
            result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
            print(f"Matched {result.matched_count} documents.")
            print(f"Modified {result.modified_count} documents.")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
