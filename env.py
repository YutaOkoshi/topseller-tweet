import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import timedelta, timezone
import os


if os.getenv("GCLOUD_PROJECT") is not None:
    print('is production mode')
    IS_PRD = True
else:
    IS_PRD = False

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

JST = timezone(timedelta(hours=+9), 'JST')

#------------ スプレットシート周り
SPREADSHEET_NAME = os.environ.get('SPREADSHEET_NAME')
MAINSHEET_NAME = os.environ.get('MAINSHEET_NAME')
TWITTERSHEET_NAME = os.environ.get('TWITTERSHEET_NAME')


#------------ アフェリエイトURL用のタグ
AFF_TAG = os.environ.get('AFF_TAG')

#------------ twitter周り
API_KEY = os.environ.get('API_KEY')
API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET_TOKEN = os.environ.get('ACCESS_SECRET_TOKEN')

#------------ PA-API周り
PA_API_ACCESS_KEY = os.environ.get('PA_API_ACCESS_KEY')
PA_API_ACCESS_SECRET_KEY = os.environ.get('PA_API_ACCESS_SECRET_KEY')

#------------ スプレイピング周り
UA = os.environ.get('UA')

#------------ GCP周り

# ローカルから実行するときはCredentialsで認証する
if not IS_PRD:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './secure.json'
BUCKET_NAME = os.environ.get('BUCKET_NAME')
