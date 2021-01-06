import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'secret', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        #New question
        self.new_question = {
            "questions": "Who invented the car",
            "answer": "Carl Benz",
            "difficulty": 2,
            "category": "1"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_categories(self):
        """Test retrieve all available categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_retrieve_categories(self):
        """Test 404, if categories list is empty"""
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource NOT found')

    def test_retrieve_questions(self):
        """Test retrieve paginated questions of page 2"""
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)

    def test_404_retrieve_questions(self):
        """Test 404 for on existing page 1000"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource NOT found')

    def test_new_question(self):
        """Test POST new question"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_new_question(self):
        """Test 405 POST new question"""
        res = self.client().post('/questions', json={
                                            "questions": "Who invented the car",
                                            "answer":1,
                                            "difficulty":"Very",
                                            "category": "1"
                                            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method NOT allowed")

    def test_delete_question(self):
        """Test deleting question by id"""
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_delete_question(self):
        """Test deleting NOT existing question by id=1000"""
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

    def test_search(self):
        """Test case-insensitive, sub-string questions search"""
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_search_fail(self):
        """Test searching non existing sub-string to fail"""
        res = self.client().post('/questions',
                                        json={'searchTerm': 'xyzxyzxyzxyz'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
