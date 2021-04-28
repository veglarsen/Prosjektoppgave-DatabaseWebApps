from werkzeug.security import generate_password_hash, check_password_hash
from database import myDB

class Bruker():

    # construct / attributes
    def __init__(self,id, bruker, etternavn, fornavn, passord, eMail):
        self.id = id
        self.bruker = bruker
        self.etternavn = etternavn
        self.fornavn = fornavn
        self.passwordHash = passord.replace("\'", "")
        self.eMail = eMail
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def set_password(self, passord):
        self.passwordHash = generate_password_hash(passord)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def __str__(self):
        return f'Username: {self.bruker}\n' + \
               f'Email: {self.eMail}\n' + \
               f'Password Hash: {self.passwordHash}'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id                          #id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False