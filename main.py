'''
1. basic_crawling을 통해 유저 이름, 문제 번호를 postgresql에 저장함
2. adv_crawling을 통해 유저 정보, 문제 정보를 kafka producer로 전달
3. kafka producer는 problemInfo topic과 userInfo로 메시지를 저장
4. kafka consumer를 통해 메시지를 받아 mongodb에 저장
'''

from solvedac_api.basic_crawling import basic_crawling
from solvedac_api.adv_crawling import adv_crawling
from kafka_file.consumer import consumer_problem, consumer_user

print('basic_crawling start..')
basic_crawling = basic_crawling()
basic_crawling.insertProblemNumber()
basic_crawling.insertUserName()
print('basic_crawling end..')

print('adv_crawling start..')
adv_crawling = adv_crawling()
adv_crawling.sendProblemNumber()
adv_crawling.sendUserName()
print('adv_crawling end..')

print('saving mongodb_problem start..')
consumer1 = consumer_problem()
consumer1.saveData()

print('saving mongodb_user start..')
consumer2 = consumer_user()
consumer2.saveData()

print('finish!')