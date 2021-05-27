FROM tensorflow/tensorflow

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY answer.py /app/answer.py

CMD ["python", "/app/answer.py"]

