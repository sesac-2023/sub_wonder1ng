# 주제: 중고차 최신 매물 매일 알림
## 사용 기술 및 라이브러리  
    - Python 3.10.11  
        - Beautiful Soup, pandas, pymysql  
    - MariaDB  
## 패키지 구조
  

  ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/c62e3cd9-60a6-40f7-ac69-6522c25e66b5)


## 프로젝트 설명
### 1. 목표  
  
매일 KB차차차 사이트에서 원하는 매물과 예산 금액 안에서 최신 게시물을 지정 개수만큼 메일로 송부(.xlsx)하기  
kb차차차 사이트 url: https://www.kbchachacha.com/  

### 2. 과정  
  
  1) get_kb_codes.ipynb으로 KB차차차 사이트의 브랜드와 클래스(차 모델) 정보 크롤링.
  2) MariaDB로 로컬에서 DB 및 테이블 생성(하단 이미지 참조)  
  ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/c631ed54-dbd4-4d21-98b7-1272233447c1)
  3) 로컬 DB에 크롤링 정보 저장.
  4) 클래스(혹은 함수)를 통해 알림 요청 정보 DB에서 관리
  5) 매일 지정 시간마다 이메일로 매물 정보(.xlsx) 첨부하여 메일 발송  
  
### 3. 발송 결과  
  1. 메일 이미지
  ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/47fc8b4a-d3eb-4266-ac6f-618ecbbabdd9)
    
  2. 엑셀 이미지
  ![image](https://github.com/sesac-2023/sub_wonder1ng/assets/124233972/b71f94e9-7cf9-4cf5-b780-14570b62725a)
