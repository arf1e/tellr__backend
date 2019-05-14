from tellr.db import db

Model = db.Model


class BadgeModel(Model):
    __tablename__ = "badges"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15), unique=True)
    title_f = db.Column(db.String(15), unique=True)
    emoji = db.Column(db.String(40), unique=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
