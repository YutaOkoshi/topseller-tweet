from distutils.util import strtobool
import re
from datetime import datetime
from model.twitter_account import TwitterAccount


class Category:

    def __init__(self, record):

        # recordの順序が、以下順序である前提
        # カテゴリID	カテゴリー名	有効か	クロール間隔(h)	データの最終更新日時	最終ツイート日時	ツイートするアカウントID
        self.category_id = record[0]
        self.is_enable = strtobool(record[2])
        self.crawl_duration = int(record[3] or 0)
        if re.match(
            r'[0-9]{4}\/[0-9]{2}\/[0-9]{2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}',
                record[4]):
            self.last_update = datetime.strptime(
                record[4]+'+0900', '%Y/%m/%d %H:%M:%S%z')
        else:
            self.last_update = None
        if re.match(
            r'[0-9]{4}\/[0-9]{2}\/[0-9]{2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}',
                record[5]):
            self.last_tweet = datetime.strptime(
                record[5]+'+0900', '%Y/%m/%d %H:%M:%S%z')
        else:
            self.last_tweet = None
        self.tweet_account_id = record[6]

    def __str__(self):
        return str(self.category_id)

    def getTwitterAccount(self, list: list[TwitterAccount]) -> TwitterAccount:
        res = None
        for account in list:
            if self.tweet_account_id == account.id:
                res = account
        return res
