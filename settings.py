import os
import datetime
import pathlib
from dotenv import load_dotenv
from dataclasses import dataclass


BASE_DIR = pathlib.Path(__file__).parent    

CMDS_DIR =  BASE_DIR / "commands"

start_time = datetime.time()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@dataclass 
class Config:
    announce = 0
    voting = 0
    duration = 0
    role = ""
    
    def configured(self):
        not_setup_channels = [attr for attr, value in self.__dict__.items() if (value == 0 or value == "")]
        return not_setup_channels
    