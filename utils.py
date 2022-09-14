from dataclasses import dataclass
import random

@dataclass
class User:
    username: str
    psw_hash: str
    rank: str

def generate_rd_n():
    '''This method is used to refresh the css'''
    return str(random.random()+random.randint(0,100))
