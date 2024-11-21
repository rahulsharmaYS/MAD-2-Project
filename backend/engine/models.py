from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, event, Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import base64
import re
from .database import db
import random
import string

class Role(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    users = relationship('User', backref='role', lazy=True)
    sponsors = relationship('Sponsor', backref='role', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'role': self.name
        }
    
class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    userhandle = Column(String(80), nullable=True, default=lambda: 'influencer_'+ ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    password = Column(String(200), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    bio = Column(String(500), nullable=True, default="Enter something good to attract sponsors!")
    phone = Column(String(20), nullable=True)
    instagram = Column(String(150), nullable=True)
    youtube = Column(String(150), nullable=True)
    twitter = Column(String(150), nullable=True)
    profilePicUrl = Column(db.Text, nullable=True)
    niche = Column(String(150))
    reach = Column(Integer, nullable=True, default=0)
    earnings = Column(Integer, nullable=True, default=0)
    campaigns = relationship('Campaign', backref='user', lazy=True)
    requests = relationship('CampaignRequest', backref='user', lazy=True)
    is_banned = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False, default=2)
    

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
        'id': self.id,
        'username': self.username,
        'email': self.email,
        'bio': self.bio,
        'phone': self.phone,
        'socialMedia': {
            'instagram': self.instagram,
            'youtube': self.youtube,
            'twitter': self.twitter
        },
        'profilePicUrl': self.profilePicUrl,
        'niche': self.niche,
        'is_banned': self.is_banned,
        'userhandle': self.userhandle,
        'reach': self.reach,
        'earnings': self.earnings
        }

class Sponsor(db.Model):
    sponsor_id = Column(String(80), primary_key=True)
    sponsor_name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    industry = Column(String(50), nullable=False)
    companyName = Column(String(100), nullable=False)
    companyWebsite = Column(String(200), nullable=False)
    contactNumber = Column(String(20), nullable=False)
    profilePicUrl = Column(db.Text, nullable=True)
    campaigns = relationship('Campaign', backref='sponsor', lazy=True)
    requests = relationship('CampaignRequest', backref='sponsor', lazy=True)
    is_banned = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False, default=3)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            'sponsor_id': self.sponsor_id,
            'sponsor_name': self.sponsor_name,
            'email': self.email,
            'industry': self.industry,
            'companyName': self.companyName,
            'companyWebsite': self.companyWebsite,
            'contactNumber': self.contactNumber,
            'profilePicUrl': self.profilePicUrl,
            'is_banned': self.is_banned
        }


class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(200), nullable=False)
    progress = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    ad_title = db.Column(db.String(200), nullable=False)
    ad_description = db.Column(db.Text, nullable=False)
    terms_and_conditions = db.Column(db.Text, nullable=False)
    payment = db.Column(db.String(50), nullable=False)
    negotiated_price = db.Column(db.Float)
    user_id = db.Column(db.String(200), db.ForeignKey('user.username'), nullable=True)
    sponsor_id = db.Column(db.String(80), db.ForeignKey('sponsor.sponsor_id'), nullable=False)
    requests = db.relationship('CampaignRequest', backref='campaign', lazy=True)
    flagged = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            # 'id': self.id,
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'ad_title': self.ad_title,
            'ad_description': self.ad_description,
            'terms_and_conditions': self.terms_and_conditions,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'payment': self.payment,
            'sponsor_id': self.sponsor_id,
            'is_active': self.is_active,
            'is_private': self.is_private,
            'flagged': self.flagged,
            'negotiated_price': self.negotiated_price,
        }

class CampaignRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_req_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'))
    campaign_name = db.Column(db.String(200), nullable=False)
    ad_title = db.Column(db.String(200), nullable=False)
    ad_description = db.Column(db.Text, nullable=False)
    terms_and_conditions = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    negotiated_price = db.Column(db.Float, nullable=False)
    payment = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Pending')
    user_id = db.Column(db.String(200), db.ForeignKey('user.username'), nullable=True)
    sponsor_id = db.Column(db.String(80), db.ForeignKey('sponsor.sponsor_id'), nullable=False)
    last_negotiated_by = db.Column(db.String(200), nullable=True)  # Add this line

    def serialize(self):
        user = User.query.filter_by(username=self.user_id).first() if self.user_id else None
        return {
            # 'id': self.id,
            'campaign_req_id': self.campaign_req_id,
            'campaign_name': self.campaign_name,
            'ad_description': self.ad_description,
            'terms_and_conditions': self.terms_and_conditions,
            'payment': self.payment,
            'status': self.status,
            'user_id': self.user_id,
            'sponsor_id': self.sponsor_id,
            'negotiated_price': self.negotiated_price,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'user':{
                'niche': user.niche if user else None,
                'userhandle': user.userhandle if user else None,
                'email': user.email if user else None
            } if user else None,
            'ad_title': self.ad_title,
            'last_negotiated_by': self.last_negotiated_by
        }



class SponsorApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    companyName = db.Column(db.String(100), nullable=False)
    companyWebsite = db.Column(db.String(200), nullable=False)
    contactNumber = db.Column(db.String(20), nullable=False)


# class BannedUser(db.Model):
#     id = Column(Integer, primary_key=True)
#     username = Column(String(80), unique=True, nullable=False)
#     userhandle = Column(String(80), nullable=True, default=lambda: 'influencer_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
#     password = Column(String(200), nullable=False)
#     email = Column(String(120), unique=True, nullable=False)
#     bio = Column(String(500), nullable=True, default="Enter something good to attract sponsors!")
#     phone = Column(String(20), nullable=True)
#     instagram = Column(String(150), nullable=True)
#     youtube = Column(String(150), nullable=True)
#     twitter = Column(String(150), nullable=True)
#     profilePicUrl = Column(db.Text, nullable=True)
#     niche = Column(String(150))
#     is_banned = Column(Boolean, default=False)
#     role_id = Column(Integer, ForeignKey('role.id'), nullable=False, default=2)

# class BannedSponsor(db.Model):
#     sponsor_id = Column(Integer, primary_key=True)
#     sponsor_name = Column(String(80), unique=True, nullable=False)
#     email = Column(String(120), unique=True, nullable=False)
#     password = Column(String(200), nullable=False)
#     industry = Column(String(50), nullable=False)
#     companyName = Column(String(100), nullable=False)
#     companyWebsite = Column(String(200), nullable=False)
#     contactNumber = Column(String(20), nullable=False)
#     profilePicUrl = Column(db.Text, nullable=True)
#     is_banned = Column(Boolean, default=False)
#     role_id = Column(Integer, ForeignKey('role.id'), nullable=False, default=3)



def add_default_roles(*args, **kwargs):
    print("Adding default roles...")
    roles = ['admin', 'user', 'sponsor']
    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            try:
                role = Role(name=role_name)
                db.session.add(role)
                db.session.commit()
                print(f"{role_name.capitalize()} role added to the database.")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding {role_name} role: {str(e)}")

def add_admin_user(*args, **kwargs):
    print("Adding admin user...")
    admin_username = 'admin'
    admin_password = '1234'
    admin_email = 'admin@mad2.com'
    admin_role = Role.query.filter_by(name='admin').first()

    admin_user = User.query.filter_by(username=admin_username).first()
    if admin_user is None:
        try:
            admin_user = User(username=admin_username, email=admin_email)
            admin_user.set_password(admin_password)
            admin_user.role_id = admin_role.id
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user '{admin_username}' with password '{admin_password}' added to the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding admin user: {str(e)}")
    else:
        print(f"Admin user '{admin_username}' already exists in the database.")

# listen for after_create event to add roles and admin user
event.listen(db.metadata, 'after_create', add_default_roles)
event.listen(db.metadata, 'after_create', add_admin_user)
