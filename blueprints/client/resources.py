from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *
from .model import Clients
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints import db, app, internal_required
import hashlib,datetime

# Password Encription
from password_strength import PasswordPolicy

bp_client = Blueprint('client', __name__)
api = Api(bp_client)


################################################
#              USING RESTFUL-API               #  
################################################


class ClientResource(Resource):

    def __init__(self):
        pass
    
    # @jwt_required
    # @internal_required
    def get(self, id):
        qry = Clients.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Clients.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    # @jwt_required
    # @internal_required
    def post(self):
        policy = PasswordPolicy.from_names(
            length = 6,
            # uppercase = 2,
            # numbers = 1,
            # special = 2
        )
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location = 'args', required = True)
        parser.add_argument('client_secret', location = 'args', required = True)
        parser.add_argument('token_instagram', location = 'args', required = True)
        parser.add_argument('status', type=inputs.boolean, location = 'args', required = True)
        args = parser.parse_args()

        validation = policy.test(args['client_secret'])

        if validation == []:
            password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()

            # client = Clients(datetime.datetime.now(),args['client_key'], password_digest)

            client = Clients(args['client_key'], password_digest, args['status'], args['token_instagram'])
            db.session.add(client)
            db.session.commit()

            app.logger.debug('DEBUG : %s', client)
            return marshal(client, Clients.response_fields), 200, {'Content-Type' : 'application/json' }
    
    # @jwt_required
    # @internal_required
    def put(self, id):

        policy = PasswordPolicy.from_names(
            length = 6,
            # uppercase = 2,
            # numbers = 1,
            # special = 2
        )

        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location = 'args', required = True)
        parser.add_argument('client_secret', location = 'args', required = True)
        parser.add_argument('status', type=inputs.boolean, location = 'args', required = True)
        args = parser.parse_args()

        qry = Clients.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        validation = policy.test(args['client_secret'])

        if validation == []:
            password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()

        qry.client_key = args['client_key']
        qry.client_secret = password_digest
        qry.status = args['status']
        db.session.commit()

        return marshal(qry, Clients.response_fields), 200, {'Content-Type' : 'application/json' }

    # @jwt_required
    # @internal_required
    def delete(self,id):
        qry = Clients.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        # Hard Delete
        # db.session.delete(qry)
        # db.session.commit()

        # Soft Delete
        qry.deleted = True
        db.session.commit()
        return {'status':'Deleted'}, 200

    # @jwt_required
    # @internal_required
    def patch(self):
        return 'Not yet implement', 501

class ClientList(Resource):

    def __init__(self):
        pass
    
    # @jwt_required
    # @internal_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('status', location = 'args', help = 'invalid sort value', choices = ('False','True'))
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ('status'))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Clients.query

        # qry = Clients.query.filter(Clients.client_key.like("%"+args['client_key']+"%"))

        if args['status'] is not None:
            qry = qry.filter_by(status = args['status'])

        if args['orderby'] is not None :
            if args['orderby'] == 'status':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.status))
                else:
                    qry = qry.order_by(Clients.status)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Clients.response_fields))
        return rows, 200

api.add_resource(ClientList, '', '/list')
api.add_resource(ClientResource, '', '/<id>')
