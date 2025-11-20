from fastapi import FastAPI, Request, Response, HTTPException
from typing import Callable, Awaitable
from .utils.authUser import AuthUser
import time, json, logging

logger = logging.getLogger('fastapi')


async def prepare_headers(request:Request):
    headers = dict(request.headers)
    try:
        headers = dict(request.scope['headers'])
        #headers[b'user-data'] = b'query_id=AAHX2ec5AAAAANfZ5zn4XdMA&user=%7B%22id%22%3A971495895%2C%22first_name%22%3A%22%D0%A1%20%D0%B0%20%D1%88%20%D0%B0%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22crymans%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FvFbVYnhG2nFxhrRcZQupOywRrxTbLcWcmixGxd1xa8I.svg%22%7D&auth_date=1759819713&signature=BJJUeEdOSMjuTCfg0gglQZw1DixnNgrcTBVjitjd0B0EwfzReaVBcFFON1sRNjwYjB0azP4wYx78JD-0ewo4DA&hash=cfe99fc8883599d4f3aaf4a6d7b21f241c8e234d42f2ed068f8bf84bda4a3156&start_param=971495895'
        res = await AuthUser.parse_user_data(headers[b'user-data'].decode('utf-8'), request.client.host)
        headers[b'user-data'] = bytes(json.dumps(res), encoding='utf-8')
        request.scope['headers'] = [(k, v) for k, v in headers.items()]
        return request
    except Exception as e:
        logger.error(f'Middleware error: {e}')
        raise HTTPException(401, 'User-Data error')
    finally:
        return request

async def add_proccess_time(request:Request, call_next:Callable[[Request], Awaitable[Response]]):
    try:
        before = time.time()
        request = await prepare_headers(request)
        response = await call_next(request)
        after = time.time() - before
        response.headers['X-Time-delta'] = f"{after:.2f}"
        return response
    except Exception as e:
        logger.error(f'add_proccess_time error: {e}')
        raise HTTPException(401, f'User Error')
        pass

def register_middleware(app:FastAPI):
    app.middleware('http')(add_proccess_time)