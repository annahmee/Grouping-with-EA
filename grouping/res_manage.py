from flask import Flask,request,render_template,Blueprint,redirect,url_for,session,g
from .auth import login_required

bp=Blueprint('result',__name__,url_prefix='/result')

@bp.route('/home')
@login_required
def home():
    return render_template('home.html')
