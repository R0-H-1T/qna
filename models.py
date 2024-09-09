from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from typing import List, Optional
from uuid import uuid4


"""
Each question in a questionnaire can be either an MCQ or text based.


Model Questionnaire >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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


/answer
Model Answer >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
questionnaire_id: <int>
answers: [
    {
        mcq: <True|False>
        'choice': <int|None>
        'text': <str|None>
    },
    {},
    {}
]


"""


class AnswerBase(SQLModel):
    mcq: bool
    choice: int | None = None
    text: str | None = None



class Answer(AnswerBase):
    pass


class Answers(SQLModel):
    questionnaire_id: int 
    answers: List[Answer]



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
    email: EmailStr
    questions: list["QuestionTable"] = Relationship(back_populates="questionnaire")
    answers: list["AnswersTable"] | None = Relationship(back_populates="questionnaire")
# why none ? at the time of creating the questionnaire this might not be present



class QuestionTable(QuestionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    options: Optional[List[str | int]] = Field(default=None, sa_column=Column(JSON))
    questionnaire_id: Optional[int] = Field(
        default=None, foreign_key="questionnairetable.id"
    )
    questionnaire: QuestionnaireTable | None = Relationship(back_populates="questions")



class AnswersTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    questionnaire_id: Optional[int] = Field(
        default=None, foreign_key="questionnairetable.id"
    )
    answers: list["AnswerTable"] = Relationship(back_populates="answer")
    questionnaire: QuestionnaireTable | None = Relationship(back_populates="answers")



class AnswerTable(AnswerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    answers_id: Optional[int] = Field(default=None, foreign_key="answerstable.id")
    answer: AnswersTable | None = Relationship(back_populates="answers")




class TestJson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    options: Optional[List[str | int]] = Field(default=None, sa_column=Column(JSON))


