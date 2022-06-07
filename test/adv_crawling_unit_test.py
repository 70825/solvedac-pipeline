from solvedac_api.adv_crawling import adv_crawling
import unittest

'''
test_adv_crawling

test_correct_info_problem: 1000번 문제를 가지고와서 1000, A+B, 브론즈5, 유형들이 정확한지 확인
test_not_exist_info_problem: 999번 문제는 존재하지 않으니 None을 반환하는지 확인
test_correct_info_user: hello70825 유저의 정보가 정확한지 확인
test_not_exist_info_user: a가 50번 반복되는 aaaaaa... 유저는 존재하지 않으므로 None을 반환하는지 확인 
test_solved_problem_from_user: hello70825 유저가 풀은 문제의 번호가 1페이지에 100문제 존재하는지 확인
'''
class test_adv_crawling(unittest.TestCase):
    def test_correct_info_problem(self):
        ac = adv_crawling()
        data = ac.getInfoProblem(1000)
        self.assertEqual(data['problemId'], 1000)
        self.assertEqual(data['titles'], 'A+B')
        self.assertEqual(data['level'], 1)
        self.assertEqual(data['tag'], ['구현', '사칙연산', '수학'])

    def test_not_exist_info_problem(self):
        ac = adv_crawling()
        data = ac.getInfoProblem(999)
        self.assertIsNone(data)

    def test_correct_info_user(self):
        ac = adv_crawling()
        data = ac.getBasicInfoUser("hello70825")
        self.assertEqual(data['handle'], 'hello70825')
        self.assertEqual(data['tier'], 21)
        self.assertEqual(data['solvedCount'], 1910)

    def test_not_exist_info_user(self):
        ac = adv_crawling()
        data = ac.getBasicInfoUser("a"*50)
        self.assertIsNone(data)

    def test_solved_problem_from_user(self):
        ac = adv_crawling()
        data =ac.getSolvedProblemFromUser('hello70825', 1)
        self.assertEqual(len(data), 100)



if __name__  == "__main__":
    unittest.main()