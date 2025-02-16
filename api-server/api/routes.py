import os
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from services.database_service import *
from services.chat_service import *
api_bp = Blueprint('api', __name__)

UPLOAD_FOLDER = 'upload_files'
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    register_user(username, password)
    return jsonify({'message': 'User created successfully'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = get_user(username)

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    return jsonify({'message': 'Login successful', 'user_id': user['id']}), 200

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    user_id = request.form.get('user_id')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and user_id:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 400

        create_file(user_id, filename, filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename, 'filepath': filepath}), 201
    else:
        return jsonify({'error': 'User ID is required'}), 400


@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    user_id = data.get('user_id')
    pdf_paths = data.get('pdf_paths')
    language = data.get('language')
    context_length = data.get('context_length')
    include_history = data.get('include_history')
    chat_tab_id = data.get('chat_tab_id')

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 400

    if not chat_tab_id:
        chat_tab_id = create_chat_tab(user_id, f'New Chat')
    refrence=[]
    if pdf_paths and len(pdf_paths) > 0:
        ai_response, refrence = get_rag_response(user_message, pdf_paths, language, context_length, include_history,chat_tab_id)
    else:
        ai_response = get_gemini_response(user_message, language, context_length, include_history,chat_tab_id)

    create_message(user_id, chat_tab_id, user_message, ai_response, str(refrence));
    return jsonify({'response': ai_response, 'refrence': str(refrence),"chat_tab_id":chat_tab_id})

@api_bp.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM user")
    users = cursor.fetchall()
    conn.close()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user['id']
        user_data['username'] = user['username']
        output.append(user_data)
    return jsonify({'users': output})

@api_bp.route('/files', methods=['GET'])
def get_files():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    files = get_files_by_user_id(user_id)
    output = []
    for file in files:
        file_data = {}
        file_data['id'] = file['id']
        file_data['filename'] = file['filename']
        file_data['filepath'] = file['filepath']
        output.append(file_data)
    return jsonify({'files': output})

@api_bp.route('/chat_history', methods=['GET'])
def get_chat_history_route():
    user_id = request.args.get('user_id')
    chat_tab_id = request.args.get('chat_tab_id')

    if not user_id or not chat_tab_id:
        return jsonify({'error': 'User ID and Chat Tab ID are required'}), 400

    messages = get_chat_history(user_id, chat_tab_id)
    output = []
    for message in messages:
        message_data = {}
        message_data['id'] = message['id']
        message_data['user_message'] = message['user_message']
        message_data['ai_response'] = message['ai_response']
        message_data['refrence'] = message['refrence']
        output.append(message_data)
    return jsonify({'chat_history': output})

@api_bp.route('/chat_tabs', methods=['GET'])
def get_chat_tabs_route():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    chat_tabs = get_chat_tabs(user_id)
    output = []
    for chat_tab in chat_tabs:
        chat_tab_data = {}
        chat_tab_data['id'] = chat_tab['id']
        chat_tab_data['tab_name'] = chat_tab['tab_name']
        output.append(chat_tab_data)
    return jsonify({'chat_tabs': output})

@api_bp.route('/delete_chat_tab', methods=['POST'])
def delete_chat_tab_route():
    data = request.get_json()
    chat_tab_id = data.get('chat_tab_id')
    print(chat_tab_id)
    if not chat_tab_id:
        return jsonify({'error': 'Chat Tab ID is required'}), 400

    delete_chat_tab(chat_tab_id)
    return jsonify({'message': 'Chat Tab deleted successfully'}), 200

@api_bp.route('/edit_chat_tab', methods=['POST'])
def edit_chat_tab_route():
    data = request.get_json()
    chat_tab_id = data.get('chat_tab_id')
    tab_name =data.get('tab_name')
    if not chat_tab_id or not tab_name:
        return jsonify({'error': 'Chat Tab ID and Tab Name are required'}), 400

    edit_chat_tab(chat_tab_id, tab_name)
    return jsonify({'message': 'Chat Tab edited successfully'}), 200
