from database.postgresql import postgresql
from validation.postgresql_validation import postgresql_validation
import pandas as pd
import requests
import json
import time

'''
유저: 골드5 ~ 플레티넘5 사이의 유저 이름을 데이터베이스에 저장
문제: 브론즈5 ~ 골드1 사이의 문제 번호를 데이터베이스에 저장
'''


class basic_crawling:
    def __init__(self):
        self.database = postgresql()
        self.validation = postgresql_validation()
        self.user_count = 1

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

    def insertProblemNumber(self):
        count = 1
        for i in range(1000, 25024):
            if self.filterProblem(i):
                validation_df = pd.DataFrame({'id': count, 'problemID': i})
                if self.validation.problem_validation(validation_df):
                    query = f"INSERT INTO problemID VALUES ({count}, {i})"
                    self.database.insertQuery(query=query)

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
                filter_list.append([self.user_count, info['items'][i]['handle']])
                self.user_count += 1

        return filter_list

    def insertUserName(self):
        for i in range(1, 1000):
            user_name_list = self.filterUser(i)

            for idx, name in user_name_list:
                validation_df = pd.DataFrame({'id': idx, 'userId': name})
                if self.validation.user_validation(validation_df):
                    query = f"INSERT INTO userID VALUES ({idx}, '{name}')"
                    self.database.insertQuery(query)