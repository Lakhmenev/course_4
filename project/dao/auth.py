from project.dao.models.user import User


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, data):
        ...

    def get_by_email(self, email):
        users = self.session.query(User)

        if email is not None:
            users = users.filter(User.email == email).one()
            data = {
                'email': users.email,
                'role': users.role,
                'password': users.password,
            }
            return data
        return None
