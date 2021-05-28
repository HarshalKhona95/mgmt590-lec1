#Importing Libraries
import os
import time
import sqlite3
import torch
from transformers import pipeline
from flask import Flask
from flask import request
from flask import jsonify

#SQLite Connections
conn = sqlite3.connect('pythonsqlite.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS Models;")
conn.commit()
cursor.execute("DROP TABLE IF EXISTS QuesAns;")
conn.commit()

#Creating Table For Models
sql = '''CREATE TABLE IF NOT EXISTS Models
        (name varchar(100), tokenizer varchar(100), model varchar(100));'''
cursor.execute(sql)
#Creating Table For Question Answers
cursor.execute("""CREATE TABLE IF NOT EXISTS QuesAns
(timestamp int, model varchar, answer varchar,question varchar,context varchar)""")
print("Tables Created Successfully")
cursor.execute('''INSERT INTO Models VALUES("distilled-bert","distilbert-base-uncased-distilled-squad","distilbert-base-uncased-distilled-squad");''')
cursor.execute('''INSERT INTO Models VALUES("deepset-roberta","deepset/roberta-base-squad2","deepset/roberta-base-squad2");''')
conn.commit()
conn.close()

# Create My Flask App
app = Flask(__name__)

#Rpute 1 - Models. Functions - Get, Put and Delete
@app.route("/models", methods=['GET', 'PUT', 'DELETE'])
def models():
#GET - To List All Models
    if request.method == 'GET':
        #Opening Connection
        conn = sqlite3.connect('pythonsqlite.db')
        cursor = conn.cursor()
        #Getting a list of all models from the table
        cursor.execute("SELECT * FROM Models")
        models = cursor.fetchall()
        #Emply List
        listmodels = []
        #Printing List as asked in the assignment
        for i in models:
            output = {
                "name": i[0],
                "tokenizer": i[1],
                "model": i[2]
            }
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)

#PUT - To insert a new model
    elif request.method == 'PUT':
        #Connecting Database
        conn = sqlite3.connect('pythonsqlite.db')
        cursor = conn.cursor()
        #Inserting Model From Body
        insertmodel = request.json
        name = insertmodel['name']
        tokenizer = insertmodel['tokenizer']
        model = insertmodel['model']
        #Inserting Into The Database
        cursor.execute("INSERT INTO Models VALUES (?, ?, ?)", (name, tokenizer, model))
        conn.commit()
        #Fetching All Models
        cursor.execute("SELECT * FROM Models")
        models = cursor.fetchall()
        listmodels = []
        #Printing list as asked in the assignment
        for i in models:
            output = {
                "name": i[0],
                "tokenizer": i[1],
                "model": i[2]
            }
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)
#DELETE - To delete models from the database
    elif request.method == 'DELETE':
        #Delete Model From Arguments in the URL
        deletemodel = request.args.get('model')
        conn = sqlite3.connect("pythonsqlite.db")
        c = conn.cursor()
        #Deleting Models In The Table
        c.execute("DELETE FROM Models WHERE name = ?", (deletemodel,))
        conn.commit()
        c.execute("SELECT * FROM Models")
        model_all = c.fetchall()
        listmodels = []
        #Printing list as required in the assignment
        for i in model_all:
            output = {
                "name": i[0],
                "tokenizer": i[1],
                "model": i[2]
            }
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)

#Answers - GET and POST
@app.route("/answer", methods=['GET', 'POST'])
def answer():
#Opening Connection
    conn = sqlite3.connect('pythonsqlite.db')
    cursor = conn.cursor()
 #POST - Posting Answers By Selecting Models 
    if request.method == "POST":
        conn = sqlite3.connect("pythonsqlite.db")
        c = conn.cursor()
        #Default Model Used - Distilled-Bert
        model_name = request.args.get('model', default = "distilled-bert")
        c.execute("SELECT * from Models WHERE name = ?", (model_name,))
        models_table = c.fetchall()
        print(models_table)
        temp = models_table[0]
        print(temp)
        name = temp[0]
        print(name)
        token = temp[1]
        print(token)
        model = temp[2]
        print(model)
        data = request.json
        ts = int(time.time())
        # Import Model
        hg_comp = pipeline('question-answering', model=model, tokenizer=token)
        # Answer the Answer
        answer = hg_comp({'question': data['question'], 'context': data['context']})['answer']
        # Create the response body.
        c.execute("INSERT INTO QuesAns VALUES (?, ?, ?, ?, ?)", (ts, model_name, answer, data['question'], data['context']))
        conn.commit()
        #Print Format
        out = {
            "model": model_name,
            "timestamp": ts,
            "question": data['question'],
            "context": data['context'],
            "answer": answer
        }
        return jsonify(out)
#GET - Getting Solutions by Fetching From Database
    elif request.method == "GET":
        #Opening Database
        conn = sqlite3.connect("pythonsqlite.db")
        cursor = conn.cursor()
        #No Default Method - Output will be For All Models Selected
        modelname = request.args.get("model", default=None)
        start = request.args.get("start")
        end = request.args.get("end")
        #Output For The Model Selected in The URL parameter
        if modelname is not None:
            cursor.execute("SELECT * FROM QuesAns where model='" + modelname + "' and timestamp between ? and ?", [start, end])
            conn.commit()
            model = cursor.fetchall()
            listmodels = []
            for i in model:
                output = {
                    "timestamp": i[0],
                    "modelname": i[1],
                    "answer": i[2],
                    "question": i[3],
                    "context": i[4],
                }
                listmodels.append(output)
        #Output for All Models used 
        else:
            cursor.execute("SELECT * FROM QuesAns where timestamp between ? and ?", (start, end))
            conn.commit()
            model = cursor.fetchall()
            listmodels = []
            for i in model:
                output = {
                    "timestamp": i[0],
                    "modelname": i[1],
                    "answer": i[2],
                    "question": i[3],
                    "context": i[4],
                }
                listmodels.append(output)
            conn.close()
        return jsonify(listmodels)

# Run if running "python answer.py"
if __name__ == '__main__':
    # Run our Flask app and start listening for requests!
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), threaded=True)

conn.close()
