from tinydb import TinyDB


def db_connector():
    """
    Connector to TinyDB
    :return:
    """
    db_name = "db_patterns.json"
    return TinyDB(db_name)


def db_get_all_documents():
    """
    Get all documents from TinyDB
    :return:
    """
    db = db_connector()
    return db.all()


def db_clean():
    """
    Clear TinyDB
    :return:
    """
    db = db_connector()
    db.truncate()
