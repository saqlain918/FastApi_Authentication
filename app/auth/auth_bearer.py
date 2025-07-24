from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime

SECRET_KEY = "99f83bd91551194a449598419c006ce4ccfa930694205d6ef187a602fabdf9df1ca63946d20c53781bc41425b3bbf60593549a263eb63bb47fb2d7e271f4135c065a44509922515cbd1e7bd504084b7f26e6047438fa3162f51eb747a706ad4fa0594e4afa72b7171f3b23ce6247d5c07c9d4f13ad07cf57911ada5eca02f934826d2f5278aec9085f631ca9aad2be583c12ad98e9166923abae635f3652ff79ac24e1b6dbbd28c368a57801fe320d454743a3103b22636dede169e00bc225960a7fb7966f4e40531da56c32868aad2def48269f0c264dea7b9be4218fe129551dc8e5394019c6ebfbee2a89f930351b2946396a7d022790be84d99365500857"
ALGORITHM = "HS256"




def decodeJWT(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = decoded_token.get("exp")
        if exp and datetime.utcnow().timestamp() < exp:
            return decoded_token
        return None
    except JWTError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

        return credentials.credentials

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = decodeJWT(jwtoken)
        return bool(payload)

