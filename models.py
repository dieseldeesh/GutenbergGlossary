from routes import db

class Annotations(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def __repr__(self):
		return '<username {}'.format(self.username)