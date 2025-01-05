from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime

def is_token_expired(request) -> bool:
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return True  # No authorization header found, treat it as expired or unauthorized

    access_token = auth_header[len('Bearer '):]

    try:
        token = AccessToken(access_token)
        print("authoooooo", token)
        if token['exp'] < datetime.utcnow().timestamp():
            return True
        
        return False
    
    except AuthenticationFailed:
        print("Token expired or invalid")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return True