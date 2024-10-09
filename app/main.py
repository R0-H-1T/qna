from fastapi import FastAPI, Header, status, Request, HTTPException, Depends
from contextlib import asynccontextmanager
from app.db import createdb, get_session
from typing import Annotated
from pydantic import ValidationError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import Questionaire, QuestionnaireTable, Answers, QuestionTable, AnswerTable, AnswersTable
# for uvi use without period, and for fastapi use with .
from app.helper import check_token
from sqlmodel import Session, select
from dotenv import load_dotenv
import os
from httpx import AsyncClient


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    createdb()
    yield


app = FastAPI(lifespan=lifespan, title="Qna Service")
security = HTTPBearer()
url = f"http://{os.environ.get('AUTH_DNS')}" or f"http://localhost:{os.getenv('PORT_NO')}"

@app.get('/auth_service', tags=['test'])
async def auth_service_test():
    async with AsyncClient() as client:
        r = await client.get(url=url)

    return r.json()
		


@app.post('/question', tags=['questionnaire'], status_code=status.HTTP_201_CREATED)
async def create_question(
    questionnaire: Questionaire,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
):

    res = await check_token(credentials.scheme, credentials.credentials, f"{url}/token")
    
    db_qna = QuestionnaireTable(title=questionnaire.title, email=res.get('sub'))
    # db_qna = QuestionnaireTable(title=questionnaire.title, email='remi@example.com')
 
    try:
        for questions in questionnaire.questions:
            db_ques = QuestionTable.model_validate(
                questions, update={'options': questions.choices, 'questionnaire': db_qna})
            session.add(db_ques)
            session.commit()
    except ValidationError as e:
        HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Model Validation failed: QuestionTable")



@app.post('/answer', tags=['answer'], status_code=status.HTTP_200_OK)
async def post_answer(
    answers: Answers,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
):
    questionnaire_id = answers.questionnaire_id

    res = await check_token(credentials.scheme, credentials.credentials, f"{url}/token")

    db_answerstable = AnswersTable(questionnaire_id=questionnaire_id)
    
    try:
        for ans in answers.answers:
            db_answer = AnswerTable.model_validate(ans, update={'answer': db_answerstable})
            session.add(db_answer)
            session.commit()
    except:
        HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Model validation failed AnswerTable"
        )        


'''
Idea:
in the analytics service, to perform analysis on a specific questionnaire, user will retrieve all the answers of
that questionnaire and spit out the results.

so the user will hit som route as - 

/analytics/{questionnaireID}, with token
request forwarded to qna service for validating token.
token contains claims 'email'

first it will check if any questionnaires with that email are present or not in the DB
then from questionnaire service, it will fetch all the answers to the questionnaire with matching email (Questionnaire Mode Add email field)
All the answers returned to the analytics, along with questionnaire
analytics perform relevent analysis - display to the user.


1. Data will be big in size to transport - any techs available?
2. clearance regarding scope in client credential OAuth flow

'''    
@app.get('/get_qna/{qna_id}', tags=['get qna'])
async def get_qna(qna_id, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: Session = Depends(get_session)):


    res = await check_token(credentials.scheme, credentials.credentials, f"{url}/token")

    final_result: dict = {}

    # will return all the questionnaires found with the email, add filteration with id
    statement = select(QuestionTable).join(QuestionnaireTable).where(QuestionnaireTable.email == res.get('sub')).where(QuestionnaireTable.id == qna_id)
    result = session.exec(statement)
    # qna_id = result.first().questionnaire_id
    qna_ques = []
    for ques in result:
        qna_ques.append({"correct":ques.correct, "mcq": ques.mcq, "qna_id": ques.questionnaire_id, "id": ques.id, "text": ques.text})

    
    statement2 = select(AnswerTable).join(AnswersTable).where(AnswersTable.questionnaire_id == qna_id)
    get_answers = session.exec(statement2)

    # @TODO
    # further testing required in regards to fetching data from DB
    # handle cases like null, etc?
    qna_ans, temp = [], []       
    count = -1
    for ans in get_answers:    
        if count == -1:
            temp.append({"mcq": ans.mcq, "choice": ans.choice, "text": ans.text})
            count = ans.answers_id
            # print(count, "top")
            continue
        if count == ans.answers_id:
            temp.append({"mcq": ans.mcq, "choice": ans.choice, "text": ans.text})
            # print(count, "mid")
        else:
            qna_ans.append(temp)
            # print(qna_ans)
            # print(temp)
            temp = []
            temp.append({"mcq": ans.mcq, "choice": ans.choice, "text": ans.text})
            count = ans.answers_id
            # print(count, "bot")

    qna_ans.append(temp)        
    # print(qna_ans)
    final_result.update({"ques": qna_ques, "ans": qna_ans})
    return final_result




@app.get('/testjson', tags=['testjson'], status_code=status.HTTP_200_OK)
async def test_json(session: Session = Depends(get_session)):
    db_test = session.exec(select(QuestionTable).offset(0).limit(100)).all()
    return db_test
