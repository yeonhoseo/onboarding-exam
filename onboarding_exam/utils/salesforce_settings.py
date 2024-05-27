import os
import requests
from dotenv import load_dotenv
from simple_salesforce import Salesforce,SalesforceAuthenticationFailed 
from .logger import Logger
DOT_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'.env')

#TODO : print -> Logger 로 변경 필요 
class SalesforceConnectionManager :
    def __init__(self,env : str ) : 
        load_dotenv(DOT_FILE_PATH)
        
        self._SALESFORCE_USERNAME : str = os.getenv("SALESFORCE_USERNAME")
        self._SALESFORCE_PASSWORD : str = os.getenv("SALESFORCE_PASSWORD")
        self._SALESFORCE_SECURITY_TOKEN : str = os.getenv("SALESFORCE_SECURITY_TOKEN")
        self._SALESFORCE_CONSUMER_KEY : str = os.getenv("SALESFORCE_CONSUMER_KEY")
        self._SALESFORCE_CONSUMER_SECRET : str = os.getenv("SALESFORCE_CONSUMER_SECRET")
        self._SALESFORCE_CALLBACK_URL : str = os.getenv("SALESFORCE_CALLBACK_URL")
        self.sf = None
        self.env = env
        self.session = requests.Session()
        
        self.logger = Logger(logger_name='dev')
        

    def is_valid_token(self) -> bool :
        if self._SALESFORCE_SECURITY_TOKEN : 
            return True
        else : 
            return False
    
    def connect(self) -> Salesforce :
        if self.is_valid_token() :
            _is_sandbox = True if self.env.lower() == 'prod' else False
            try : 
                if _is_sandbox : 
                    self.sf = Salesforce(username=self._SALESFORCE_USERNAME,
                        password=self._SALESFORCE_PASSWORD, 
                        security_token=self._SALESFORCE_SECURITY_TOKEN,
                        session=self.session)
                else : 
                    self.sf = Salesforce(username=self._SALESFORCE_USERNAME,
                        password=self._SALESFORCE_PASSWORD, 
                        security_token=self._SALESFORCE_SECURITY_TOKEN,
                        session=self.session)
                    #,domain='test'
                print("Successfully connected to Salesforce")
                self.logger.info("Successfully connected to Salesforce")
                return self.sf
            except SalesforceAuthenticationFailed as e :
                self.logger.error(f"Salesforce Authentication Failure : {e}")
            except Exception as e : 
                self.logger.error(f"Salesforce Authentication Failure : {e}")
            
    def request_salesforce_token(self) : 
        if self.is_valid_token() :
            data = {
                'grant_type': 'authorization_code',
                'client_id': self._SALESFORCE_CONSUMER_KEY,
                'client_secret': self._SALESFORCE_CONSUMER_SECRET,
                'username': self._SALESFORCE_USERNAME,
                'password': self._SALESFORCE_PASSWORD
            }
                      
            response = requests.post(self._token_url, data=data)
            token_data = response.json()
            print(token_data)
            self.access_token = token_data['access_token']

            with open(DOT_FILE_PATH,'r+') as f : 
                lines = f.readlines()
                f.seek(0)
                for idx, line in enumerate(lines) : 
                    if line.startswith('SALESFORCE_SECURITY_TOKEN') : 
                        lines[idx] = f"SALESFORCE_SECURITY_TOKEN = \'{self.access_token}\'\n"
                f.truncate()
                f.writelines(lines)

    def refresh_salesfroce_token(self) :
        pass 
