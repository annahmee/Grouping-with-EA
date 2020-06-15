from flask import Flask,request,render_template,Blueprint,redirect,url_for,session,g,jsonify,current_app
from .auth import login_required
from .dao.Item import Scheme
from .dao.SchemeManage import SchemeManage
import os,json

bp=Blueprint('result',__name__,url_prefix='/result')
basedir = os.path.abspath(os.path.dirname(__file__))


@bp.route('/list', methods=['POST'])
@login_required
def list_data():
    if request.is_json:
        data = request.json
        if not data.get('pid'):
            return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
        elif not isinstance(data.get('pid'), str):
            return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
        elif len(str(data.get('pid'))) > 40:
            return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
        else:
            sm = SchemeManage("rdpg", "root", '123456')
            res = sm.findProjectFile(Scheme(pid=str(data.get('pid'))))
            if res:
                rid = []
                for i in res:
                    rid.append(i.toDic()['sid'])
                return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {'rid':rid}})
            else:
                return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
    else:
        return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})

@bp.route('/detail', methods=['GET', 'POST'])
@login_required
def detail():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            if not data.get('rid'):
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            elif not isinstance(data.get('rid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            elif len(data.get('rid')) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                sm = SchemeManage("rdpg", "root", '123456')
                res=sm.findProjectFile(Scheme(sid=str(data.get('rid'))))
                if res:
                    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': json.loads(res[0].toDic().get('data'))})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})
    return render_template('load.html')

@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            if not data.get('rid'):
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            elif not isinstance(data.get('rid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            elif len(str(data.get('rid'))) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                sm = SchemeManage("rdpg", "root", '123456')
                res = sm.findProjectFile(Scheme(sid=str(data.get('rid'))))
                if res:
                    filePath = res[0].toDic().get('filePath')
                    file_dir = os.path.join(basedir, current_app.config['RESULT_FOLDER'])
                    path=os.path.join(file_dir,filePath)
                    if os.path.exists(path):
                        os.remove(path)
                    res2 = sm.deleteScheme(Scheme(sid=str(data.get('rid'))))
                    if res2:
                        return jsonify(
                            {'status': 0, 'statusInfo': 'Success', 'data':{}})
                    else:
                        return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'rid Not Found', 'data': {}})
        else:
            return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})
    return render_template('load.html')
