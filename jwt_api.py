import jwt

clave_secreta = "mi_clave_secreta"
def generar_jwt(datos):
    payload = {"datos": datos}

    jwt_token = jwt.encode(payload, clave_secreta, algorithm='HS256')

    return jwt_token

def verificar_jwt(jwt_token):
    try:
        payload = jwt.decode(jwt_token, clave_secreta, algorithms=['HS256'])
        return payload['datos']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None