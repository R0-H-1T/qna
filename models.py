from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from typing import List, Optional
from uuid import uuid4


'''
Each question in a questionnaire can be either an MCQ or text based.


Model >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'questionaireID': <ID>
'title': <str>
'questions': [
    {
        'question': <ID>,
        'mcq': <True|False>
        'options': [option1, option2, option3],
        'correct': [optionAns],
        'text': <string>
    }
]
'''


class QuestionBase(SQLModel):
    mcq: bool
    question: str
    correct: int | None = None
    text: str | None = None



class Question(QuestionBase):
    choices: Optional[List[str | int]] = None



class Questionaire(SQLModel):
    title: str
    questions: List[Question]



class QuestionnaireTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    questions: list["QuestionTable"] = Relationship(back_populates="questionnaire")



class QuestionTable(QuestionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    options: Optional[List[str | int]] = Field(default=None, sa_column=Column(JSON))
    questionnaire_id: Optional[int] = Field(default=None, foreign_key="questionnairetable.id")
    questionnaire: QuestionnaireTable | None = Relationship(back_populates="questions")



class TestJson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    options: Optional[List[str|int]] = Field(default=None, sa_column=Column(JSON))