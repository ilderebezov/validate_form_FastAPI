from src.db_data import db_get_all_documents
import re
from datetime import datetime


def email_valid(email: str) -> bool:
    """
    validate email
    :param email: input email
    :return: is email valid
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    try:
        if re.fullmatch(regex, email):
            return True
    except:
        return False
    return False


def phone_valid(phone: str) -> bool:
    """
    validate phone number
    :param phone: input phone number
    :return: is phone number valid
    """
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    try:
        phone = phone.replace("+", "")
        phone = phone.replace(" ", "")
        if Pattern.match(phone):
            return True
    except:
        return False
    return False


def date_valid(date: str) -> bool:
    """
    validate date
    :param date: input date
    :return: is date valid
    """
    try:
        format_str = '%d.%m.%Y'
        datetime.strptime(date, format_str).date()
        return True
    except:
        try:
            format_str = '%Y-%m-%d'
            datetime.strptime(date, format_str).date()
            return True
        except:
            return False


def text_valid(text: str) -> bool:
    """
    validate input text
    :param text: input text
    :return: is text valid
    """
    return True


check_func = {
    "email": email_valid,
    "phone": phone_valid,
    "date": date_valid,
    "text": text_valid
}


def validate(validate_data: bytes) -> dict:
    """
    validate input request
    :param validate_data: input request
    :return:
    """
    validate_data_dict = {element.split('=')[0]: element.split('=')[1]
                          for element in validate_data.decode().split("&")}

    check_validate_data_dict = {"User_form": check_user_form(check_element=validate_data_dict)}

    for element in db_get_all_documents():
        check_validate_data_dict[element['pattern_name']] = check_fields(
            pattern={key: value for key, value in element.items() if "pattern" not in key},
            check_element=validate_data_dict)

    cor_form = set()
    for key_main, value_main in check_validate_data_dict.items():
        if key_main != "User_form":
            flat_list = [item for sublist in value_main.values() for item in sublist]
            if False not in flat_list:
                cor_form.add(key_main)
            for key_in, value_in in value_main.items():
                if not any(value_in) or value_in[1] is False:
                    check_validate_data_dict[key_main].update({key_in: None})
                else:
                    check_validate_data_dict[key_main].update({key_in: value_in[1]})
    cor_form_dict = {}
    if cor_form:
        for cor_key in cor_form:
            cor_form_dict[cor_key] = check_validate_data_dict[cor_key]
        max_key = max(cor_form_dict, key=lambda x: len(cor_form_dict[x]))
        return {"form name": max_key}
    return check_validate_data_dict["User_form"]


def check_user_form(check_element: dict) -> dict:
    """
    check init user data
    :param check_element: input user data
    :return: check type result
    """
    check_order_user = ["date", "phone", "email"]
    check_func_user = {
        "email": email_valid,
        "phone": phone_valid,
        "date": date_valid,
    }
    user_form = {}
    for key, value in check_element.items():
        is_key_used = False
        for element in check_order_user:
            if check_func_user[element](value) is True:
                user_form[key] = element
                is_key_used = True
                break
        if is_key_used is False and "text" not in key.lower():
            user_form[key] = "FAILD_TYPE"
        elif "text" in key.lower():
            user_form[key] = "text"
    return user_form


def check_fields(pattern: dict, check_element: dict) -> dict:
    """
    check fields in request
    :param pattern: input pattern
    :param check_element: input check element
    :return: check result
    """
    check_order = ["date", "phone", "email", "text"]
    check_rez = {}
    for element in check_order:
        pattern_keys = pattern.keys()
        pattern_key_check = [key for key in pattern_keys if element in key]
        check_element_key = [key for key in check_element if element in key]
        if pattern_key_check:
            for check_key in check_element_key:
                if check_key == pattern_key_check[0]:
                    if check_func[element](check_element[check_key]):
                        check_rez[pattern_key_check[0]] = [True, pattern[pattern_key_check[0]]]
                    else:
                        check_rez[pattern_key_check[0]] = [True, False]
                else:
                    if check_func[element](check_element[check_key]):
                        check_rez[pattern_key_check[0]] = [False, pattern[pattern_key_check[0]]]
                    else:
                        check_rez[pattern_key_check[0]] = [False, False]
    return check_rez
