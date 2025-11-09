from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from typing import List, Optional
from app.helper import gen_alphanumeric_str
from uuid import UUID, uuid4


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
    """
    `questionnaire_id` - Id of the questionnaire to which this answer is for.

    `answers` - [mcq, choice, text], [mcq, choice, text], ...  
    """
    questionnaire_id: str 
    answers: List[Answer]



class QuestionBase(SQLModel):
    mcq: bool
    question: str
    correct: int | None = None
    text: str | None = None


class Question(QuestionBase):
    options: Optional[List[str | int]] = None


class Questionaire(SQLModel):
    title: str
    questions: List[Question]



class QuestionnaireTable(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    quiz_code: str|None = Field(default_factory=gen_alphanumeric_str, index=True)
    title: str
    user_id: UUID

    questions: list["QuestionTable"] = Relationship(back_populates="questionnaire", cascade_delete=True)
    answers: list["AnswersTable"] | None = Relationship(back_populates="questionnaire", cascade_delete=True)



class QuestionTable(QuestionBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    options: Optional[List[str | int]] = Field(default=None, sa_column=Column(JSON))

    questionnaire_id: Optional[UUID] = Field(
        default=None, foreign_key="questionnairetable.id", ondelete="CASCADE" # ondelete for removing all the questions if questionnaire is deleted
    )
    questionnaire: QuestionnaireTable | None = Relationship(back_populates="questions")



class AnswersTable(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID

    questionnaire_id: Optional[UUID] = Field(
        default=None, foreign_key="questionnairetable.id", ondelete="CASCADE")
    questionnaire: QuestionnaireTable | None = Relationship(back_populates="answers")

    answers: list["AnswerTable"] = Relationship(back_populates="answer", cascade_delete=True)



class AnswerTable(AnswerBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    answers_id: Optional[UUID] = Field(default=None, foreign_key="answerstable.id", ondelete="CASCADE")

    answer: AnswersTable | None = Relationship(back_populates="answers")




# class TestJson(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     options: Optional[List[str | int]] = Field(default=None, sa_column=Column(JSON))


