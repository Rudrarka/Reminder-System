from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import json
import utils

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@127.0.0.1/Numberz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    due_date = db.Column(db.Date)

    def __init__(self, name):
        self.name = name
        self.due_date = due_date

class Reminder(db.Model):
    __tablename__ = 'reminder'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice.id"))
    trigger_date = db.Column(db.Date)

    def __init__(self, name):
        self.name = name
        self.invoice_id = invoice_id
        self.trigger_date = trigger_date


"""API to update the due date of the invoice and trigger date of the reminder.
Input params : String invoice_id and String due_date_str.
"""
@app.route('/api/invoice/update-due-date', methods=['PATCH'])
def update_due_date():
    data = request.get_json(force=True)
    invoice_id = data['invoice_id']
    due_date_str = data['due_date_str']
    updated_due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    diff = utils.diff_days(updated_due_date)

    if diff < 0:
        message = {
            'message' : 'Requested due date has already passed. Please select a relevant date. '
        }
        return json.dumps(message)

    try:
        status, message = utils.update_invoice_due_date(db.session, invoice_id, updated_due_date)
        if not status:
            message = {
                'message' : message
            }
            return json.dumps(message)
        db.session.commit()
        app.logger.info('Committed successfully.')
        message = {
            'message' : 'Updated due date of the invoice.' + message
        }
        return json.dumps(message)
    except Exception as e:
        db.session.rollback()
        print (e)
        app.logger.error(str(e))
        message = {
            'message' : 'Update failed due to some issue. Plese try again later.'
        }
        return json.dumps(message)
    finally:
        db.session.close()
        app.logger.info('Session closed.')
 
    
        


