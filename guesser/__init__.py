import os

from flask import Flask


def create_app(test_config=None):
    """Application factory function"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import predict
    app.register_blueprint(predict.BP)

    return app
