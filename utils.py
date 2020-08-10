import app
from datetime import datetime, date, timedelta

"""Method to find the difference of days between a given date and current date.
"""
def diff_days(dt):
    date_today = date.today()
    date_diff = dt - date_today
    return date_diff.days

"""Method to update the trigger date of a reminder.
"""
def update_trigger_date(session, delta_days, invoice_id):
    message = ''
    if session.query(app.Reminder).filter(app.Reminder.id == invoice_id).count() > 0:
        reminder = app.Reminder.query.filter_by(id = invoice_id ).first()
        trigger_date = reminder.trigger_date
        updated_trigger_date = trigger_date + timedelta(days=delta_days)
        reminder.trigger_date = updated_trigger_date
        session.add(reminder)
        diff = diff_days(updated_trigger_date)
            # date_diff = updated_trigger_date - date_today
        if diff < 0:
            message = 'Updated trigger date of the reminder is in the past.'
        else:
            message = 'Updated trigger date of the reminder.'
        print(updated_trigger_date)
    else:
        message = 'Reminder is not present for the invoice.'
    return message

"""Method to update the due date of an Invoice.
"""
def update_invoice_due_date(session, invoice_id, updated_due_date):
    status = True
    if session.query(app.Invoice).filter(app.Invoice.id == int(invoice_id)).count() == 0:
        status = False
        message = 'No invoice with the given id is present'
        return status, message
    invoice = app.Invoice.query.filter_by(id = int(invoice_id) ).first()
    due_date = invoice.due_date    
    delta = updated_due_date - due_date
    delta_days = delta.days
    print(delta_days)
    if delta_days == 0:
        status = False
        message = 'Current due date is same as the requested due date.'
        return status, message
    invoice.due_date = updated_due_date
    session.add(invoice)
    message = update_trigger_date(session, delta_days, invoice.id)
    return status, message