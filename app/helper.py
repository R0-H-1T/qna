import httpx
from fastapi import HTTPException, status


# class Config:
#     url: str = 'http://localhost:8000/token'





async def check_token(scheme: str, credentials: str, end_url: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            url=end_url,
            headers={
                'Authorization': f'{scheme} {credentials}'}
        )

    if r.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=r.status_code)
    
    return r.json()
       