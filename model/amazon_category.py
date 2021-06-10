from enum import Enum, auto


class AmazonCategory(Enum):

    # -をキー値に使えないのでValuesに入れて比較する
    AMAZON_DEVICES = 'amazon-devices'
    APPAREL = 'apparel'
    APPLIANCES = 'appliances'
    AUDIBLE = 'audible'
    AUTOMOTIVE = 'automotive'
    BABY = 'baby'
    BEAUTY = 'beauty'
    BOOKS = 'books'
    COMPUTERS = 'computers'
    DIGITAL_TEXT = 'digital-text'
    DIY = 'diy'
    DVD = 'dvd'
    ELECTRONICS = 'electronics'
    ENGLISH_BOOKS = 'english-books'
    FASHION = 'fashion'
    FOOD_BEVERAGE = 'food-beverage'
    GIFT_CARDS = 'gift-cards'
    HOBBY = 'hobby'
    HPC = 'hpc'
    INDUSTRIAL = 'industrial'
    INSTANT_VIDEO = 'instant_video'
    JEWELRY = 'jewelry'
    KITCHEN = 'kitchen'
    MOBILE_APPS = 'mobile_apps'
    # MUSIC = 'dmusic' # こいつだけページ構造が異なるので除外
    MUSIC = 'music'
    MUSICAL_INSTRUMENTS = 'musical-instruments'
    OFFICE_PRODUCTS = 'office-products'
    PANTRY = 'pantry'
    PET_SUPPLIES = 'pet-supplies'
    SHOES = 'shoes'
    SOFTWARE = 'software'
    SPORTS = 'sports'
    TOYS = 'toys'
    VIDEOGAMES = 'videogames'
    WATCH = 'watch'


    @classmethod
    def has_enum(cls, name):
        for e in cls:
            if e.value == name:
                return True
        return False
