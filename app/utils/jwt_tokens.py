# Import required libraries
import jwt
from time import time
from flask import current_app

# Function to generate user-specific training token for use with training campaign emails
def get_training_token(user_id, campaign_id, expires_in=604800):
    # Generate JWT token
    return jwt.encode(
        {'user_id': user_id,
         'campaign_id': campaign_id,
         'exp': time() + expires_in},
         current_app.config['SECRET_KEY'], 
         algorithm='HS256'
         )

# Function to verify user-specific training token for use with training campaign emails
def verify_training_token(token):
    # Decode JWT, verify decoded contents match format for encoding the original token
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id'], payload['campaign_id']
    # Skip functionality if JWT does not match encoding format
    except:
        return None, None