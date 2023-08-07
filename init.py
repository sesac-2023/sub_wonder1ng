from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from datetime import datetime
import time, re
from sub_email.get_email import send_mail
from sub_sql.get_sql import Get_sql

class Get_used_car_data():
    def __init__(self, db_secret_path, email_account_path) -> None:
        
        with open(db_secret_path) as f:
            res = dict(map(lambda x: x.replace('\n','').split('='), f.readlines()))
            for i, v in res.items():
                if v.isdigit(): res[i] = int(v)
        # MariaDB connector
        self.con = Get_sql(res)
        # DB에서 요청 사항 속성으로 저장
        self.request_list = self.con.get_request_data()
        # 요청 사항에서 알람 목록만 별도 저장
        self.alarm_time_list = self.request_list[1]
        # 요청 사항에서 column 별로 저장된 것에서 row 별로 변경
        self.request_list = list(zip(self.request_list[0], self.request_list[1], self.request_list[2], self.request_list[3], self.request_list[4], self.request_list[5], self.request_list[6], self.request_list[7]))
        # 이메일 계정 정보 속성으로 저장
        self.email_account_path = email_account_path
    
    # 중고차 매물 정보 크롤링 함수
    def crawling_used_car(self,request_list):
        # 첨부할 데이터 리스트
        self.send_email_data_list = []
        # 동일 시간대 알람이 1개일 경우를 대비하여 if 조건식 기재
        for target_addr, alarm_time, class_name, high_price, low_price, max_sales_count, brand_id, class_id in request_list if type(request_list)==list else [request_list]:

            base = 'https://www.kbchachacha.com'
            sub = '/public/search/list.empty?page={current_page}&sort=-orderDate&makerCode={brand_id}&classCode={class_id}&_pageSize=4&pageSize=5'
            my_datas=[]
            for current_page in range(1,max_sales_count//20+1):
                page = urlopen(base+sub .format (current_page=current_page, brand_id=brand_id, class_id=class_id))
                soup = BeautifulSoup(page, 'html.parser')
                try: 
                    soup = soup.find_all('div', attrs={"class":"list-in"})[2]
                    # url, id
                    url_list = [base+n for n in set([i['href'] for i in soup.find_all('a')])]
                    id_list = [int(n.split('carSeq=')[-1]) for n in url_list]
                    # 한 번만 실행. 불필요 제거
                    [n.decompose() for n in soup.find_all('span', class_='bbadge bbadge-service-small bbadge-stock')] 
                    model_pirce = [re.sub("(\n|\t|\r)", "", n.text) for n in soup.find_all('strong')]
                    # 실차주, 모델명, 가격
                    car_model=[]
                    price=[]
                    for n in range(0,len(model_pirce),2):
                        car_model.append(model_pirce[n])
                        price.append(int(model_pirce[n+1].split()[0].replace(',','').replace('만원','')))
                    # 출고일
                    birthday = [n.get_text() for n in soup.find_all('div', class_='first')]
                    # 주행거리, 지역
                    driven=[]
                    location=[]
                    driven_location = [n.get_text().split('\n')[1:3] for n in soup.find_all('div', class_='data-in')]
                    for distance, loc in driven_location:
                        driven.append(distance[:-2].replace(',',''))
                        location.append(loc)
                    my_datas.append(pd.DataFrame(zip(url_list, id_list, car_model, price, birthday, driven, location, [class_id]*len(id_list))))
                # 오류 발생 경우 지금까지 찾은 data만 첨부 발송
                except: break
            my_datas = pd.concat(my_datas)
            my_datas.columns=['url', 'id','model','price','released_day','driven_distance','location', 'model_code']
            # 크롤링 후 금액 조건 반영
            if high_price<999999:
                my_datas = my_datas[(my_datas.price<=high_price)&(my_datas.price>low_price)]

            # 파일명 이메일주소_모델명_날짜
            path = f'./{target_addr}_{class_name}_{datetime.today().strftime("%Y%m%d")}.xlsx'
            my_datas.to_excel(path, index=False)
            self.send_email_data_list.append([target_addr, alarm_time, class_name, high_price, low_price, path, len(my_datas)])
            return self.send_email_data_list
    
    # '시' 기준으로 정보 알림 발송. '분'의 경우 크롤링 시간으로 인한 누락 발생 위험.
    def run_alarm(self):
        while True:
            # 실행시 현재 시각과 동일한 '시'일 경우 메일 발송
            for i in range(len(self.alarm_time_list)):
                if self.alarm_time_list[i]==datetime.today().strftime("%H")+":00":
                    send_mail(self.email_account_path, self.crawling_used_car(self.request_list[i]))
            # 각 '시'의 정각에 맞춰 발송
            if datetime.today().strftime("%M")=="00":
                time.sleep(3600)
            else:
                time.sleep((60-int(datetime.today().strftime("%M")))*60)