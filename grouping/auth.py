import functools
from flask import request,render_template,Blueprint,redirect,url_for,session,g,jsonify
from werkzeug.security import check_password_hash

bp=Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            if not data.get('userName') or not data.get('email') or not data.get('password'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            return jsonify({'status':0,'statusInfo':'Success','data':{}})
        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})

    return render_template('register.html')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.is_json:
            data = request.json
            if not data.get('email') or not data.get('password'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            return jsonify({'status':0,'statusInfo':'Success','data':{}})
        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})


        '''
        if not a_doc:
            flash('用户不存在')
        elif not check_password_hash(a_doc['password'],password):
            flash('邮箱或密码错误')
        else:
            session.clear()
            session['user_mail']=a_doc['mail']
            return redirect(url_for('grouping.home'))
        '''

    return render_template('load.html')

@bp.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            if not data.get('oldPassword') or not data.get('newPassword'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            return jsonify({'status':0,'statusInfo':'Success','data':{}})
        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})
    return render_template('load.html')

@bp.route('/unsubscribe',methods=['GET','POST'])
def unsubscribe():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            if not data.get('password'):
                return jsonify({'status':10001,'statusInfo':'Empty Form','data':{}})
            return jsonify({'status':0,'statusInfo':'Success','data':{}})
        else:
            return jsonify({'status':20001,'statusInfo':'Content-Type Error','data':{}})
    return render_template('load.html')

@bp.before_app_request
def load_logged_in_user():
    user_mail = session.get('user_mail')

    if not user_mail:
        g.user = None
    else:
        g.user = user_col.find_one({'mail':user_mail})

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view




