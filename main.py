from fastapi import FastAPI, Header, status, Request, HTTPException, Depends
from contextlib import asynccontextmanager
from db import createdb, get_session
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Questionaire, QuestionnaireTable, TestJson
# for uvi use without period, and for fastapi use with .
import httpx
import json
from sqlmodel import Session, select

@asynccontextmanager
async def lifespan(app: FastAPI):
    createdb()
    yield


app = FastAPI(lifespan=lifespan)
security = HTTPBearer()


'''
Extract credentials using HTTPBearer under 

credentials: token and scheme: <bearer>

'''
@app.post('/question', tags=['question'], status_code=status.HTTP_200_OK)
async def create_question(questionnaire: Questionaire,
                        #    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
                        session: Session = Depends(get_session)
                           ):
    # async with httpx.AsyncClient() as client:
    #     r = await client.get(
    #         url='http://localhost:8000/token', 
    #         headers={'Authorization': f'{credentials.scheme} {credentials.credentials}'}
    #     )    
    # if r.status_code != 201:
    #     raise HTTPException(status_code=r.status_code, detail='Blah Blah Blah')
    ch = questionnaire.questions[0].choices
    x = json.dumps(['welcome', 'reynolds', 34])
    print(x)
    
    x = TestJson(options=questionnaire.questions[0].choices)

    session.add(x)
    session.commit()
    session.refresh(x)
    # session.refresh(x)


    return {
        'What i got': x
    }



@app.get('/testjson', tags=['testjson'], status_code=status.HTTP_200_OK)
async def test_json(session: Session = Depends(get_session)):
    db_test =  session.exec(select(TestJson).offset(0).limit(100)).all()
    for x in db_test:
        print(x.options, end='\n')    
    return db_test