from tinydb import TinyDB, Query


def db_connector():
    db_name = "db_patterns.json"
    return TinyDB(db_name)


def db_insert():
    db = db_connector()
    db.insert({'pattern_name': "From_01", "user_work_email": "email", "user_work_phone": "phone",
               "user_work_from_data": "data", "user_work_text": "str"})


def db_get_all_documents():
    db = db_connector()
    return db.all()


def db_search(search_str: str):
    Search_val = Query()
    db = db_connector()
    print(db.search(Search_val.type == search_str))


def db_update():
    db = db_connector()
    Fruit = Query()
    db.update({'count': 10}, Fruit.type == 'apple')


def db_clean():
    db = db_connector()
    db.truncate()
