from functools import partial

from fastapi import APIRouter
from fastapi import Request
from fastapi.concurrency import run_in_threadpool

from src.validate_form import validate

router = APIRouter()


@router.post("/get_form")
async def read_root(request: Request):
    """
    end point for check input form
    :param request:
    :return:
    """
    try:
        body = await request.body()
        return await run_in_threadpool(partial(validate, validate_data=body))
    except Exception as error:
        return {"Wrong requests": "Please, update your request and try again"}
