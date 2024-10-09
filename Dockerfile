FROM python:3.10

WORKDIR /qna

COPY ./requirements.txt /qna/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /qna/requirements.txt

COPY ./app /qna/app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--port", "80", "--host", "0.0.0.0"]
