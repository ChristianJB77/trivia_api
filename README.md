# Trivia API of Udacity

This API provides a Trivia Quiz game. Users can add new questions, delete and group them by the defined categories. The Game function can played by category or with all questions. Questions in game mode will be randomly selected and dame questions will not be repeated.

API follows the RESTful principles and returns HTTP json responses.


## Installation - API Set-up

### Pre-requisites and Local Development

Developers using this project should already have at least Python3.7 (better the latest Python stable release), pip and node installed on their local machines.

### Backend

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

#### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

#### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

#### Base URL
App runs only locally and is not hosted as a base URL. The backend app is hosted at the default:
http://www.127.0.0.1:5000/books
Which is set as proxy in the frontend.

#### API Keys/Authentication
No keys or authentification available or necessary.

### Errors
App error handler returns HTTP status codes and json objects in following format:

{
    "success": False,
    "error": 400,
    "message": "bad request"
}

#### Client errors
- 400: Bad request
- 404: Resource not found
- 422: Unprocessable

### Resource endpoint library

#### GET /categories
- Show all categories
- Request categories: None
- Returns: success value, categories dictionary (key=id, value=category name)

Sample json object:
`curl http://127.0.0.1:5000/categories`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

```

#### GET /questions
- Show all questions paginated by 10 per site, default page=1
- Questions are ordered by their id
- Request categories: None
- '/questions?page=2' returns 10 questions of page
- Returns: success value, questions, total_questions, categories, current_category

Sample json object:
`curl http://127.0.0.1:5000/questions?page=2`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": "2",
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": "2",
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": "2",
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of acti
on painting?"
    },
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": "4",
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Carl Benz",
      "category": "4",
      "difficulty": 2,
      "id": 25,
      "question": "Who invented the car?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```

### DELETE /questions/{question_id}
- Deletes existing question by id
- Example path '/questions/1', deletes question with id=1
- Request category: Path = question_id
- Returns: success value

`curl -X DELETE http://127.0.0.1:5000/questions/11`
```
{
  "success": true
}
```

### POST /questions
#### Create new question
- Creates new question
- Request category: JSON = question, answer, category, difficulty
- Returns: success value

`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d '{"questions": "Who invented the car", "answer": "Carl Benz", "difficulty": 2, "category": "1"}'`

```
{
  "success": true
}

```

#### Search question
- Based on submitted search from body
- Performs case-insensitive search
- Request category: JSON = searchTerm
- Returns: success value, questions list paginated, total_questions of search result, current_category
- Current category = 0 -> All

`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d '{"searchTerm":"title"}'`

```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bl
aded appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}

```

#### GET /categories/{category_id}/questions
- Show all questions per category paginated
- Questions are ordered by their id of their selected category
- Request categories: Path = category_id
- Returns: success value, questions, total_questions of current category, current_category

Sample json object:
`curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Cross section of an electric motor.",
      "category": "1",
      "difficulty": 4,
      "id": 44,
      "question": "On what is the Tesla Motors logo based?"
    },
    {
      "answer": "384400 km",
      "category": "1",
      "difficulty": 4,
      "id": 47,
      "question": "How far is the moon from our planet earth? (in km)"
    },
    {
      "answer": "Carl Benz",
      "category": "1",
      "difficulty": 2,
      "id": 48,
      "question": null
    }
  ],
  "success": true,
  "total_questions": 6
}
```

#### POST /quizzes
- Trivia game mode
- Questions are shown in random sequence by selected category and will be not repeated, if previous questions list is sent by JSON
- Request categories: JSON = quiz_category, previous_questions
- Returns: success value, question

Sample json object:
`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type:application/json" -d '{"quiz_category": {"id": 1}, "previous_questions": [44]}'`

```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": "1",
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```

## Authors
Christian Johann Bayerle
Based on the Udacity Nanodegree 'Full Stack Development'

## Acknowledgements
Thanks to Udacity
