import time
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from flask import Flask
from flask import request
from flask import jsonify
import sqlite3
import torch

conn = sqlite3.connect('pythonsqlite.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS models;")
conn.commit()

#Creating table as per requirement
sql = '''CREATE TABLE IF NOT EXISTS Models
        (name varchar(100), tokenizer varchar(100), model varchar(100));'''
cursor.execute(sql)
print("Table Created Successfully")
cursor.execute('''INSERT INTO Models VALUES("distilled-bert","distilbert-base-uncased-distilled-squad","distilbert-base-uncased-distilled-squad");''')
cursor.execute('''INSERT INTO Models VALUES("deepset-roberta","deepset/roberta-base-squad2","deepset/roberta-base-squad2");''')
conn.commit()
conn.close()

# Create my flask app
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/models", methods=['GET', 'PUT', 'DELETE'])
def models():
    if request.method == 'GET':
        conn = sqlite3.connect('pythonsqlite.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Models")
        models = cursor.fetchall()
        listmodels = []
        for i in models:
            output = {
                "name": i[0],
                "tokenizer": i[1],
                "model": i[2]
            }
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)

    elif request.method == 'PUT':
        conn = sqlite3.connect('pythonsqlite.db')
        cursor = conn.cursor()

        insertmodel = request.json
        name = insertmodel['name']
        tokenizer = insertmodel['tokenizer']
        model = insertmodel['model']

        cursor.execute("INSERT INTO Models VALUES (?, ?, ?)", (name, tokenizer, model))
        conn.commit()
        cursor.execute("SELECT * FROM Models")
        models = cursor.fetchall()
        listmodels = []
        for i in models:
            output = {
                "name": i[0],
                "tokenizer": i[1],
                "model": i[2]
            }
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)

    elif request.method == 'DELETE':
        deletemodel = request.args.get('model')

        conn = sqlite3.connect("pythonsqlite.db")
        c = conn.cursor()
        c.execute("DELETE FROM Models WHERE name = ?", (deletemodel,))
        conn.commit()
        c.execute("SELECT * FROM Models")
        model_all = c.fetchall()
        listmodels = []
        for i in model_all:
            output = {
                "name": i[0],
                "tokenizer": i[1],
                "model": i[2]
            }
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)


@app.route("/answer", methods=["POST", "GET"])
def answer():
    conn = sqlite3.connect("pythonsqlite.db")
    cursor = conn.cursor()
    create_table = """CREATE TABLE IF NOT EXISTS QuesAns 
    (timestamp int, answer varchar(100), question varchar(100), context varchar(1000), model varchar(100));"""
    cursor.execute(create_table)
    conn.commit()
    conn.close()

    if request.method == "POST":
        conn = sqlite3.connect("pythonsqlite.db")
        cursor = conn.cursor()
        model_name = request.args.get('model')
        cursor.execute("SELECT * from Models WHERE name = ?", (model_name,))
        temp = cursor.fetchall()
        name = temp[0][0]
        token = temp[0][1]
        model = temp[0][2]
        data = request.json

        ts = int(time.time())
        # Import model
        hg_comp = pipeline('question-answering', model=model, tokenizer=token)
        # Answer the answer
        answer = hg_comp({'question': data['question'], 'context': data['context']})['answer']
        # Create the response body.
        cursor.execute("INSERT INTO answer VALUES (?, ?, ?, ?, ?)", (ts, answer, data['question'], data['context'], model))
        conn.commit()

        out = {
            "model": model_name,
            "timestamp": ts,
            "question": data['question'],
            "context": data['context'],
            "answer": answer
        }
        return jsonify(out)

@app.route("/answer", methods=['GET', 'PUT', 'POST', 'DELETE'])
def answer():
    conn = sqlite3.connect('pythonsqlite.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS QuesAns
    (timestamp int, model varchar, answer varchar,question varchar,context varchar)""")

    if request.method == 'POST':
        answermodel = request.args.get('model', None)
        cursor.execute("SELECT DISTINCT name, tokenizer, model from Models WHERE name = ?", (answermodel,))
        temp = cursor.fetchall()
        name = temp[0][0]
        token = temp[0][1]
        model = temp[0][2]
        data = request.json

        timestamp = int(time.time())
        # Import model
        hg_comp = pipeline('question-answering', model=model, tokenizer=token)
        # Answer the answer
        answer = hg_comp({'question': data['question'], 'context': data['context']})['answer']
        # Create the response body.
        output = {
            "model": answermodel,
            "timestamp": timestamp,
            "question": data['question'],
            "context": data['context'],
            "answer": answer
        }
        return jsonify(output)

    elif request.method == "GET":
        conn = sqlite3.connect("pythonsqlite.db")
        cursor = conn.cursor()

        modelname = request.args.get("model")
        start = request.args.get("start")
        end = request.args.get("end")

        c.execute("SELECT * FROM answer")
        conn.commit()
        model = c.fetchall()
        listmodels = []

        for i in model:
            output = {
                "timestamp": i[0],
                "modelname": i[4],
                "answer": i[1],
                "question": i[2],
                "context": i[3],
            }
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)

# Run if running "python answer.py"
if __name__ == '__main__':
    # Run our Flask app and start listening for requests!
    app.run(host='0.0.0.0', port=8000, threaded=True)

conn.close()
