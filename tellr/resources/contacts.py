from flask_restplus import Resource
from tellr.models.contact import ContactModel
from tellr.schemas.contact import ContactSchema

contact_schema = ContactSchema()
contact_list_schema = ContactSchema(many=True)


class ContactList(Resource):
    @classmethod
    def get(cls):
        contacts = ContactModel.find_all()
        return {"contacts": contact_list_schema.dump(contacts)}, 200


class Contact(Resource):
    @classmethod
    def get(cls, contact_id):
        contact = ContactModel.find_by_id(contact_id)
        if contact:
            return {"contact": contact_schema.dump(contact)}, 200
        return {"message": "contact was not found"}, 404

    @classmethod
    def delete(cls, contact_id):
        contact = ContactModel.find_by_id(contact_id)
        if contact:
            contact.delete_from_db()
            return {"message": "contact was deleted"}, 200
        return {"message": "contact was not found"}, 404
