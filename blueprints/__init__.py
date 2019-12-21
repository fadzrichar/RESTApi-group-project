import json, os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from datetime import timedelta
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

app = Flask(__name__)
app.config['APP_DEBUG'] = True

try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/db_rest_api'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/db_test_rest_api'
except Exception as e:
    raise e



# sqlalchemy config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta123@0.0.0.0:3306/rest_training'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#######
# JWT #
#######

app.config['JWT_SECRET_KEY'] = 'FaDzRiChArIsMa'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['isinternal']:
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

##############################
# SQLAlchemy Database config #
##############################

db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    # if request.method == 'GET':
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s",
            json.dumps({
                'status_code': response.status_code,
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request':request.args.to_dict(),
                'response':json.loads(response.data.decode('utf8'))
                })
                )
    elif response.status_code == 404:
        app.logger.warning("REQUEST_LOG\t%s",
            json.dumps({
                'status_code': response.status_code,
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request':request.args.to_dict(),
                'response':json.loads(response.data.decode('utf8'))
                })
                )
    else:
        app.logger.error("REQUEST_LOG\t%s",
            json.dumps({
                'status_code': response.status_code,
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request':request.args.to_dict(),
                'response':json.loads(response.data.decode('utf8'))
                })
                )

    return response


#####################
# IMPORT BLUEPRINTS #
#####################

from blueprints.mealdb.resources import bp_mealdb
from blueprints.client.resources import bp_client

app.register_blueprint(bp_mealdb, url_prefix='/mealdb')
app.register_blueprint(bp_client, url_prefix='/client')

db.create_all()