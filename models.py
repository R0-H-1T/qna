from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from typing import List, Optional
from uuid import uuid4
'''
'questionaireID': <ID>
'questions': [
    {
        'question': <ID>,
        'mcq': <True|False>
        'options': [option1, option2, option3],
        'correct': [optionAns],
        'text': <string>
    }
]


questionaire_id | question_id | 


'''


class QuestionBase(SQLModel):
    mcq: bool
    question: str
    correct: int | None = None
    text: str | None = None
    # choices: Optional[List[str]] = Field(default=None)



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
    questionnaire_id: int | None = Field(default=None, foreign_key="questionnairetable.id")
    questionnaire: QuestionnaireTable | None = Relationship(back_populates="questions")

    # questionnaire_id: Optional[int] = Field(foreign_key="questionaire.id")
    # options: Optional[List[str]] = Field(sa_column=Column(JSON))
    # questionnaire: Questionaire | None = Relationship(back_populates="questions")



# class QuestionnnaireTable(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
    # title: str
    # questions: List["QuestionTable"] = Relationship(back_populates="questionnairetable")


# Question.questionnaire = Relationship(back_populates="questions")


class TestJson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    options: Optional[List[str|int]] = Field(default=None, sa_column=Column(JSON))