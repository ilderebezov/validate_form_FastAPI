from fastapi.testclient import TestClient

from src import routes as api_routes
from src.server import app

app.include_router(api_routes.router)

client = TestClient(app)


def test_check_form00_01():
    """
    correct user form for pattern name Form_00
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_email=test@gmail.com&user_phone=+7123 123 12 12&user_date=01.01.2023&user_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"form name": "Form_00"}


def test_check_form00_02():
    """
    non-correct user email form for pattern name Form_00
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_email=test-gmail.com&user_phone=+7123 123 12 12&user_date=01.01.2023&user_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"user_date": "date",
                               "user_phone": "phone",
                               "user_email": "FAILD_TYPE",
                               "user_text": "text"}


def test_check_form00_03():
    """
    non-correct user phone form for pattern name Form_00
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_email=test@gmail.com&user_phone=123 123 12 12&user_date=01.01.2023&user_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"user_date": "date",
                               "user_phone": "FAILD_TYPE",
                               "user_email": "email",
                               "user_text": "text"}


def test_check_form00_04():
    """
    non-correct user date form for pattern name Form_00
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_email=test@gmail.com&user_phone=+7 123 123 12 12&user_date=01_01_2023&user_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"user_date": "FAILD_TYPE",
                               "user_phone": "phone",
                               "user_email": "email",
                               "user_text": "text"}


def test_check_form01_00():
    """
    correct user form for pattern name Form_01
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_work_email=test@gmail.com&user_work_phone=+7 123 123 12 12&user_work_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"form name": "Form_01"}


def test_check_form01_01():
    """
    non-correct user form for pattern name Form_01
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_work_email=test@gmail.com&user_workphone=+7 123 123 12 12&user_work_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"user_work_email": "email",
                               "user_workphone": "phone",
                               "user_work_text": "text"}


def test_check_form02_00():
    """
    correct user form for pattern name Form_02
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_work_date=01.01.2023&user_work_email=test@gmail.com&user_work_phone=+7 123 123 12 12&user_work_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"form name": "Form_02"}


def test_check_form02_01():
    """
    non-correct user form for pattern name Form_02
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_date=01.01.2023&userwork_date=01.01.2023&user_workemail=test@gmail.com&user_work_phone=+7 123 123 12 12&user_work_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"user_date": "date",
                               "userwork_date": "date",
                               "user_workemail": "email",
                               "user_work_phone": "phone",
                               "user_work_text": "text"}


def test_check_form02_02():
    """
    non-correct user form for pattern with FAILD_TYPE fields
    :return:
    """
    response = client.post(
        "/get_form/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="user_date=01.01.2023&userwork_date=01.01-2023&user_workemail=test-gmail.com&user_work_phone=123-123-12-12&user_work_text=test text"
    )
    assert response.status_code == 200
    assert response.json() == {"user_date": "date",
                               "userwork_date": "FAILD_TYPE",
                               "user_workemail": "FAILD_TYPE",
                               "user_work_phone": "FAILD_TYPE",
                               "user_work_text": "text"}
