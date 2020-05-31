from flask import Flask,request,render_template,Blueprint,redirect,url_for,session,g,jsonify

bp=Blueprint('project',__name__,url_prefix='/project')

@bp.route('/home')
def show_list():
    return render_template('load.html')

@bp.route('/list')
def list_data():
    if True:
        return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {'pid':[]}})
    else:
        return jsonify({'status': 10003, 'statusInfo': 'Not Authenticated', 'data': {}})

