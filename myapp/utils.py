import jwt
from django.conf import settings

def generate_jwt_token(certificate_id):
    payload = {'certificate_id': certificate_id}
    token = jwt.encode(payload, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithm=settings.JWT_AUTH['JWT_ALGORITHM'])
    return token