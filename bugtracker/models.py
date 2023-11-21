from bugtracker.extensions import db


log_bug = db.Table('log_bug',
    db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True),
    db.Column('bug_id', db.Integer, db.ForeignKey('bug.id'), primary_key=True)
)

class Bug(db.Model):
    __tablename__ = 'bug'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(2500), nullable=False)
    
    @property
    def calories(self):
        return self.description

class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    bugs = db.relationship('Bug', secondary=log_bug)