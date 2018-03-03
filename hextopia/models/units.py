from hextopia.app import db


class Unit(db.Model):

    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.id'))

    health = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    range = db.Column(db.Integer)
    speed = db.Column(db.Integer)

    is_alive = db.Column(db.Boolean)
