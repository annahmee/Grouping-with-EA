import functools
from flask import Flask,request,render_template,flash,Blueprint,redirect,url_for,session,g
from werkzeug.security import generate_password_hash, check_password_hash
from .form import LoginForm,RegisterForm
from .db import user_col

bp=Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/remider')
def login_remider():
    return render_template('remider.html')
    
@bp.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        account=form.account.data
        mail=form.mail.data
        password=form.password.data
        a_doc=user_col.find_one({'mail':mail})
        if a_doc:
            flash('邮箱已注册')
        else:
            user_col.insert_one({'account':account,'mail':mail,'password':generate_password_hash(password)})
            #flash('注册成功，正在跳转到登陆界面...')
            return redirect(url_for('auth.login'))
    return render_template('register.html',form=form)

@bp.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        mail=form.mail.data
        password=form.password.data
        a_doc=user_col.find_one({'mail':mail})
        if not a_doc:
            flash('用户不存在')
        elif not check_password_hash(a_doc['password'],password):
            flash('邮箱或密码错误')
        else:
            session.clear()
            session['user_mail']=a_doc['mail']
            return redirect(url_for('grouping.home'))
    return render_template('login.html',form=form)



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
            return redirect(url_for('auth.login_remider'))

        return view(**kwargs)

    return wrapped_view




