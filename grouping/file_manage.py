from flask import Flask,request,render_template,Blueprint,redirect,url_for,session,g,jsonify,current_app
from .auth import login_required
from .dao.ProjectFileManage import ProjectFileManage
from .dao.Item import ProjectFile
import os,datetime,uuid,time
import pandas as pd

bp=Blueprint('file',__name__,url_prefix='/file')

@bp.route('/home')
@login_required
def show_list():
    return render_template('load.html')


@bp.route('/list')
@login_required
def list_data():
    uid = g.uid
    pfm = ProjectFileManage("rdpg", "root", '123456')
    res = pfm.findProjectFile(ProjectFile(uid=uid))
    if not res:
        return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
    fid = []
    for i in res:
        fid.append(i.toDic()['fid'])
    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {'fid': fid}})


@bp.route('/detail', methods=['GET', 'POST'])
@login_required
def detail():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            if not data.get('fid'):
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            elif not isinstance(data.get('fid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            elif len(str(data.get('fid'))) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                pfm = ProjectFileManage("rdpg", "root", '123456')
                res = pfm.findProjectFile(ProjectFile(fid=data.get('fid')))
                if res:
                    basedir = os.path.abspath(os.path.dirname(__file__))
                    file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
                    df=pd.read_excel(io=os.path.join(file_dir,res[0].toDic().get('filePath')))
                    res_data = df.to_json(orient='records').encode('utf-8').decode('unicode_escape')
                    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': res_data})
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
            if not data.get('fid'):
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            elif not isinstance(data.get('fid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            elif len(str(data.get('fid'))) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                pfm = ProjectFileManage("rdpg", "root", '123456')
                res = pfm.deleteProjectFile(ProjectFile(fid=data.get('fid')))
                if res:
                    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})
    return render_template('load.html')
