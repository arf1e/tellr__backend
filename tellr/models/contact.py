from tellr.db import db

Model = db.Model


class ContactModel(Model):

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)

    boy_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    girl_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    boy_request = db.Column(db.Integer, db.ForeignKey("requests.id"), nullable=False)
    girl_request = db.Column(db.Integer, db.ForeignKey("requests.id"), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_contacts(cls, sex, id):
        if sex:
            return cls.query.filter_by(boy_id=id)
        return cls.query.filter_by(girl_id=id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
