import csv
import base64
import requests
import pandas as pd
from slack import WebClient


class notify(object):

    def __init__(self):
        self.token = ''
        self.gitee_token = ''
        self.client = WebClient(token=self.token)
        self.channel = '#生日提醒'

        self.in_advance = []
        self.in_advance1 = '''🎂Birthday Notification🎂\n'''
        self.in_advance2 = '''{name} has 10 days until {age} birthday 🧁\n'''
        self.in_advance3 = '''Don't forget to buy gifts 🎈'''

        self.on_the_day = []
        self.on_the_day1 = '''🎂Birthday Notification🎂\n'''
        self.on_the_day2 = '''Today is {name}'s birthday, turn {age}🧁\n'''
        self.on_the_day3 = '''Go and send your blessings!🎈'''
        self.data = {name: pd.to_datetime(dates if len(dates) > 5
                                          else f'{pd.Timestamp.today().year}-{dates}')
                     for name, dates in self.get_data()}

    def remind(self, msg):
        return self.client.chat_postMessage(channel=self.channel, text=msg)

    def process(self):
        today = pd.Timestamp.today()
        # today = pd.to_datetime('2022-12-14')
        for name, bday in self.data.items():
            age = round((today - bday).days / 365)
            diff = bday + pd.DateOffset(days=-10)
            if today.month == bday.month and today.day == bday.day:
                self.on_the_day.append([name, age])
            elif today.month == diff.month and today.day == diff.day:
                self.in_advance.append([name, age])

        if self.in_advance:
            self.in_advance.sort(key=lambda x: x[1])
            for name, age in self.in_advance:
                fage = f"{age}'s" if age else ''
                self.in_advance1 += self.in_advance2.format(
                    name=name, age=fage)
            self.in_advance1 += self.in_advance3
            self.remind(self.in_advance1)

        if self.on_the_day:
            self.on_the_day.sort(key=lambda x: x[1])
            for name, age in self.on_the_day:
                fage = f'{age} years old' if age else ''
                self.on_the_day1 += self.on_the_day2.format(
                    name=name, age=fage)
            self.on_the_day1 += self.on_the_day3
            self.remind(self.on_the_day1)

        if today.day == 1:
            self.remind('A new month has begun, I am still running!')

    def get_data(self):
        get_file_hash = f'https://gitee.com/api/v5/repos/sentimentalk/notify/contents/dates.csv?access_token={self.gitee_token}&ref=master'
        sha = requests.get(get_file_hash).json()['sha']
        get_file_content = f'https://gitee.com/api/v5/repos/sentimentalk/notify/git/blobs/{sha}?access_token={self.gitee_token}'
        content = requests.get(get_file_content).json()['content']
        content = base64.b64decode(content).decode('utf-8').splitlines()
        return csv.reader(content)


x = notify()
x.process()
