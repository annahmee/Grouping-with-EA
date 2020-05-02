from flask import Flask,request,render_template,flash,Blueprint,redirect,url_for,session,g
from .auth import login_required
from .db import user_col

bp=Blueprint('grouping',__name__,url_prefix='/grouping')

@bp.route('/home')
@login_required
def home():
    return render_template('home.html')
