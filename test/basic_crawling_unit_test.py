from solvedac_api.basic_crawling import basic_crawling
import unittest

'''
basic_crawling
test_correct_problem: BOJ 1000번 문제를 가져오면 문제가 존재하므로 1이 나오는지 확인
test_not_correct_problem: BOJ 999번 문제를 가져오면 정보가 없으므로 0이 나오는지 확인
test_filter_user_list: 랭킹 200페이지에 있는 유저 100명의 정보를 제대로 가져오는지 확인
test_filter_user_empty_list: 랭킹 1페이지에 있는 유저는 실버5~플레1에 존재하지 않으니 빈 리스트를 반환하는지 확인
'''
class test_basic_crawling(unittest.TestCase):
    def test_correct_problem(self):
        bc = basic_crawling()
        existProblemValue = bc.filterProblem(1000)
        self.assertTrue(existProblemValue)

    def test_not_correct_problem(self):
        bc = basic_crawling()
        notExistProblemValue = bc.filterProblem(999)
        self.assertFalse(notExistProblemValue)

    def test_filter_user_list(self):
        bc = basic_crawling()
        filterUserList = bc.filterUser(200)
        self.assertEqual(len(filterUserList), 100)

    def test_filter_user_empty_list(self):
        bc = basic_crawling()
        emptyUserList = bc.filterUser(1)
        self.assertEqual(len(emptyUserList), 0)


if __name__ == "__main__":
    unittest.main()