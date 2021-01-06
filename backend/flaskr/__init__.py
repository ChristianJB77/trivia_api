import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#Site pagination function
def paginate_questions(request, response):
    #Get page from HTML (frontend), default page 1
    page = request.args.get('page', 1, type=int)
    #HTML page starts at 1, but list has 0 indexing
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    #Format questions, list comprehension
    questions = [q.format() for q in response]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS, allow all origins
    CORS(app)

    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                                'Content-Type,Authorization,true')
        #Display(GET), Add(POST), Delete(DELETE) methods necessary
        response.headers.add('Access-Control-Methods',
                                'GET,POST,DELETE,OPTIONS')
        return response


    """GET all available categories"""
    @app.route('/categories') #GET
    def retrieve_categories():
        res = Category.query.order_by('id').all()
        #Fontend needs dict for categories
        categories = {r.id: r.type for r in res}
        #If categories empty -> 404
        if len(categories) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "categories": categories
        })


    """GET questions paginated"""
    @app.route('/questions')
    def retrieve_questions_paginated():
        response = Question.query.order_by('id').all()
        questions = paginate_questions(request, response)
        #If questions empty of selected page -> 404
        if len(questions) == 0:
            abort(404)

        cat_res = Category.query.order_by('id').all()
        #Fontend needs dict for categories
        categories = {c.id: c.type for c in cat_res}
        #All categories by default
        current_category = None

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(response),
            "categories": categories,
            "current_category": current_category
        })


    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        try:
            q = Question.query.filter(Question.id == q_id).one_or_none()

            if q is None:
                abort(404)

            q.delete()

            return jsonify({
                "success": True
            })
        except:
            abort(422)


    """POST new question"""
    @app.route('/questions', methods=['POST'])
    def new_question():
        #Get HTML json body response
        body = request.get_json()

        try:
            #Subtract data
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)

            if (new_question == '') or (new_answer == ''):
                abort(404)

            question = Question(
                question = new_question,
                answer = new_answer,
                category = new_category,
                difficulty = new_difficulty
                )
            #Add to db with model method
            question.insert()

            return jsonify({
                "success": True,
            })

        except:
            abort(405)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''


    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    """Error handler"""
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource NOT found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method NOT allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    return app
