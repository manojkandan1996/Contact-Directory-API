from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
api = Api(app)

contacts = []
contact_id_counter = 1

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

class ContactListResource(Resource):
    def get(self):
        return {'contacts': contacts}, 200

    def post(self):
        global contact_id_counter
        data = request.get_json()

        if not data or 'name' not in data or 'phone' not in data:
            raise BadRequest("Name and phone are required.")

        if not is_valid_phone(data['phone']):
            raise BadRequest("Phone number must be exactly 10 digits.")

        new_contact = {
            'id': contact_id_counter,
            'name': data['name'],
            'phone': data['phone'],
            'email': data.get('email', "")
        }
        contacts.append(new_contact)
        contact_id_counter += 1
        return new_contact, 201

class ContactResource(Resource):
    def get(self, id):
        contact = next((c for c in contacts if c['id'] == id), None)
        if not contact:
            raise NotFound("Contact not found.")
        return contact, 200

    def put(self, id):
        data = request.get_json()
        contact = next((c for c in contacts if c['id'] == id), None)
        if not contact:
            raise NotFound("Contact not found.")

        if 'name' in data:
            contact['name'] = data['name']
        if 'phone' in data:
            if not is_valid_phone(data['phone']):
                raise BadRequest("Phone number must be exactly 10 digits.")
            contact['phone'] = data['phone']
        if 'email' in data:
            contact['email'] = data['email']

        return contact, 200

    def delete(self, id):
        global contacts
        contact = next((c for c in contacts if c['id'] == id), None)
        if not contact:
            raise NotFound("Contact not found.")
        contacts = [c for c in contacts if c['id'] != id]
        return {'message': f'Contact with id {id} deleted.'}, 200

# Register endpoints
api.add_resource(ContactListResource, '/contacts')
api.add_resource(ContactResource, '/contacts/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
