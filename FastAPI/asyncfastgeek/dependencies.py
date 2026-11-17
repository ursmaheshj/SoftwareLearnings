from fastapi import HTTPException, status

def verify_token(token: str):
    if token!="1234":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Does not have proper Access")
    return token
