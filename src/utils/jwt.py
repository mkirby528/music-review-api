import jwt
def decode(token):
    return jwt.decode(token, options={"verify_signature": False})