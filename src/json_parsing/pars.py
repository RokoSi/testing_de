from src.json_parsing.model.users import Users


def pars_user(dict_param: dict):
    users = [Users(**user) for user in dict_param]
    return users

