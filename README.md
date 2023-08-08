# 주제: 중고차 최신 매물 매일 알림
## 사용 기술 및 라이브러리  
    - Python 3.10.11  
        - Beautiful Soup, pandas, pymysql  
    - MariaDB  
## 패키지 구조
  
  ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/0fb766cd-a931-4ebc-9b33-63283081c326)

## 프로젝트 설명
### 1. 목표  
  
매일 KB차차차 사이트에서 원하는 매물과 예산 금액 안에서 최신 게시물을 지정 개수만큼 메일로 송부(.xlsx)하기  
kb차차차 사이트 url: https://www.kbchachacha.com/  

### 2. 과정  
  
  1) get_kb_codes.ipynb으로 KB차차차 사이트의 브랜드와 클래스(차 모델) 정보 크롤링.
  2) MariaDB로 로컬에서 DB 및 테이블 생성(하단 이미지 참조)  
    2-1) 테이블 구조  
    ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/79d617b9-5b94-47cf-89c8-16d2b4ff48c1)  
    2-2) ERD  
    ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/b5509ba5-f8a9-4970-8d2b-da058ae5c2a4)  
  3) 로컬 DB에 크롤링 정보 저장.
  4) 클래스(혹은 함수)를 통해 알림 요청 정보 DB에서 관리
  5) 매일 지정 시간마다 이메일로 매물 정보(.xlsx) 첨부하여 메일 발송  
  
### 3. 발송 결과  
  1. 메일 이미지
  ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/afedf0f5-06e3-409e-b7f8-4578647f5d8d)
    
  2. 엑셀 이미지
  ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/e540c11f-d716-455f-aafe-3426f5c74c59)
