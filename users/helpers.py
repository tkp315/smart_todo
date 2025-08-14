import datetime
from core.config.env_config import ENV_VARIABLES
import jwt
def generate_token(is_refresh,user):
 
    token_payload = {
            "id":str(user.id),
        "exp":datetime.datetime.utcnow()+datetime.timedelta(hours=ENV_VARIABLES['ACCESS_TOKEN_EXPIRY']) if is_refresh==False else datetime.datetime.utcnow()+datetime.timedelta(days=ENV_VARIABLES['REFRESH_TOKEN_EXPIRY'])
    }
    secret = ENV_VARIABLES['ACCESS_TOKEN_SECRET'] if is_refresh==False else ENV_VARIABLES['REFRESH_TOKEN_SECRET']

    token = jwt.encode(token_payload,secret,algorithm='HS256')

    return token

   

