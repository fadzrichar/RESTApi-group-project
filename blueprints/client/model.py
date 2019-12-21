from blueprints import db
from flask_restful import fields
import datetime

class Clients(db.Model):
	__tablename__ = "client"
	client_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
	client_key = db.Column(db.String(30), unique=True, nullable=False)
	client_secret = db.Column(db.String(255), nullable=False)
	status = db.Column(db.Boolean, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.now())
	updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
	deleted = db.Column(db.Boolean, default=False)

	response_fields = {
		'client_id' :fields.Integer,
		'client_key' :fields.String,
		'client_secret' :fields.String,
		'status' :fields.Boolean,
		'created_at' :fields.DateTime,
		'updated_at' :fields.DateTime,
		'deleted' :fields.Boolean
	}

	jwt_claims_fields = {
		'client_key': fields.String,
		'status': fields.Boolean
	}

	def __init__(self, client_key, client_secret, status):
		self.client_key = client_key
		self.client_secret = client_secret
		self.status = status
		# self.created_at = created_at
		# self.updated_at = updated_at
		# self.deleted = deleted

	def __repr__(self):
		return '<Clients %r>' % self.client_id