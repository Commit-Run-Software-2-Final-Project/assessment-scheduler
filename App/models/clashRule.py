from App.database import db

class clashRuleS(db.Model):
    __tablename__ = 'clashRule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    active = db.Column(db.Boolean, default=True)


    def __init__(self, name, description, active):
        self.name = name
        self.description = description
        self.active = active