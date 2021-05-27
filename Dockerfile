FROM tensorflow/tensorflow

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY answer.py answer.py

CMD ["python", "answer.py"]

