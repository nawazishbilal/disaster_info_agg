from db import db

class DisasterReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disaster_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
