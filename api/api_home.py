from flask import Blueprint, request, make_response, jsonify, g, Response


from api.templating.render_document import render_docx, render_xlsx, render_pptx
from api.middleware import api_post_data_middleware
from auth.middleware import authorization_middleware
from gsuite_api import credentials, gdrive
from slack_bot import send_message
from models.document import Document
from models.user import User

api_blueprint = Blueprint('apiv1', __name__, url_prefix="/apiv1")

# ALLOWED_EXTENSIONS = {'docx', 'xlsx', 'pdf'}
# ALLOWED_TYPE = ['bv', 'rm', 'bv']


@api_blueprint.before_request
def api_middleware():
    if request.method != 'OPTIONS' and request.path.startswith(api_blueprint.url_prefix):
        # Check the user token
        resp = authorization_middleware(request)
        if isinstance(resp, Response):
            return resp
        else:
            g.user = User.get_user_by_id(resp)


@api_blueprint.route('/')
def home():
    return {'ok': True, 'message': 'root'}

@api_blueprint.route('/render/docx', methods=['POST'])
@api_post_data_middleware()
def docx():
    # get the post data
    post_data = request.get_json()
    output_path = render_docx(post_data['type'], post_data['data'], post_data['name'])
    scopes = ['https://www.googleapis.com/auth/drive']
    metadata_mime_type = 'application/vnd.google-apps.document'
    media_mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    creds = credentials.get_delegated_credentials(scopes)
    link = gdrive.upload(creds, output_path, metadata_mime_type, media_mimetype)
    response_object = {
        'ok': True,
        'message': 'File rendered and uploaded in GDrive.',
        'link': link
    }
    resp = send_message.send('Nouveau document généré sur IdéSYS-ERP: ' + link, 'zapier-test')
    print(resp)
    doc = Document(title=post_data['name'], path=output_path, link=link, type=post_data['type'], status="created")
    doc.save()
    return make_response(jsonify(response_object))

@api_blueprint.route('/render/xlsx', methods=['POST'])
@api_post_data_middleware()
def xlsx():
    # get the post data
    post_data = request.get_json()
    output_path = render_xlsx(post_data['type'], post_data['data'], post_data['name'])
    scopes = ['https://www.googleapis.com/auth/drive']
    metadata_mime_type = 'application/vnd.google-apps.spreadsheet'
    media_mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    creds = credentials.get_delegated_credentials(scopes)
    link = gdrive.upload(creds, output_path, metadata_mime_type, media_mimetype)
    response_object = {
        'ok': True,
        'message': 'File rendered and uploaded in GDrive.',
        'link': link
    }
    resp = send_message.send('Nouveau document généré sur IdéSYS-ERP : ' + link, 'zapier-test')
    print(resp)
    doc = Document(title=post_data['name'], path=output_path, link=link, type=post_data['type'], status="created")
    doc.save()
    return make_response(jsonify(response_object))

@api_blueprint.route('/render/pptx', methods=['POST'])
@api_post_data_middleware()
def pptx():
    # get the post data
    post_data = request.get_json()
    output_path = render_pptx(post_data['type'], post_data['data'], post_data['name'])
    scopes = ['https://www.googleapis.com/auth/drive']
    metadata_mime_type = 'application/vnd.google-apps.presentation'
    media_mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    creds = credentials.get_delegated_credentials(scopes)
    link = gdrive.upload(creds, output_path, metadata_mime_type, media_mimetype)
    response_object = {
        'ok': True,
        'message': 'File rendered and uploaded in GDrive.',
        'link': link
    }
    resp = send_message.send('Nouveau document généré sur IdéSYS-ERP : ' + link, 'zapier-test')
    print(resp)
    doc = Document(title=post_data['name'], path=output_path, link=link, type=post_data['type'], status="created")
    doc.save()
    return make_response(jsonify(response_object))

@api_blueprint.route('/documents/<type>', methods=['GET'])
def documents(type):
    docs = Document.objects(type=type)
    response_object = {
        'ok': True,
        'data': docs
    }
    return make_response(jsonify(response_object))


@api_blueprint.route('/documents/validate', methods=['PUT'])
@api_post_data_middleware()
def validate():
    post_data = request.get_json()
    doc_id = post_data['id']
    doc = Document.get_document_by_id(doc_id)
    if g.user.can_validate:
        doc.status = "validated"
        doc.save()
        response_object = {
            'ok': True,
            'data': {
                'document': doc,
            }
        }
        return make_response(jsonify(response_object))
    response_object = {
        'ok': False,
        'error': "User can't validate document"
    }
    return make_response(jsonify(response_object), 403)


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# @api_blueprint.route('/upload-template/<str:type>', methods=['POST'])
# def upload_template(type):
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         return {'ok': False, 'message': 'no file part'}
#
#     file = request.files['file']
#     # if user does not select file, browser also submit an empty part without filename
#     if file.filename == '':
#         return {'ok': False, 'message': 'no selected file'}
#
#     if type not in ALLOWED_TYPE:
#         return {'ok': False, 'message': 'type not allowed'}
#
#     if file and allowed_file(file.filename):
#         type = secure_filename(type)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'template', type))
#         return {'ok': True, 'message': 'file saved'}
#     return {'ok': False, 'message': 'extension file not allowed'}
