from flask import Flask, request, render_template, Blueprint, redirect, url_for, session, g, jsonify,current_app,after_this_request
from .auth import login_required
import grouping.algorithm.DE.DE
import grouping.algorithm.GA_MU.GA_MU
import os,datetime,uuid,time
from .dao.Item import Project,Scheme,ProjectFile
from .dao.ProjectManage import ProjectManage
from .dao.SchemeManage import SchemeManage
from .dao.ProjectFileManage import ProjectFileManage



bp = Blueprint('project', __name__, url_prefix='/project')


@bp.route('/home')
@login_required
def show_list():

    return render_template('load.html')


@bp.route('/list')
@login_required
def list_data():
    uid = g.uid
    pm = ProjectManage("rdpg", "root", '123456')
    res = pm.findPro(Project(uid=uid))
    if not res:
        return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
    pid=[]
    for i in res:
        pid.append(i.toDic()['pid'])
    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {'pid': pid}})


@bp.route('/detail', methods=['GET', 'POST'])
@login_required
def detail():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            if not data.get('pid'):
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            elif not isinstance(data.get('pid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            elif len(data.get('pid')) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                pm = ProjectManage("rdpg", "root", '123456')
                res = pm.findPro(Project(pid=data.get('pid')))
                if res:
                    res_data={
                        "basic": {
                            "projectName": res[0].toDic().get('projectName'),
                            "school": res[0].toDic().get('school'),
                            "college": res[0].toDic().get('college'),
                            "year": res[0].toDic().get('year'),
                            "major": res[0].toDic().get('major')
                        },
                        "requirements": {
                            "algorithm": res[0].toDic().get('algorithm'),
                            "groupNum": res[0].toDic().get('groupNum'),
                            "teacherNum": res[0].toDic().get('teacherNum')
                        },
                        "addition": {
                            "nonparticipation": [],
                            "together": res[0].toDic().get('together'),
                            "notTogether": res[0].toDic().get('notTogether'),
                        },
                        "fid": res[0].toDic().get('fid'),
                        "createTime":res[0].toDic().get('createTime')
                    }
                    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': res_data})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})
    return render_template('load.html')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            basic = data.get('basic')
            requirements = data.get('requirements')
            addition = data.get('addition')
            print(addition.get('together'))
            if not data.get('fid') or not basic or not requirements:
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            if not isinstance(data.get('fid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            if len(str(data.get('fid'))) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            if len(basic) < 5 or len(requirements) < 3:
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            for key in basic:
                if not basic[key]:
                    return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            for key in requirements:
                if not requirements[key]:
                    return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            for key in basic:
                if not isinstance(basic[key], str):
                    return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
                if len(basic[key]) > 20:
                    return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            for key in requirements:
                if not isinstance(requirements[key], int):
                    return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
                if len(str(requirements[key])) > 10:
                    return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            pm = ProjectManage("rdpg", "root", '123456')
            pid = uuid.uuid5(uuid.NAMESPACE_DNS, str(request.remote_addr) + str(time.time()))
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res = pm.createPro(Project(uid=g.uid,createTime=dt,fid=data.get('fid'),pid=str(pid),school=basic.get('school'),algorithm=requirements.get('algorithm'),groupNum=requirements.get('groupNum'),teacherNum=requirements.get('teacherNum'),projectName=basic.get('projectName'),major=basic.get('major'),year=basic.get('year'),college=basic.get('college'),together=','.join(addition.get('together')),notTogether=','.join(addition.get('notTogether'))))
            if res:
                return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {'pid':str(pid)}})
            else:
                return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})
    return render_template('load.html')

@bp.route('/execute', methods=['GET', 'POST'])
@login_required
def execute():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            if not data.get('pid') or not data.get('times'):
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            elif not isinstance(data.get('pid'), str) or not isinstance(data.get('times'),int):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            elif len(str(data.get('pid'))) > 40 or len(str(data.get('times')))>10:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                pm = ProjectManage("rdpg", "root", '123456')
                res1 = pm.findPro(Project(pid=data.get('pid')))
                pfm = ProjectFileManage("rdpg", "root", '123456')
                res2 = pfm.findProjectFile(ProjectFile(fid=res1[0].toDic().get('fid')))
                basedir = os.path.abspath(os.path.dirname(__file__))
                file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
                #res_data,filePath = grouping.algorithm.GA_MU.GA_MU.begin(n=4,teachers=4,filedir=file_dir,filename='2020_data.xlsx')
                k=0
                for i in range(data.get('times')):
                    res_data,filePath=grouping.algorithm.GA_MU.GA_MU.begin(n=res1[0].toDic().get('groupNum'), teachers=res1[0].toDic().get('teacherNum'), filedir=file_dir,filename=res2[0].toDic().get('filePath'))
                    sm = SchemeManage("rdpg", "root", '123456')
                    sid = uuid.uuid5(uuid.NAMESPACE_DNS, str(request.remote_addr) + str(time.time()))
                    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    res3=sm.uploadScheme(Scheme(sid=str(sid),createTime=dt, pid=data.get('pid'), data=str(res_data),filePath=filePath))
                    if res3:
                        k+=1
                if k>0:
                    return jsonify({'status': 0, 'statusInfo': 'Success('+str(k)+')Failed('+str(data.get('times')-k)+')', 'data': {}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})
    return render_template('load.html')

@bp.route('/modify', methods=['GET', 'POST'])
@login_required
def modify():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            basic = data.get('basic')
            requirements = data.get('requirements')
            addition = data.get('addition')
            if not isinstance(data.get('fid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            if len(str(data.get('fid'))) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            if not isinstance(data.get('pid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            if len(str(data.get('pid'))) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            for key in basic:
                if not isinstance(basic[key], str):
                    return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
                if len(basic[key]) > 20:
                    return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            for key in requirements:
                if not isinstance(requirements[key], int):
                    return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
                if len(str(requirements[key])) > 10:
                    return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            pm = ProjectManage("rdpg", "root", '123456')
            res1=pm.findPro(Project(pid=data.get('pid')))
            if not res1:
                return jsonify({'status': 12345, 'statusInfo': 'pid Error', 'data': {}})
            old_pro=res1[0].toDic()
            for key in basic:
                if basic[key]:
                    old_pro[key]=basic[key]
            change=0
            for key in requirements:
                if requirements[key]:
                    old_pro[key]=requirements[key]
                    change=1
            res = pm.updatePro(old_pro,change=change)
            if res:
                return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {}})
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
            if not data.get('pid'):
                return jsonify({'status': 10001, 'statusInfo': 'Empty Form', 'data': {}})
            elif not isinstance(data.get('pid'), str):
                return jsonify({'status': 10007, 'statusInfo': 'Data Type Error', 'data': {}})
            elif len(str(data.get('pid'))) > 40:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            else:
                pm = ProjectManage("rdpg", "root", '123456')
                res = pm.deletePro(Project(pid=data.get('pid')))
                if res:
                    return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status': 20001, 'statusInfo': 'Content-Type Error', 'data': {}})
    return render_template('load.html')