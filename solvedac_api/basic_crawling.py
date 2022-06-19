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
        '''
        :param number: 문제 번호
        :return: 문제가 조건에 만족하는지 유무
        '''

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
        '''
        :param s: 탐색을 시작할 문제 번호
        :param e: 탐색을 끝낼 문제 번호
        :return: index와 문제 번호를 SQL에 저장
        '''

        count = self.database.findMaxIndex(True)

        for i in range(s, e):
            if self.filterProblem(i):
                validation_df = pd.DataFrame({'index': [count], 'num': [i]})
                if self.validation.problem_validation(validation_df):
                    query = f"INSERT INTO problemID VALUES ({count}, {i})"
                    self.database.insertQuery(query=query)
                    count += 1

    def findTierPage(self, startTier, endTier): # 이진 탐색 알고리즘 적용
        '''
        :param startTier: 탐색을 시작하는 티어
        :param endTier:  탐색을 끝내는 티어
        :return: start_page(시작 페이지), end_page(끝 페이지)
        '''
        start_page, end_page = 0, 0

        # start_page 설정
        s, e = 1, 719
        while s + 1 <= e:
            mid_page = (s + e) // 2

            url = f"https://solved.ac/api/v3/ranking/tier?page={mid_page}"
            r_tier_user = requests.get(url)

            while r_tier_user.status_code != requests.codes.ok:
                time.sleep(30)
                r_tier_user = requests.get(url)

            info = json.loads(r_tier_user.content.decode('utf-8'))
            first_user_tier = int(info['items'][0]['tier'])
            last_user_tier = int(info['items'][-1]['tier'])

            # 첫번째 유저의 티어가 startTier보다 작은 경우, 해당 리스트에 있는 모든 유저는 티어가 startTier보다 작으므로 볼 필요가 없다.
            if first_user_tier < startTier:
                e = mid_page
                continue

            # 첫번째 유저의 티어가 startTier와 같은 경우, 현재 페이지가 시작 페이지가 아닐 수도 있으니 다시 탐색한다.
            if first_user_tier == startTier:
                e = mid_page
                start_page = mid_page
                continue

            # 첫번째 유저의 티어가 startTier보다 작은 경우, 마지막 티어의 유저가 startTier보다 크거나 같으면 해당 페이지, 작으면 더 탐색한다.
            if first_user_tier > startTier:
                if last_user_tier <= startTier:
                    start_page = mid_page
                    break
                else:
                    s = mid_page
                    continue

        # end_page 설정
        s, e = 1, 719
        while s + 1 <= e:
            mid_page = (s + e) // 2

            url = f"https://solved.ac/api/v3/ranking/tier?page={mid_page}"
            r_tier_user = requests.get(url)

            while r_tier_user.status_code != requests.codes.ok:
                time.sleep(30)
                r_tier_user = requests.get(url)

            info = json.loads(r_tier_user.content.decode('utf-8'))
            first_user_tier = int(info['items'][0]['tier'])
            last_user_tier = int(info['items'][-1]['tier'])

            # 마지막 유저의 티어가 endTier보다 큰 경우, 해당 리스트에 있는 모든 유저는 티어가 endTier보다 크므로 나머지는 볼 필요가 없다.
            if last_user_tier > endTier:
                s = mid_page
                continue

            # 마지막 유저의 티어가 endTier와 같은 경우, 현재 페이지가 마지막 페이지가 아닐 수도 있으니 다시 탐색한다.
            if last_user_tier == endTier:
                s = mid_page
                end_page = mid_page
                continue

            # 마지막 유저의 티어가 endTier보다 작은 경우, 첫번째 유저의 티어가 endTier보다 크거나 같으면 해당 페이지, 아니면 더 탐색한다.
            if last_user_tier < endTier:
                if first_user_tier >= endTier:
                    end_page = mid_page
                    break
                else:
                    e = mid_page
                    continue

        return start_page, end_page

    def filterUser(self, page):
        '''
        :param page: 랭킹 목록에서의 page 값
        :return: 해당 page에 속하는 유저의 아이디
        '''
        filter_list = []

        url = f"https://solved.ac/api/v3/ranking/tier?page={page}"
        r_user = requests.get(url)

        while r_user.status_code != requests.codes.ok:
            time.sleep(30)
            r_user = requests.get(url)

        info = json.loads(r_user.content.decode('utf-8'))

        for i in range(len(info['items'])):
            if 5 < info['items'][i]['tier'] <= 15:
                filter_list.append(info['items'][i]['handle'])

        return filter_list

    def filterTierUser(self, page, startTier, endTier):
        '''
        :param page: 탐색 페이지
        :param startTier: 해당 티어에 속하는 유저인지 확인
        :param endTier: 해당 티어에 속하는 유저인지 확인
        :return: 유저의 닉네임
        '''

        filter_list = []

        url = f"https://solved.ac/api/v3/ranking/tier?page={page}"
        r_user = requests.get(url)

        while r_user.status_code != requests.codes.ok:
            time.sleep(30)
            r_user = requests.get(url)

        info = json.loads(r_user.content.decode('utf-8'))

        for i in range(len(info['items'])):
            if startTier <= info['items'][i]['tier'] <= endTier:
                filter_list.append(info['items'][i]['handle'])

        return filter_list

    def insertUserName(self, tierFlag=False, s=1, e=1000):
        '''
        :param tierFlag: 특정 티어에 속하는 유저를 확인하는지의 유무(False면 페이지로 확인)
        :param s: tierFlag(True): 어느 티어부터 탐색을 시작할지, tierFlag(False): 몇페이지에서 탐색을 시작할지
        :param e: tierFlag(True): 어느 티어에서 탐색을 끝낼지, tierFlag(False): 몇페이지에서 탐색을 끝낼지
        :return: index와 유저 id를 SQL에 저장
        '''
        count = self.database.findMaxIndex(False)
        user_name_list = []

        if tierFlag:
            start_page, end_page = self.findTierPage(s, e)
            for i in range(start_page, end_page + 1):
                if s == 31 and e == 31: user_name_list += self.filterTierUser(i, s, e)[:5] # test 용도
                else: user_name_list += self.filterTierUser(i, s, e)
        else:
            for i in range(s, e):
                if s == 100 and e == 101: user_name_list += self.filterUser(i)[:5] # test 용도
                else: user_name_list += self.filterUser(i)

        for name in user_name_list:
            validation_df = pd.DataFrame({'index': [count], 'name': [name]})
            if self.validation.user_validation(validation_df):
                query = f"INSERT INTO userID VALUES ({count}, '{name}')"
                self.database.insertQuery(query)
                count += 1