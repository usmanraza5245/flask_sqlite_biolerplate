from bson.objectid import ObjectId
import snscrape.modules.twitter as sntwitter
from config.db import db


class Scrapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def scrapKeywords(target):
        if (target['targetType'] == 'keywords'):
            if len(target['tweets']) == 0:
                for keyword in eval(target['targets']):
                    tweets = []
                    snsScrapper = sntwitter.TwitterSearchScraper(keyword)
                    for counter, tweet in enumerate(snsScrapper.get_items()):
                        if counter > target['limit']:
                            break
                        tweets.append({'keyword': keyword, 'date': tweet.date, 'id': tweet.id, 'rawContent': tweet.rawContent, 'username': tweet.user.username})
                    if len(tweets) > 0:
                        update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                        result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                        print(f"First Entry !!! Matched {result.matched_count} documents.")
                        print(f"First Entry !!! Modified {result.modified_count} documents.")
                    else:
                        print(">>> First Entry !!! No new tweets were found for "+exist['_id']+" " + exist['targetType'])

            else:
                for keyword in eval(target['targets']):
                    tweets = []
                    snsScrapper = sntwitter.TwitterSearchScraper(keyword)
                    for counter, tweet in enumerate(snsScrapper.get_items()):
                        if counter > target['limit']:
                            break
                        exist = list(filter(lambda tweet: tweet["id"] == tweet['id'], target['tweets']))
                        if not exist:
                            tweets.append({'keyword': keyword, 'date': tweet.date, 'id': tweet.id, 'rawContent': tweet.rawContent, 'username': tweet.user.username})
                    if len(tweets) > 0:
                        update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                        result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                        update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                        result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                        print(f"Scheduled : Matched {result.matched_count} documents.")
                        print(f"Scheduled : Modified {result.modified_count} documents.")
                    else:
                        print(">>> Scheduled!!! No new tweets were found for "+target['_id']+" " + target['targetType'] + " against keyword " + keyword)

        elif (target['targetType'] == 'twitter-hashtag'):
            if len(target['tweets']) == 0:
                for hashtag in eval(target['targets']):
                    tweets = []
                    snsScrapper = sntwitter.TwitterHashtagScraper(hashtag)
                    for counter, tweet in enumerate(snsScrapper.get_items()):
                        if counter > target['limit']:
                            break
                        tweets.append({'hashtag': hashtag, 'date': tweet.date, 'id': tweet.id, 'rawContent': tweet.rawContent, 'username': tweet.user.username})
                    if len(tweets) > 0:
                        update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                        result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                        print(f"First Entry !!! Matched {result.matched_count} documents for "+target['_id']+" " + target['targetType'] + " against hashtag " + hashtag)
                        print(f"First Entry !!! Modified {result.modified_count} documents for "+target['_id']+" " + target['targetType'] + " against hashtag " + hashtag)
                    else:
                        print(">>> First Entry !!! No new tweets were found for "+target['_id']+" " + target['targetType'] + " against hashtag " + hashtag)

            else:
                for hashtag in eval(target['targets']):
                    tweets = []
                    snsScrapper = sntwitter.TwitterSearchScraper(hashtag)
                    for counter, tweet in enumerate(snsScrapper.get_items()):
                        if counter > target['limit']:
                            break
                        exist = list(filter(lambda tweet: tweet["id"] == tweet['id'], target['tweets']))
                        if not exist:
                            tweets.append({'hashtag': hashtag, 'date': tweet.date, 'id': tweet.id, 'rawContent': tweet.rawContent, 'username': tweet.user.username})
                    if len(tweets) > 0:
                        update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                        result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                        update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                        result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                        print(f"Scheduled : Matched {result.matched_count} documents.")
                        print(f"Scheduled : Modified {result.modified_count} documents.")
                    else:
                        print(">>> Scheduled!!! No new tweets were found for "+target['_id']+" " + target['targetType'] + " against hashtag " + hashtag)

        elif (target['targetType'] == 'twitter-user'):
            try:
                if len(target['tweets']) == 0:
                    for username in eval(target['targets']):
                        tweets = []
                        snsScrapper = sntwitter.TwitterUserScraper(username)
                        for counter, tweet in enumerate(snsScrapper.get_items()):
                            if counter > target['limit']:
                                break
                            tweets.append({'username': username, 'date': tweet.date, 'id': tweet.id, 'rawContent': tweet.rawContent, 'username': tweet.user.username})
                        if len(tweets) > 0:
                            update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                            result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                            print(f"First Entry !!! Matched {result.matched_count} documents for "+target['_id']+" " + target['targetType'] + " against username " + username)
                            print(f"First Entry !!! Modified {result.modified_count} documents for "+target['_id']+" " + target['targetType'] + " against username " + username)
                        else:
                            print(">>> First Entry !!! No new tweets were found for "+target['_id']+" " + target['targetType'] + " against username " + username)

                else:
                    for username in eval(target['targets']):
                        tweets = []
                        snsScrapper = sntwitter.TwitterSearchScraper(username)
                        for counter, tweet in enumerate(snsScrapper.get_items()):
                            if counter > target['limit']:
                                break
                            exist = list(filter(lambda tweet: tweet["id"] == tweet['id'], target['tweets']))
                            if not exist:
                                tweets.append({'username': username, 'date': tweet.date, 'id': tweet.id, 'rawContent': tweet.rawContent, 'username': tweet.user.username})
                        if len(tweets) > 0:
                            update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                            result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                            update = {'$set': {'status': 1}, '$push': {'tweets': {'$each': tweets}}}
                            result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
                            print(f"Scheduled : Matched {result.matched_count} documents.")
                            print(f"Scheduled : Modified {result.modified_count} documents.")
                        else:
                            print(">>> Scheduled!!! No new tweets were found for "+target['_id']+" " + target['targetType'] + " against username " + username)
            except Exception as e:
                print(e)
                update = {'$set': {'status': 2}, }

                result = db.targets.update_one({'_id': ObjectId(target['_id'])}, update)
