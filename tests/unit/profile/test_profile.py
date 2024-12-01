import unittest
from flask import url_for
from app import create_app, db
from app.auth.models import Student, Alum
from app.profile.models import Project, Experience, Achievement

class TestProfile(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.student = Student(
            student_id=1,
            first_name='Test',
            last_name='User',
            initial='T',
            username='student_test',
            email='student@test.com',
            password_hash='hashed_password'
        )
        self.alum = Alum(
            alum_id=1,
            first_name='Test',
            last_name='Alum',
            initial='T',
            username='alum_test',
            email='alum@test.com',
            password_hash='hashed_password'
        )

        # Check for existing student
        if not Student.query.get(self.student.student_id):
            db.session.add(self.student)
        # Check for existing alum
        if not Alum.query.get(self.alum.alum_id):
            db.session.add(self.alum)

        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_profile_page_load_for_student(self):
        with self.client.session_transaction() as session:
            session['user_id'] = self.student.student_id
            session['user_type'] = 'student'
        response = self.client.get(url_for('profile.create_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile Page', response.data)


if __name__ == '__main__':
    unittest.main()