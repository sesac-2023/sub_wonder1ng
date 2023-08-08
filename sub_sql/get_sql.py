import pymysql
import pandas as pd

class Get_sql():
    def __init__(self, res) -> None:
        self.con = pymysql.connect(**res)

    def insert_request(self, target_addr: str, alarm_time:str, brand_name:str, car_model:str, high_price:int=999999, low_price:int=0, max_sales_count:int=500) -> None:
        with self.con.cursor() as cur:
            cur.execute(f'select brand_id from brand where brand_name=\'{brand_name}\'')
            brand_code = cur.fetchone()[0]
            cur.execute(f'insert into user_requests values(\'{target_addr}\', \'{alarm_time}\', {brand_code}, \'{car_model}\', {high_price}, {low_price}, {max_sales_count})')
        self.con.commit()

    def select_request(self) -> pd.DataFrame:
        with self.con.cursor() as cur:
            cur.execute(f'select * from user_requests')
            result = cur.fetchall()
        return pd.DataFrame(result)

    def delete_request(self, target_addr: str, car_model:str) -> None:
        with self.con.cursor() as cur:
            cur.execute(f'delete from user_requests where target_addr=\'{target_addr}\' and class_name=\'{car_model}\'')
        self.con.commit()

    def get_request_data(self) -> [list, list, list, list, list, list, list]:
        with self.con.cursor() as cur:
            cur.execute(f'select r.target_addr, r.alarm_time, r.class_name, r.high_price, r.low_price, r.sales_count, c.brand_id, c.class_id from user_requests r, car_class c where r.class_name=c.class_name')
            result = cur.fetchall()
        target_addr_list = []
        alarm_time_list = []
        class_name_list = []
        high_price_list = []
        low_price_list = []
        sales_count_list = []
        brand_id_list = []
        class_id_list = []
        for v1, v2, v3, v4, v5, v6, v7, v8 in result:
            target_addr_list.append(v1)
            alarm_time_list.append(v2)
            class_name_list.append(v3)
            high_price_list.append(v4)
            low_price_list.append(v5)
            sales_count_list.append(v6)
            brand_id_list.append(v7)
            class_id_list.append(v8)
        return [target_addr_list, alarm_time_list, class_name_list, high_price_list, low_price_list, sales_count_list, brand_id_list, class_id_list]
    
    def insert_brand(self, brand_code_list: list) -> None:
        with self.con.cursor() as cur:
            for brand_code, brand_name in brand_code_list:
                try:
                    cur.execute(f'insert into brand values(\'{brand_name}\', {brand_code}')
                    self.con.commit()
                except:
                    print(f'이미 입력되어 있습니다. brand_code: {brand_code}, brand_name: {brand_name}')

    def insert_class(self, class_code_list: list) -> None:
        with self.con.cursor() as cur:
            for brand_code, class_name, class_code in class_code_list:
                try:
                    cur.execute(f'insert into car_class values({brand_code}, \'{class_name}\', {class_code}')
                    self.con.commit()
                except:
                    print(f'이미 입력되어 있습니다. class_code: {class_code}, class_name: {class_name}')