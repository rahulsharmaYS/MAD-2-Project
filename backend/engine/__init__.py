import os
import redis
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_restful import Api
from .config import Config
from .database import db
from .models import User, Role, add_default_roles
import engine.workers as workers
from celery import Celery
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_mail import Mail


app = None
api = None
celery = None
cache = Cache()
jwt = None
mail = Mail()

load_dotenv()

def create_admin():
    try:
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)
        
        db.session.commit()

        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@mad2.com',
                password='1234',
                role_id=admin_role.id
            )
            admin_user.set_password('1234')
            db.session.add(admin_user)
            db.session.commit()
            print("admin and roles added to the database.")
        else:
            print("admin already exists in the db")

    except Exception as e:
        db.session.rollback()
        print(f"error adding admin user and roles: {str(e)}")


def create_app():
    global celery, cache, jwt, mail
    
    app = Flask(__name__)
    app.secret_key = 'sponsornet'
    allowed_origins = ["http://localhost:5173"]
    app.config.from_object(Config)


    CORS(app, resources={r"/*": {"origins": allowed_origins}})
    if os.getenv('ENV', 'development') == 'production':
        raise Exception('not configured')
    else:
        print('Starting in development mode')
        app.config.from_object(Config)
    app.app_context().push()
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_admin()
        add_default_roles()

    api = Api(app)    
    jwt = JWTManager(app)  


    celery = workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.Task = workers.ContextTask
    # app.app_context().push()

    redis_connection = redis.Redis(host='localhost', port=6379, db=0)
    user = redis_connection.get('user')
    print(f"hello from redis: {user}")
    app.redis = redis_connection
    app.app_context().push()
    cache.init_app(app)
    print("Cache initialized")

    app.app_context().push()

    mail.init_app(app)

    from .resources import initialize_resources
    initialize_resources(api)

    return app, api, celery, cache


app, api, celery, cache = create_app()
