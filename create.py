from routes import db
from models import Annotations

db.create_all()

db.session.commit()