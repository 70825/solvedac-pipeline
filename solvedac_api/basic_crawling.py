from database.postgresql import postgresql
from validation.postgresql_validation import postgresql_validation
import pandas as pd
import requests
import json
import time

'''
유저: 실버5 ~ 플레티넘1 사이의 유저 이름을 데이터베이스에 저장
문제: 브론즈5 ~ 골드1 사이의 문제 번호를 데이터베이스에 저장
'''


class basic_crawling:
    def __init__(self):
        self.database = postgresql()
        self.validation = postgresql_validation()

    def filterProblem(self, number):
        url = f"https://solved.ac/api/v3/problem/show?problemId={number}"
        r_problem = requests.get(url)

        # 404 Not Found: 문제가 존재하지 않으므로 0을 반환
        if r_problem.status_code == 404: return 0

        while r_problem.status_code != requests.codes.ok:
            time.sleep(30)
            r_problem = requests.get(url)

        info = json.loads(r_problem.content.decode('utf-8'))
        if info['isSolvable'] and info['acceptedUserCount'] >= 50 and 0 < info['level'] <= 15:
            return 1
        return 0

    def insertProblemNumber(self, s=1000, e=25024):
        count = self.database.findMaxIndex(True)

        for i in range(s, e):
            if self.filterProblem(i):
                validation_df = pd.DataFrame({'index': [count], 'num': [i]})
                if self.validation.problem_validation(validation_df):
                    query = f"INSERT INTO problemID VALUES ({count}, {i})"
                    self.database.insertQuery(query=query)
                    count += 1

    def filterUser(self, page):
        filter_list = []

        url = f"https://solved.ac/api/v3/ranking/tier?page={page}"
        r_user = requests.get(url)
        if r_user.status_code == 404: return 0

        while r_user.status_code != requests.codes.ok:
            time.sleep(30)
            r_user = requests.get(url)

        info = json.loads(r_user.content.decode('utf-8'))

        for i in range(len(info['items'])):
            if 5 < info['items'][i]['tier'] <= 15:
                filter_list.append(info['items'][i]['handle'])

        return filter_list

    def insertUserName(self, s=1, e=1000):
        count = self.database.findMaxIndex(False)

        for i in range(s, e):
            if e == 1000: user_name_list = self.filterUser(i)
            else: user_name_list = self.filterUser(i)[:5]

            for name in user_name_list:
                validation_df = pd.DataFrame({'index': [count], 'name': [name]})
                if self.validation.user_validation(validation_df):
                    query = f"INSERT INTO userID VALUES ({count}, '{name}')"
                    self.database.insertQuery(query)
                    count += 1