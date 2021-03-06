import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random #random quiz choice

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


    """Delete questions"""
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


    """POST new question / Search question"""
    @app.route('/questions', methods=['POST'])
    def new_question():
        #Get HTML json body response
        body = request.get_json()

        #New question
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        #Search question
        search = body.get('searchTerm', None)

        try:
            if search != None:
                res = Question.query.filter(
                                Question.question.ilike('%{}%'.format(search)))
                #Pagination and MUST formating for frontend
                q = paginate_questions(request, res)
                #All categories by default
                current_category = None

                return jsonify({
                    "success": True,
                    "questions": q,
                    "total_questions": len(q),
                    "current_category": current_category
                })
            elif search == '':
                redirect('/questions')

            else: #Add new question
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


    @app.route('/categories/<int:c_id>/questions')
    def retrieve_questions_by_category(c_id):
        try:
            id = str(c_id)
            res = Question.query.filter(Question.category == id)
            #Pagination and MUST formating for frontend
            q = paginate_questions(request, res)

            current_category = c_id

            return jsonify({
                "success": True,
                "questions": q,
                "total_questions": len(q),
                "current_category": current_category
            })
        except:
            abort(404)


    """POST play quiz with random questions"""
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()

            quiz_category = body.get('quiz_category', None)
            #Get str of user selected category, as category id is strored as string
            selected_cat = str(quiz_category['id'])
            #Get list of ids of previous questions
            previous_qs_ids = body.get('previous_questions', None)
            #Get random question id of selected category,
            #which is NOT in list of previous question ids
            res = 0
            #All categories or selected category differentiation
            if selected_cat == '0':
                res = Question.query.all()
            else:
                res = Question.query.filter(Question.category == selected_cat)

            questions = [r.id for r in res]
            cat_q_ids=[]
            for q in questions:
                if q not in previous_qs_ids:
                    cat_q_ids.append(q)
            #If all questions of category are asked, return to quiz start page
            if len(cat_q_ids) == 0:
                return retrieve_categories()
            else: #Stay in category and play quiz
                #Get random question from unused questions of selected category
                random_id = random.choice(cat_q_ids)
                res = Question.query.filter(Question.id == random_id)
                current_q = paginate_questions(request, res)[0]

                return jsonify({
                    "success": True,
                    "question": current_q
                })
        except:
            abort(422)


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

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal database error"
        }), 500

    return app
