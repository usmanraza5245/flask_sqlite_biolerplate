import snscrape.modules.twitter as sntwitter


class Scrapper:

    def scrapKeywords(target):
        if (target['targetType'] == 'keywords'):
            tweets = []
            snsScrapper = sntwitter.TwitterSearchScraper(
                'COVID Vaccine since:2021-01-01 until:2021-05-31')
            for counter, tweet in enumerate(snsScrapper.get_items()):
                if counter > 10:
                    break
                tweets.append(
                    [tweet.date, tweet.id, tweet.content, tweet.user.username])
            print(tweets)
