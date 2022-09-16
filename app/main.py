# Public Imports
from flask import Flask

# Private Imports
from routes import blueprint


def main():
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    app.run(debug=True)


if __name__ == '__main__':
    main()
