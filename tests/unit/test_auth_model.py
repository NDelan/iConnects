from app.auth.models import Student, Alum

'''
    Tests the Student table
'''
def test_student_set_password():
    student = Student()
    student.set_password('password')
    assert student.password_hash is not None
    assert student.password_hash != 'password'


def test_student_check_password():
    student = Student()
    student.set_password('password')
    assert student.check_password('password')
    assert not student.check_password('wrongpassword')


def test_student_set_username():
    student = Student()
    student.set_username('username')
    assert student.username == 'username'
    assert not student.username == 'no_name'


def test_student_check_username():
    student = Student()
    student.set_username('username')
    assert student.check_username()


def test_student_set_mentor():
    student = Student()
    student.set_mentor('Akezhan')
    assert student.mentor == 'Akezhan'
    assert not student.mentor == 'something_else'


def test_student_get_mentor():
    student = Student()
    student.set_mentor('Akezhan')
    assert student.get_mentor() == 'Akezhan'
    assert not student.get_mentor() == 'something_else'


'''
    Tests the Alum table
'''
def test_alum_set_password():
    alum = Alum()
    alum.set_password('password')
    assert alum.password_hash is not None
    assert alum.password_hash != 'password'


def test_alum_check_password():
    alum = Alum()
    alum.set_password('password')
    assert alum.check_password('password')
    assert not alum.check_password('wrongpassword')


def test_alum_set_username():
    alum = Alum()
    alum.set_username('username')
    assert alum.username == 'username'
    assert not alum.username == 'no_name'


def test_alum_check_username():
    alum = Alum()
    alum.set_username('username')
    assert alum.check_username()
