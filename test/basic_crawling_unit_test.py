from solvedac_api.basic_crawling import basic_crawling
import unittest

'''
crawling
상속을 하기 위한 부모 클래스 생성
'''
class crawling:
    def __init__(self):
        self.bc = basic_crawling()

'''
basic_crawling
test_correct_problem: BOJ 1000번 문제를 가져오면 문제가 존재하므로 1이 나오는지 확인
test_not_correct_problem: BOJ 999번 문제를 가져오면 정보가 없으므로 0이 나오는지 확인
test_filter_user_list: 랭킹 200페이지에 있는 유저 100명의 정보를 제대로 가져오는지 확인
test_filter_user_empty_list: 랭킹 1페이지에 있는 유저는 실버5~플레1에 존재하지 않으니 빈 리스트를 반환하는지 확인
'''
class test_basic_crawling(unittest.TestCase, crawling):
    def test_correct_problem(self):
        existProblemValue = self.bc.filterProblem(1000)
        self.assertEqual(existProblemValue, 1)

    def test_not_correct_problem(self):
        notExistProblemValue = self.bc.filterProblem(999)
        self.assertEqual(notExistProblemValue, 0)

    def test_filter_user_list(self):
        filterUserList = self.bc.filterUser(200)
        self.assertEqual(len(filterUserList), 100)

    def test_filter_user_empty_list(self):
        emptyUserList = self.bc.filterUser(1)
        self.assertEqual(len(emptyUserList), 0)


if __name__ == "__main__":
    unittest.main()