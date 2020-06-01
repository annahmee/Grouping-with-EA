from flask import Flask,request,render_template,Blueprint,redirect,url_for,session,g,jsonify
from .auth import login_required

bp=Blueprint('project',__name__,url_prefix='/project')

@bp.route('/home')
@login_required
def show_list():
    return render_template('load.html')

@bp.route('/list')
@login_required
def list_data():
    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {'pid':[]}})

@bp.route('/detail',methods=['POST'])
@login_required
def detail():
    if request.is_json:
        data=request.json
        if not data.get('pid'):
            return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
        elif len(data.get('pid'))>64:
            return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
        else:
            if True:
                return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {}})
            else:
                return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
    else:
        return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})

@bp.route('/create',methods=['GET','POST'])
@login_required
def detail():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            if not data.get('pid'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            elif len(data.get('pid'))>64:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                if True:
                    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})
    return render_template('load.html')


@bp.route('/detail',methods=['POST'])
@login_required
def detail():
    if request.is_json:
        data=request.json
        if not data.get('pid'):
            return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
        elif len(data.get('pid'))>64:
            return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
    else:
        return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})

@bp.route('/detail',methods=['POST'])
@login_required
def detail():
    if request.is_json:
        data=request.json
        if not data.get('pid'):
            return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
        elif len(data.get('pid'))>64:
            return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
    else:
        return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})