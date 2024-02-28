from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/madmin')
def madmin():
    return 'This is admin ssssssspage'




