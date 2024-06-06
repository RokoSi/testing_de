import json
from pprint import pprint

from src.json_parsing.get_user import get_users_url
from src.json_parsing.model.cities import Cities
from get_user import get_users_url
from src.json_parsing.model.users import Users


def pars_user(dict_param: dict):
    users = [Users(**user) for user in dict_param["results"]]






if __name__ == "__main__":
    kkk = get_users_url(2)
    pprint(kkk)
    pars_user(kkk)
