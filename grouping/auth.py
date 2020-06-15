import functools,uuid,time
from flask import request,render_template,Blueprint,redirect,url_for,session,g,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from .dao.Item import User
from .dao.UserManage import UserManage

bp=Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            um=UserManage("rdpg","root",'123456')
            if not data.get('userName') or not data.get('email') or not data.get('password'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            elif len(data.get('userName'))>20 or len(data.get('password'))>20 or len(data.get('password'))<6 or len(data.get('email'))>64:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            elif um.findUserByUserInfo(User(email=data.get('email'))):
                return jsonify({'status': 10004, 'statusInfo': 'Email Registered', 'data': {}})
            else:
                uid=uuid.uuid5(uuid.NAMESPACE_DNS,str(request.remote_addr)+str(time.time()))
                if um.register(User(str(uid),data.get('userName'),generate_password_hash(data.get('password')),data.get('email'))):
                    return jsonify({'status':0,'statusInfo':'Success','data':{}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})

        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})
    return render_template('load.html')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.is_json:
            data = request.json
            um=UserManage("rdpg","root",'123456')
            res=um.findUserByUserInfo(User(email=data.get('email')))
            if not data.get('email') or not data.get('password'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            elif len(data.get('password'))>20 or len(data.get('password'))<6 or len(data.get('email'))>64:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            elif not res:
                return jsonify({'status': 10002, 'statusInfo': 'Email or Password Error', 'data': {}})
            elif not check_password_hash(res[0][2],data.get('password')):
                return jsonify({'status': 10002, 'statusInfo': 'Email or Password Error', 'data': {}})
            else:
                session.clear()
                session['uid'] = str(res[0][0])
                return jsonify({'status':0,'statusInfo':'Success','data':{}})
        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})
    return render_template('load.html')

@bp.before_app_request
def load_logged_in_user():
    uid = session.get('uid')

    if not uid:
        g.uid = None
    else:
        g.uid = uid

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.uid is None:
            return jsonify({'status': 10003, 'statusInfo': 'Not Authenticated', 'data': {}})

        return view(**kwargs)

    return wrapped_view

@bp.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            um=UserManage("rdpg","root",'123456')
            res=um.findUserByUid(g.uid).toDic()
            if not data.get('oldPassword') or not data.get('newPassword'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            elif len(data.get('oldPassword'))>20 or len(data.get('oldPassword'))<6 or len(data.get('newPassword'))>20 or len(data.get('newPassword'))<6:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            elif not res:
                return jsonify({'status': 10003, 'statusInfo': 'Not Authenticated', 'data': {}})
            elif not check_password_hash(res.get('password'),data.get('oldPassword')):
                return jsonify({'status': 10002, 'statusInfo': 'Password Error', 'data': {}})
            else:
                if um.updateUserByUserInfo(User(res.get('uid'),res.get('userName'),generate_password_hash(data.get('newPassword')),res.get('email'))):
                    return jsonify({'status':0,'statusInfo':'Success','data':{}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})

        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})
    return render_template('load.html')

@bp.route('/unsubscribe',methods=['GET','POST'])
@login_required
def unsubscribe():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            um = UserManage("rdpg", "root", '123456')
            res = um.findUserByUid(g.uid).toDic()
            if not data.get('password'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            elif len(data.get('password'))>20 or len(data.get('password'))<6:
                return jsonify({'status': 10006, 'statusInfo': 'Length Error', 'data': {}})
            elif not res:
                return jsonify({'status': 10003, 'statusInfo': 'Not Authenticated', 'data': {}})
            elif not check_password_hash(res.get('password'),data.get('password')):
                return jsonify({'status': 10002, 'statusInfo': 'Password Error', 'data': {}})
            else:
                if um.deleteUserByUid(g.uid):
                    return jsonify({'status':0,'statusInfo':'Success','data':{}})
                else:
                    return jsonify({'status': 12345, 'statusInfo': 'Unknown', 'data': {}})
        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})
    return render_template('load.html')






