# Settings Of Prod Env
from config.settings import *

DEBUG = False

# Salesforce 연결 설정
SALESFORCE_SETTINGS = {
    'USERNAME': 'your_prod_username',
    'PASSWORD': 'your_prod_password',
    'TOKEN': 'your_prod_token',
    'Sandbox': False,  # 프로덕션 환경에서는 False로 설정
}

#syh2916_onboarding_exam@kusrc.co.kr
#@aa1149118
#https://kuresearchcenter-e-dev-ed.develop.my.salesforce.com