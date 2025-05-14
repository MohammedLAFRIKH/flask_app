from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def accueil():
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/health')
def health_check():
    return jsonify({"status": "OK"}), 200
