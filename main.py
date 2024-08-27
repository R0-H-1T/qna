from fastapi import FastAPI, Header, status, Request, HTTPException, Depends
from contextlib import asynccontextmanager
from db import createdb, get_session
from typing import Annotated
from pydantic import ValidationError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Questionaire, QuestionnaireTable, TestJson, QuestionTable
# for uvi use without period, and for fastapi use with .
import httpx
import json
from sqlmodel import Session, select


@asynccontextmanager
async def lifespan(app: FastAPI):
    createdb()
    yield


app = FastAPI(lifespan=lifespan, title="Qna Service")
security = HTTPBearer()


'''
Extract credentials using HTTPBearer under 

credentials: token and scheme: <bearer>

'''


@app.post('/question', tags=['question'], status_code=status.HTTP_201_CREATED)
async def create_question(questionnaire: Questionaire,
                          credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
                          session: Session = Depends(get_session)
                          ):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            url='http://localhost:8000/token',
            headers={
                'Authorization': f'{credentials.scheme} {credentials.credentials}'}
        )

    if r.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=r.status_code, detail='Unauthorized')

    db_qna = QuestionnaireTable(title=questionnaire.title)

    try:
        for questions in questionnaire.questions:
            db_ques = QuestionTable.model_validate(
                questions, update={'options': questions.choices, 'questionnaire': db_qna})
            session.add(db_ques)
            session.commit()
    except ValidationError as e:
        HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Model Validation failed: QuestionTable")
        


@app.get('/testjson', tags=['testjson'], status_code=status.HTTP_200_OK)
async def test_json(session: Session = Depends(get_session)):
    db_test = session.exec(select(QuestionTable).offset(0).limit(100)).all()
    return db_test
