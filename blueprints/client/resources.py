from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Clients
from . import *
from blueprints import db, app, internal_required
import datetime, hashlib
from flask_jwt_extended import jwt_required
from password_strength import PasswordPolicy

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):
    
    def __init__(self):
        pass

    @jwt_required
    @internal_required    
    def get(self, client_id):
        qry = Clients.query.get(client_id)
        if qry is not None:
            return marshal(qry, Clients.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        policy = PasswordPolicy.from_names(
            length = 7
            # uppercase = 2,
            # number = 1,
            # special = 2,
            # nonletter = 1
        )

        parser = reqparse.RequestParser()
        # parser.add_argument('client_id', type=int, location = 'json', required = True)
        parser.add_argument('client_key', location = 'json', required = True)
        parser.add_argument('client_secret', location = 'json', required = True)
        parser.add_argument('status', type = inputs.boolean, location = 'json')
        args = parser.parse_args()

        validation = policy.test(args['client_secret'])
        if validation == []:
            password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()

            client = Clients(args['client_key'], password_digest, args['status'])
        
            db.session.add(client)
            db.session.commit()

            app.logger.debug('DEBUG %s', client)
            return marshal(client, Clients.response_fields), 200
        return {'status':'failed', 'result': validation}, 400, {'Content-Type':'applicaton/json'} 

    @jwt_required
    @internal_required
    def delete(self, client_id):
        qry = Clients.query.get(client_id)
        if qry is None:
            return {'status': 'NOT_FOUND', 'message': 'Client not found'}, 404, { 'Content-Type': 'application/json' }

        # hard delete
        db.session.delete(qry)
        db.session.commit()

        # soft delete
        # qry.deleted = True
        # db.session.commit()
        return {'status': 'DELETED'}, 200

    @jwt_required
    @internal_required
    def put(self, client_id):
        policy = PasswordPolicy.from_names(
            length = 7
        )

        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location = 'json', required = True)
        parser.add_argument('client_secret', location = 'json', required = True)
        parser.add_argument('status', type = inputs.boolean, location = 'json')
        args = parser.parse_args()

        validation = policy.test(args['client_secret'])
        qry = Clients.query.get(client_id)
        if qry is None:
            return {'status': 'NOT_FOUND', 'message': 'Client not found'}, 404, { 'Content-Type': 'application/json' }

        if validation == []:
            password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()

            qry = Clients.query.get(client_id)
            qry.client_key = args['client_key']
            qry.client_secret = password_digest
            qry.status = args['status']
            qry.updated_at = datetime.datetime.now()
            db.session.commit()

            if qry is not None:
                return marshal(qry, Clients.response_fields), 200, { 'Content-Type': 'application/json' }

   
class ClientList(Resource):
    
    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location = 'args', default = 1)
        parser.add_argument('rp', type=int, location = 'args', default = 25)
        parser.add_argument('client_id', location = 'args')
        parser.add_argument('status', location = 'args', help = 'invalid status', choices = ('True', 'False', 'true', 'false'))
        parser.add_argument('order_by', location = 'args', help = 'invalid order_by value', choices = ('client_id', 'client_key', 'client_secret', 'status', 'created_at', 'updated_at'))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        # qry = Clients.query.limit(args['rp']).offset(offset)
        # qry = Clients.query.filter(Clients.client_key.like("%"+args['client_key']+"%"))
        qry = Clients.query
        
        if args['status'] is not None:
            qry = qry.filter_by(status=args['status'])

        if args['order_by'] is not None:
            if args['order_by'] == 'client_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.client_id))
                else:
                    qry = qry.order_by((Clients.client_id))
            elif args['order_by'] == 'client_key':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.client_key))
                else:
                    qry = qry.order_by((Clients.client_key))
            elif args['order_by'] == 'client_secret':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.client_secret))
                else:
                    qry = qry.order_by((Clients.client_secret))
            elif args['order_by'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.created_at))
                else:
                    qry = qry.order_by((Clients.created_at))
            elif args['order_by'] == 'updated_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.updated_at))
                else:
                    qry = qry.order_by((Clients.updated_at))
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Clients.response_fields))
        return rows, 200

api.add_resource(ClientResource,'','/<client_id>')
api.add_resource(ClientList,'','/list')