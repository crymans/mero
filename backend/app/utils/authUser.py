from fastapi import HTTPException
import hmac, hashlib, json
from urllib.parse import parse_qs, unquote
from app.config import settings
import logging
import jwt, time

logger = logging.getLogger('fastapi')


class AuthUser:
    @classmethod
    async def is_bot(cls, user_data:dict):
        try:
            if user_data.get('is_bot') != None:
                return user_data['is_bot'] == True
            return False
        except Exception as e:
            logger.warning(f"AuthUser is_bot error: {e}")
            raise HTTPException(402)
        
    @classmethod
    async def __check_hash(cls, user_data:str):
        try:
            data_check_string = user_data
            data_check_arr = data_check_string.split('&')
            needle = 'hash='
            hash_item = ''
            telegram_hash = ''
            for item in data_check_arr:
                if item[0:len(needle)] == needle:
                    telegram_hash = item[len(needle):]
                    hash_item = item

            data_check_arr.remove(hash_item)
            data_check_arr.sort()
            data_check_string = "\n".join(data_check_arr)
            secret_key = hmac.new("WebAppData".encode(), settings.BOT_TOKEN.encode(),  hashlib.sha256).digest()
            calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
            return calculated_hash == telegram_hash
        except Exception as e:
            raise HTTPException(401)
    
    @classmethod
    async def parse_user_data(cls, user:str, ip:str=''):
        try:
            user_unquote = unquote(user, encoding='utf-8')
            au = await cls.__check_hash(user_unquote)
            print(au)
            if not au:
                raise Exception()
            # logger.info(user)
            params_before = parse_qs(user_unquote)
            params = unquote(params_before['user'][0])
            user_dict = json.loads(params)
            # is_bot =  await cls.is_bot(user_dict)
            # if is_bot:
            #     raise Exception()

            return user_dict
        except Exception as e:
            logger.warning(f"AuthUser error: {e}")
            raise HTTPException(402)

    @classmethod
    async def create_jwt(cls, data:dict):
        try:
            data['exp'] = time.time() + 86400 * 21
            token = jwt.encode(payload=data, key=settings.JWT_TOKEN, algorithm='HS256')
            return token
        except Exception as e:
            logger.warning(f"AuthUser jwt_create: {e}")
            raise HTTPException(402)

    @classmethod
    async def decode_jwt(cls, token:str):
        try:
            data = jwt.decode(token, settings.JWT_TOKEN, algorithms='HS256')
            return data
        except Exception as e:
            logger.warning(f"AuthUser jwt_encode: {e}")
            raise HTTPException(402)