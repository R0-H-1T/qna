from fastapi import HTTPException, status

class MyExceptions:
    def __init__(self) -> None:
        pass

    def __call__(self) -> None:
        pass

    def create_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={'WWW-Authenticate': 'Bearer'}
        )