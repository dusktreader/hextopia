from hextopia.app import db


class UnitType(db.Model):

    __tablename__ = 'unit_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, index=True)

    initial_health = db.Column(db.Integer)
    initial_strength = db.Column(db.Integer)
    initial_range = db.Column(db.Integer)
    initial_speed = db.Column(db.Integer)
