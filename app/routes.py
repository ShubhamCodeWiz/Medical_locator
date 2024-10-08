from flask import request
from flask_restful import Resource
from flasgger import swag_from
from app.models import Equipment
from app import db
from app.utils import get_nearby_equipment

class EquipmentList(Resource):
    @swag_from({
        'tags': ['Equipment'],
        'summary': 'Get a list of all equipment',
        'responses': {
            '200': {
                'description': 'A list of all equipment',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'equipment': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/Equipment'}
                        }
                    }
                }
            }
        }
    })
    def get(self):
        equipment = Equipment.query.all()
        return {'equipment': [e.to_dict() for e in equipment]}, 200

    @swag_from({
        'tags': ['Equipment'],
        'summary': 'Create a new equipment',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'schema': {
                    '$ref': '#/definitions/Equipment'
                }
            }
        ],
        'responses': {
            '201': {
                'description': 'Created equipment',
                'schema': {'$ref': '#/definitions/Equipment'}
            },
            '400': {
                'description': 'Invalid input'
            }
        }
    })
    def post(self):
        data = request.get_json()
        required_fields = ['name', 'latitude', 'longitude', 'address']
        for field in required_fields:
            if field not in data:
                return {'error': f"'{field}' is a required field."}, 400

        existing_equipment = Equipment.query.filter_by(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude']
        ).first()
        if existing_equipment:
            return {'message': 'Equipment with the same name and location already exists.'}, 400

        new_equipment = Equipment(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            address=data['address'],
            contact_info=data.get('contact_info'),
            availability_status=data.get('availability_status', True)
        )
        db.session.add(new_equipment)
        db.session.commit()
        return new_equipment.to_dict(), 201

class EquipmentResource(Resource):
    @swag_from({
        'tags': ['Equipment'],
        'summary': 'Get a specific equipment',
        'parameters': [
            {
                'name': 'equipment_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Equipment details',
                'schema': {'$ref': '#/definitions/Equipment'}
            },
            '404': {
                'description': 'Equipment not found'
            }
        }
    })
    def get(self, equipment_id):
        equipment = Equipment.query.get_or_404(equipment_id)
        return equipment.to_dict(), 200

    @swag_from({
        'tags': ['Equipment'],
        'summary': 'Update a specific equipment',
        'parameters': [
            {
                'name': 'equipment_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'body',
                'in': 'body',
                'schema': {
                    '$ref': '#/definitions/Equipment'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Updated equipment',
                'schema': {'$ref': '#/definitions/Equipment'}
            },
            '404': {
                'description': 'Equipment not found'
            }
        }
    })
    def put(self, equipment_id):
        equipment = Equipment.query.get_or_404(equipment_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(equipment, key, value)
        db.session.commit()
        return equipment.to_dict(), 200

    @swag_from({
        'tags': ['Equipment'],
        'summary': 'Delete a specific equipment',
        'parameters': [
            {
                'name': 'equipment_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            '204': {
                'description': 'Equipment deleted'
            },
            '404': {
                'description': 'Equipment not found'
            }
        }
    })
    def delete(self, equipment_id):
        equipment = Equipment.query.get_or_404(equipment_id)
        db.session.delete(equipment)
        db.session.commit()
        return '', 204

class NearbyEquipment(Resource):
    @swag_from({
        'tags': ['Equipment'],
        'summary': 'Get nearby equipment',
        'parameters': [
            {
                'name': 'lat',
                'in': 'query',
                'type': 'number',
                'required': True
            },
            {
                'name': 'lon',
                'in': 'query',
                'type': 'number',
                'required': True
            },
            {
                'name': 'radius',
                'in': 'query',
                'type': 'number',
                'default': 5.0
            }
        ],
        'responses': {
            '200': {
                'description': 'List of nearby equipment',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nearby_equipment': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/Equipment'}
                        }
                    }
                }
            },
            '400': {
                'description': 'Invalid input'
            }
        }
    })
    def get(self):
        try:
            lat = float(request.args.get('lat'))
            lon = float(request.args.get('lon'))
            radius = float(request.args.get('radius', 5.0))
        except ValueError:
            return {'error': 'Invalid latitude, longitude, or radius values.'}, 400

        nearby = get_nearby_equipment(lat, lon, radius)
        return {'nearby_equipment': [e.to_dict() for e in nearby]}, 200

def initialize_routes(api):
    api.add_resource(EquipmentList, '/api/equipment')
    api.add_resource(EquipmentResource, '/api/equipment/<int:equipment_id>')
    api.add_resource(NearbyEquipment, '/api/equipment/nearby')

# Swagger definitions
definitions = {
    'Equipment': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'readOnly': True},
            'name': {'type': 'string'},
            'latitude': {'type': 'number'},
            'longitude': {'type': 'number'},
            'address': {'type': 'string'},
            'contact_info': {'type': 'string'},
            'availability_status': {'type': 'boolean'}
        },
        'required': ['name', 'latitude', 'longitude', 'address']
    }
}