# Production Scale Data Products - Assignment 2

## Functionalities of The Code

<br>
We have created several routes for the question-answer code. These are -
<br>
<br>
GET /moodels
<br>
PUT /models
<br>
DELETE /models?model=<model name>
<br>
POST /answer?model=<model name>
<br>
GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp>
 

## General Information about API
 <br>
The API used is a Question-Answering API which generates answers for the questions from the given context. 
<br>
We have created multiple models and have added the functionality to add or delete models. We can choose any model which has been added in the database to answer the questions
<br>
 <br>
The First Route (GET /models) helps us to get the list of all the available models

 ### Route 1 : GET /models
<br> 
Response:
 <br>
```
 [
    {
        "model": "distilbert-base-uncased-distilled-squad",
        "name": "distilled-bert",
        "tokenizer": "distilbert-base-uncased-distilled-squad"
    },
    {
        "model": "deepset/roberta-base-squad2",
        "name": "deepset-roberta",
        "tokenizer": "deepset/roberta-base-squad2"
    }
  ]
```

 <br>
The second route is used to add a new model to our existing database of models. The model details(model, model-name, tokenixer) of the model is extracted from request.json (Body)  

 ### Route 2: PUT /models
  <br>
Body (request.json):
<br>
 ```
 {
    "name": "bert-tiny",
    "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
    "model": "mrm8488/bert-tiny-5-finetuned-squadv2"
  }
```

Response:
 <br>
```
  [
    {
        "model": "distilbert-base-uncased-distilled-squad",
        "name": "distilled-bert",
        "tokenizer": "distilbert-base-uncased-distilled-squad"
    },
    {
        "model": "deepset/roberta-base-squad2",
        "name": "deepset-roberta",
        "tokenizer": "deepset/roberta-base-squad2"
    },
    {
        "model": "mrm8488/bert-tiny-5-finetuned-squadv2",
        "name": "bert-tiny",
        "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2"
    }
  ]
```
 <br> 
The third route is to delete models from our dataset. The model name which is to be deleted is extracted from the DELETE request and deletes it from the database

 ### Route 3: DELETE /models?model=<model name>
 <br> 
 Example: DELETE /models?model=tiny-bert
 
Response:
 <br> 
 After selecting tiny-bert, the model will be deleted from the database  
```
 [
    {
        "model": "distilbert-base-uncased-distilled-squad",
        "name": "distilled-bert",
        "tokenizer": "distilbert-base-uncased-distilled-squad"
    },
    {
        "model": "deepset/roberta-base-squad2",
        "name": "deepset-roberta",
        "tokenizer": "deepset/roberta-base-squad2"
    }
  ]
 ``` 
<br>
The fourth route is to answer the questions based on the context provided for the particular question. The post request is used to extract the Question and Context from the body (request.json)
<br>
 We have provided an option for the user to choose any model to answer the particular question. The model will be fetched from our database of models.
<br>
 By default, we have selected distilled-bert to answer the questions. The API uses the default model if no model is passed in the syntax.
<br>
 Additionally, a time-stamp is also added to maintain the record of all the questions answered in a new database which can be later fetched

### Route 4:   
  POST /answer?model=<model name>
  Example: POST/answer
  Example: POST/answer?model=deepset-roberta

Body (request.json):
```
 {
    "question": "who did holly matthews play in waterloo rd?",
    "context": "She attended the British drama school East 15 in 2005,
    and left after winning a high-profile role in the BBC drama Waterloo
    Road, playing the bully Leigh-Ann Galloway.[6] Since that role,
    Matthews has continued to act in BBC's Doctors, playing Connie
    Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
    she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
  }
 ```
<br>
 Response:
```
 {
    "answer": "Leigh-Ann Galloway",
    "context": "She attended the British drama school East 15 in 2005, and left after winning a high-profile role in the BBC drama Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that role, Matthews has continued to act in BBC's Doctors, playing Connie Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and she was back in the BBC soap Doctors in 2009, playing Tansy Flack.",
    "model": "distilled-bert",
    "question": "who did holly matthews play in waterloo rd?",
    "timestamp": 1622161059
  }
```

 <br>
 The fifth functionality is to fetch the database of questions answered.
 <br> 
 We have provided an option to select a specific model in which case the output will only display the Question-Answers used by the specific model. If no model is provided, the output will display the answers for all the models which are there in the database
 <br>
 We have also added an option to select the time frame which will help us fetch the question-answers used between the two time frames (UNIX). This is mandatory to fetch the answers.

 
### Route:
  
<br>
  GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp>
<br>  

  
## Where the API can be located (the base URL): 
 
https://assignment2-aqldvq5usa-uc.a.run.app
 

  
## How to build and run the API locally via Docker or Flask
<br>
 The app will locally run thorugh localhost link on port 8080 and can be accessed through postman. The routes need to be added in the url followed by a '/'
  
## Launching the API
<br>
 APIs can be launched using Flask. Flask is used in the code to launch the host and other 5 routes. 

## Making the Handlers
 Handlers facilitate the goals in API. Handlers have a route/path which receives the request and the handler has been invoked. 
 <br>The second function of Handler is to execute the function once Handlers has been invoked.
