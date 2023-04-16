from src import db


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    phone = db.Column('phone', db.String(20), nullable=False)
    email = db.Column('email', db.String(100), nullable=True)
    address = db.Column('address', db.String(100), nullable=True)
