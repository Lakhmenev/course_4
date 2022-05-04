from project.dao.models.user import User


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, data):
        ...

    def get_by_email(self, email):
        emails = self.session.query(User)

        if email is not None:
            emails = emails.filter(User.email == email).all()
            return emails
        return None
