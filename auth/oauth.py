
from fastapi import Depends,HTTPException, status
import token_controller.jwtToken as token_checker 

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_checker.verify_token(token,credentials_exception)