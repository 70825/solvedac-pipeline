from database.postgresql import postgresql
from kafka_file.producer import producer
import requests
import time
import json


class adv_crawling:

    def __init__(self):
        self.database = postgresql()
        self.producer = None


    '''
    문제 정보 가져오기: getInfoProblem
    1. 문제 번호
    2. 문제 이름
    3. 문제 난이도
    4. 문제 유형
    -> Kafka topic: problemInfo로 전송
    '''
    def getInfoProblem(self, number):
        url = f"https://solved.ac/api/v3/problem/show?problemId={number}"
        r_problem = requests.get(url)

        if r_problem.status_code == 404: return

        while r_problem.status_code != requests.codes.ok:
            time.sleep(30)
            r_problem = requests.get(url)

        info = json.loads(r_problem.content.decode('utf-8'))

        # 문제 번호
        problemId = info['problemId']

        # 문제 이름
        if len(info['titles']) == 1: title = info['titles'][0]['title']
        else:
            for i in range(len(info['titles'])):
                if info['titles'][i]['language'] == 'ko':
                    title = info['titles'][i]['title']

        # 문제 난이도
        level = info['level']

        # 문제 유형
        tag = []
        for i in range(len(info['tags'])):
            for j in range(len(info['tags'][i]['displayNames'])):
                if info['tags'][i]['displayNames'][j]['language'] == 'ko':
                    tag.append(info['tags'][i]['displayNames'][j]['name'])

        # producer에 전달
        data = {
            'problemId': problemId,
            'titles': title,
            'level': level,
            'tag': tag
        }

        return data


    '''
    유저 기본 정보 가져오기: getBasicInfoUser
    1. 유저 닉네임
    2. 유저 solved.ac 티어
    3. 유저가 풀은 문제 수
    '''
    def getBasicInfoUser(self, name):
        url = f"https://solved.ac/api/v3/user/show?handle={name}"
        r_user = requests.get(url)
        if r_user.status_code == 404: return

        while r_user.status_code != requests.codes.ok:
            time.sleep(30)
            r_user = requests.get(url)

        info = json.loads(r_user.content.decode('utf-8'))

        # 유저 닉네임
        handle = info['handle']

        # 유저 티어
        tier = info['tier']

        # 유저가 풀은 문제 수
        solvedCount = info['solvedCount']

        # 반환값
        data = {
            'handle': handle,
            'tier': tier,
            'solvedCount': solvedCount
        }

        return data


    '''
    유저가 풀은 문제가 page당 100문제씩 있는 것을 처리하는 함수: getSolvedProblemPageFromUser
    유저가 풀은 문제 번호 가져오기: getSolvedProblemFromUser
    1. 문제 번호 리스트
    '''
    def getSolvedProblemPageFromUser(self, name):
        url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{name}%26tier%3Ab5..g1"
        r_pages = requests.get(url)

        while r_pages.status_code != requests.codes.ok:
            time.sleep(30)
            r_pages = requests.get(url)

        info = json.loads(r_pages.content.decode('utf-8'))
        pages = (info['count'] // 100) + 1

        data = {
            'solvedProblems': []
        }

        for page in range(1, pages + 1):
            data['solvedProblems'].append(self.getSolvedProblemFromUser(name, page))

        return data


    def getSolvedProblemFromUser(self, name, page):
        url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{name}%26tier%3Ab5..g1&sort=level&direction=asc&page={page}"
        r_solved_problem = requests.get(url)

        while r_solved_problem.status_code != requests.codes.ok:
            time.sleep(30)
            r_solved_problem = requests.get(url)

        info = json.loads(r_solved_problem.content.decode('utf-8'))

        solved_problem_number = []
        for i in range(len(info['items'])):
            solved_problem_number.append(info['items'][i]['problemId'])

        # 리스트로 반환하고, getSolvedProblemPageFromUser에서 dict로 변환
        return solved_problem_number

    '''
    kafka proucer 연결
    '''
    def connectKafkaProducer(self):
        self.producer = producer()

    '''
    문제 정보를 kafka에 보내기
    '''
    def sendProducerInfoProblem(self, data):
        self.connectKafkaProducer()
        self.producer.send("problemInfo", data)


    '''
    유저 정보를 kafka에 보내기
    '''
    def sendProducerInfoUser(self, data):
        self.connectKafkaProducer()
        self.producer.send("userInfo", data)


    '''
    postgresql에서 문제 번호를 찾고, 문제에 대한 정보를 kafka에 전송
    * 유저가 풀은 문제 리스트가 postgresql에 저장한 시점과 다를 경우가 존재함
    * 이런 경우 postgrsql에 있는 번호만 나중에 처리하려고 저장한 것임
    '''
    def sendProblemNumber(self):
        query = "SELECT num FROM problemID"
        problem_number = self.database.readQuery(query=query)

        for p_num in problem_number:
            data = self.getInfoProblem(p_num[0])
            self.sendProducerInfoProblem(data)

    '''
    postgresql에서 저장된 유저 이름을 찾고, 유저에 대한 정보를 kafka에 전송
    '''
    def sendUserName(self):
        query = "SELECT name FROM userID"
        user_name = self.database.readQuery(query=query)

        for u_name in user_name:
            user_data = {}
            user_data.update(self.getBasicInfoUser(u_name[0]))
            user_data.update(self.getSolvedProblemPageFromUser(u_name[0]))
            self.sendProducerInfoUser(user_data)