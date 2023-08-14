import sys
from io import BytesIO
import wsq  # noqa # pylint: disable=unused-import

from PIL import Image, ImageOps, UnidentifiedImageError
from flask import Flask, request, send_file, render_template, send_from_directory
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

auth = HTTPBasicAuth()

app = Flask(__name__)

_users = {
    'cns_demo': generate_password_hash('cns_demo'),
}


@auth.verify_password
def verify_password(username, password):
    if username in _users:
        return check_password_hash(_users.get(username), password)
    return False


@app.post('/convert-image')
@auth.login_required
def convert_image():
    try:
        image_file = request.files.get('image')
        if image_file is None:
            return 'Image file is required', 400
        dst_format = request.form.get('format')
        if dst_format is None:
            return 'Format is required', 400
        if dst_format not in ('WSQ', 'PNG', 'JPG', 'JPEG', 'BMP', 'TIFF', 'GIF'):
            return 'Unsupported format', 400
        grayscale = request.form.get('grayscale', default=0, type=int)
        dst_w = request.form.get('width', type=int)
        dst_h = request.form.get('height', type=int)
        keep_ratio = request.form.get('keep_ratio', default=1, type=int)
        img = Image.open(image_file.stream)
        target_format = img.format
        if grayscale:
            img = img.convert('L')
        if dst_w and dst_h and dst_w > 0 and dst_h > 0:
            w, h = dst_w, dst_h
            if keep_ratio:
                img = ImageOps.contain(img, (w, h))
            else:
                img = img.resize((w, h))
        if dst_format:
            match dst_format.strip().upper():
                case 'WSQ':  # Force Grayscale
                    if not grayscale:
                        img = img.convert('L')
                    target_format = 'WSQ'
                case 'JPG' | 'JPEG':
                    if not grayscale and img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    target_format = 'JPEG'
                case 'BMP':
                    target_format = 'BMP'
                case 'TIFF':
                    target_format = 'TIFF'
                case 'PNG':
                    target_format = 'PNG'
                case 'GIF':
                    target_format = 'GIF'
        f = BytesIO()
        img.save(f, format=target_format)
        f.seek(0)
        file_name = f'image.{target_format.lower()}'
        return send_file(f, download_name=file_name)
    except UnidentifiedImageError:
        return 'Cannot identify input image format', 400
    except Exception as e:
        print(e, file=sys.stderr)
        return 'Something went wrong', 500


@app.route('/')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')


if __name__ == '__main__':
    app.run()
