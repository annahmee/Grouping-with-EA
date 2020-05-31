from flask import send_from_directory, abort, Blueprint
from werkzeug.utils import secure_filename
from flask import current_app, render_template, jsonify, request
import time, os, uuid, random

bp = Blueprint('resource', __name__, url_prefix='/resource')
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 用于测试上传，稍后用到
@bp.route('/test')
def upload_test():
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, '123'))


@bp.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == "GET":
        file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
        if os.path.isfile(os.path.join(file_dir, filename)):
            return send_from_directory(file_dir, filename, as_attachment=True)
        return jsonify({'status': 20404, 'statusInfo': 'File Not Found', 'data': {}})


@bp.route("/static/<filename>", methods=['GET'])
def static_file(filename):
    if request.method == "GET":
        file_dir = os.path.join(basedir, current_app.config['STATIC_FOLDER'])
        if os.path.isfile(os.path.join(file_dir, filename)):
            return send_from_directory(file_dir, filename, as_attachment=True)
        return jsonify({'status': 20404, 'statusInfo': 'File Not Found', 'data': {}})


# 上传文件
@bp.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['input_file']  # 从表单的file字段获取文件，input_file为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + str(random.randint(100000, 999999)) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        return jsonify({'status': 0, 'statusInfo': 'Success', 'data': {}})
    else:
        return jsonify({'status': 20002, 'statusInfo': 'Upload Failed', 'data': {}})
