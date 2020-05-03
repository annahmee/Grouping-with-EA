from flask import Flask,request,render_template,flash

def create_app():
    app=Flask('grouping')
    
    app.config.from_pyfile('settings.py')

    from . import auth
    app.register_blueprint(auth.bp)
    from . import grouping
    app.register_blueprint(grouping.bp)

    return app


