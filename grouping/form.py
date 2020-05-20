from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm): 
    account = StringField('account', validators=[DataRequired('请输入用户名')]) 
    password = PasswordField('Password', validators=[DataRequired('请输入密码'), Length(8, 20)]) 
    mail = StringField('mail', validators=[DataRequired('请输入邮箱')]) 
    submit = SubmitField('submit')

class LoginForm(FlaskForm): 
    password = PasswordField('Password', validators=[DataRequired('请输入密码'), Length(8, 20)]) 
    mail = StringField('mail', validators=[DataRequired('请输入邮箱')]) 
    submit = SubmitField('submit')