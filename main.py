from datetime import datetime, timedelta
import io
from logging import exception
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from distutils.util import strtobool
import requests
import time
from bs4 import BeautifulSoup, Tag
from google.cloud import storage
import pandas as pd

import env
from model.category import Category
from model.twitter_account import TwitterAccount
from model.amazon_category import AmazonCategory

# ------------ GSpreadSheet周り
ApiScope = ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']
Credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'secure.json', ApiScope)
GspreadClient = gspread.authorize(Credentials)
SpreadSheet = GspreadClient.open(env.SPREADSHEET_NAME)
MainSheet = SpreadSheet.worksheet(env.MAINSHEET_NAME)
TwitterSheet = SpreadSheet.worksheet(env.TWITTERSHEET_NAME)


def getTwitterAccount():
    TwitterList = TwitterSheet.get_all_values()
    TwitterList.pop(0)
    TwitterList.pop(0)
    res = []
    for item in TwitterList:
        res += [TwitterAccount(item)]
    return res


def getTargetCategory():
    MainList = MainSheet.get_all_values()
    MainList.pop(0)
    MainList.pop(0)
    res = []
    # print(MainList)
    for item in MainList:
        # 「有効か」列が有効で存在するカテゴリーなこと
        if strtobool(item[2]) \
                and AmazonCategory.has_enum(item[0]):
            res += [Category(item)]
    return res


def updateLastTweetDatetime(categoryRow:int, datetime:datetime):
    MainSheet.update_cell(
        categoryRow,
        # F列が最終ツイート日時の前提で6にしている
        # update_cell()は1から始めるので5ではない
        6,
        datetime.strftime('%Y/%m/%d %H:%M:%S'))  # (行,列,更新値)
    pass

def main(event, context):

    twitterAccounts = getTwitterAccount()
    categories = getTargetCategory()

    print('Event ID: {}'.format(context.event_id))
    print('File: {}'.format(event['name']))
    # 2021-06-04T18:31:30.967Zなので区切る
    nowCreatedTime = datetime.strptime(
        event['updated'][:19], '%Y-%m-%dT%H:%M:%S').astimezone(env.JST)
    agoCreatedTime = nowCreatedTime + timedelta(hours=-1)

    filename = os.path.basename(event['name'])

    account = None
    for category in categories:
        if category.category_id == filename[:-4]:
            account = category.getTwitterAccount(twitterAccounts)
            if account is None:
                print("{} category is not set twitter account id".format(
                    filename[:-4]))
                return
            else:
                print("category name : "+filename[:-4])
                break
    if account is None:
        print("Unexpected error occurred.")
        return

    client = storage.Client()
    bucket = client.get_bucket(env.BUCKET_NAME)

    agoFileName = "{}/{}/{}/{}/{}".format(
        agoCreatedTime.year, agoCreatedTime.month,
        agoCreatedTime.day, agoCreatedTime.hour, filename)
    isExists = bool(bucket.get_blob(blob_name=agoFileName))
    # 前時のCSVファイルが存在しない場合は終了
    if not isExists:
        print("ago {} is not found".format(filename))
        return

    agoBlob = bucket.blob("{}/{}/{}/{}/{}".format(
                          agoCreatedTime.year, agoCreatedTime.month,
                          agoCreatedTime.day, agoCreatedTime.hour, filename))
    nowBlob = bucket.blob("{}/{}/{}/{}/{}".format(
                          nowCreatedTime.year, nowCreatedTime.month,
                          nowCreatedTime.day, nowCreatedTime.hour, filename))

    agoText = agoBlob.download_as_text()
    nowText = nowBlob.download_as_text()

    agoDf = pd.read_csv(io.StringIO(agoText), header=0, index_col=1)
    nowDf = pd.read_csv(io.StringIO(nowText), header=0, index_col=1)

    if not agoDf.index.is_unique:
        raise ValueError(
            "error! index is not unique\ncheck to {} file".format(filename))

    isTweet=False
    tweetCount = 0
    for index, nowItem in nowDf.iterrows():

        # TwitterAPIの上限に引っかからないように1カテゴリー5ツイート以上はしないようにする
        if 5 < tweetCount:
            break


        if len(agoDf) == 0 or not index in agoDf.keys():
            text = '''
Amazonランキング急上昇中！！
#Amazon #アマゾン #お買い得

■商品名：{title}
■URL：{url}
［{date}]
'''.format(
                title=nowItem['title'],
                url=nowItem['affUrl'],
                date=nowCreatedTime.strftime('%Y/%m/%d %H:%M:%S')).strip()
            isTweet = account.tweet(text)
            tweetCount+=1

        elif agoDf.at[index, 'rank'][1:] > nowItem['rank'][1:]:
            text = '''
Amazonランキング上昇中！
{ago}位 → {now}位!

#Amazon #アマゾン #お買い得 #ランキング

■商品名：{title}
■URL：{url}
［{date}]
'''.format(
                title=nowItem['title'],
                ago=agoDf.at[index, 'rank'][1:],
                now=nowItem['rank'][1:],
                url=nowItem['affUrl'],
                date=nowCreatedTime.strftime('%Y/%m/%d %H:%M:%S')).strip()
            isTweet = account.tweet(text)
            tweetCount+=1

        else:
            print("{} is not target".format(nowItem['title']))

    if isTweet:

        categoryRow = MainSheet.find(filename[:-4]).row
        updateLastTweetDatetime(categoryRow, nowCreatedTime)
