from app import db


class Magazine(db.Model):
    __tablename__ = "magazines"

    id = db.Column(db.Integer, primary_key=True)
    publisher = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)