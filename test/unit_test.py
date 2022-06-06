from solvedac_api.basic_crawling import basic_crawling
import unittest


'''
basic_crawling
test_correct_problem: BOJ 1000번 문제를 가져오면 문제가 존재하므로 1이 나오는지 확인
test_uncorrect_problem: BOJ 999번 문제를 가져오면 정보가 없으므로 0이 나오는지 확인
test_filter_user_list: 랭킹 200페이지에 있는 유저 100명의 정보를 제대로 가져오는지 확인
'''
class test_basic_crawling(unittest.TestCase):
    def test_correct_problem(self):
        bc = basic_crawling()
        existProblemValue = bc.filterProblem(1000)
        self.assertEqual(existProblemValue, 1)

    def test_uncorrect_problem(self):
        bc = basic_crawling()
        notExistProblemValue = bc.filterProblem(999)
        self.assertEqual(notExistProblemValue, 0)

    def test_filter_user_list(self):
        bc = basic_crawling()
        filterUserList = bc.filterUser(200)
        self.assertEqual(len(filterUserList), 100)


if __name__ == "__main__":
    unittest.main()