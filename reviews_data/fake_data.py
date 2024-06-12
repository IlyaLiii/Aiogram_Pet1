from datetime import datetime

from faker import Faker
from reviews_data.fake_str import FAKE_STR
import os
from pathlib import Path
# PARENT_DIR = os.path.abspath(os.path.join('.', os.pardir))
# PHOTO_DIR = os.path.abspath(os.path.join(PARENT_DIR, 'files/review_images/'))
# # print(PHOTO_DIR)

img = Path(__file__).resolve().parents[1] / 'files' / 'review_images'

# print(img)
def get_photos():
    for file in os.listdir(Path(__file__).resolve().parents[1] / 'files' / 'review_images'):
        src = Path(__file__).resolve().parents[1] / 'files' / 'review_images'
        if os.path.isfile(os.path.join(src, file)):
            yield os.path.join('files/review_images', file)

# print([*get_photos()])



def create_ten_review(date):
    locale_list = ['en-US', 'en_US', 'ru_RU', 'en_US']
    fake = Faker(locale_list)
    names = [fake.unique.first_name() for i in range(10)]
    dates = [fake.date_between_dates(
        fake.date_between_dates(date_end=date, date_start='-2d')
    ) for i in range(10)]

    fake_textes = FAKE_STR.replace('\n', '').split(';')
    fake_textes.pop(-1)

    photos = [*get_photos()]

    new_list = []
    for i in range(10):
        new_list.append(list((names[i], dates[i], fake_textes[i], photos[i])))

    return new_list


data = create_ten_review(datetime.now())
new_text = ''
for i in range(10):
    new_text +=  f'''
name: {data[i][0]}
surname: {data[i][1]}
''' + '---------------'
