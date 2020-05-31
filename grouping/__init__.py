from flask import Flask

def create_app():
    app=Flask('grouping')
    
    app.config.from_pyfile('settings.py')

    from . import auth,pro_manage,resource,res_manage,file_manage
    app.register_blueprint(auth.bp)
    app.register_blueprint(pro_manage.bp)
    app.register_blueprint(resource.bp)
    app.register_blueprint(res_manage.bp)
    app.register_blueprint(file_manage.bp)

    return app



