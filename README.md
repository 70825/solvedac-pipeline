# 🧩solvedac-pipeline
- solved.ac API를 사용한 간단한 데이터 파이프라인을 제작
- 특정 티어 구간에 속한 유저 정보 혹은 특정 랭킹 페이지 구간에 속하는 유저 정보를 데이터베이스에 저장
- 특정 문제 구간에 속한 문제 정보를 데이터베이스에 저장

## 🛠️ 데이터 파이프라인
![image](https://user-images.githubusercontent.com/79046106/170855003-bd66c67f-8a2b-447f-aaf4-a96de8ddd39b.png)

## ⚙ 데이터 파이프라인 설명
- API를 사용하여 특정 시간에서 아래 데이터를 가져와 PostgreSQL에 저장한다.
  - 브론즈5 ~ 골드1 티어의 문제 번호
  - 실버5 ~ 플레티넘1 티어의 유저 닉네임
- PostgreSQL에 저장된 유저 이름, 문제 번호를 API에 적용하여 아래 데이터를 Kafka Producer에 전달한다.
  - problemInfo: (문제 번호, 문제 이름, 문제 유형)
  - userInfo: (유저 닉네임, 유저 티어, 유저가 풀은 문제 수, 유저가 풀은 문제 번호)
- Kafka Consumer를 통해 MongoDB에 저장한다.
