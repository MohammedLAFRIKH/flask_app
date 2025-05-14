from flask import Flask
from routes.main import main_bp  # Import the blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
