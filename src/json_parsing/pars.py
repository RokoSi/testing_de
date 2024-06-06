from src.json_parsing.model.users import Users


def pars_user(dict_param: dict):
    try:

        users = [Users(**user) for user in dict_param]
        return users

    except (TypeError, KeyError, ValueError) as e:
        print(f"Ошибка {e}")
        return False
