import jwt
from time import time
from flask import current_app

def get_training_token(user_id, campaign_id, expires_in=604800):
    return jwt.encode(
        {'user_id': user_id,
         'campaign_id': campaign_id,
         'exp': time() + expires_in},
         current_app.config['SECRET_KEY'], 
         algorithm='HS256'
         )

def verify_training_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id'], payload['campaign_id']
    except:
        return None, None