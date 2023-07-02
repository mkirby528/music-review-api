import jwt
def decode(jwt):
    return jwt.decode(jwt, options={"verify_signature": False})