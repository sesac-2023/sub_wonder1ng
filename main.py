from init import Get_used_car_data
import os
os.chdir(__file__.replace(__file__.split('\\')[-1],''))

# db계정 정보와 이미지 계정정보 파일 경로
tmp = Get_used_car_data('./db_secret', './email_secret')
# 실행 코드
tmp.run_alarm()