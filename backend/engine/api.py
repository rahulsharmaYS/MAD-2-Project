from flask import request, jsonify, Flask, Blueprint, make_response
from flask_restful import Resource, reqparse, Api
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, cache
from .models import User, Sponsor, SponsorApplication, Campaign, CampaignRequest, Role
import matplotlib.pyplot as plt
import io
import base64
from .auth import token_required
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging
from flask import jsonify, Response
import json

logging.basicConfig(level=logging.DEBUG)


#  <----------------------------------User Resources------------------------------------->

class RegisterUserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        niche = data.get('niche')
        social_media = data.get('social_media', {})
        
        if User.query.filter_by(username=username).first():
            return {'status': False, 'error': 'Username already exists'}, 400

        if username.isdigit():
            return {'status': False, 'error': 'Username cannot be an integer'}, 400

        if User.query.filter_by(email=email).first():
            return {'status': False, 'error': 'Email already exists'}, 400

        role = Role.query.filter_by(name='user').first()
        if not role:
            return {'status': False, 'error': 'User role does not exist'}, 500
        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            user = User(
                username=username, 
                email=email, 
                niche=niche,
                instagram=social_media.get('instagram'),
                youtube=social_media.get('youtube'),
                twitter=social_media.get('twitter')
            )
            user.password = hashed_password
            user.role_id = role.id            
            db.session.add(user)
            db.session.commit()

            return {'status': True, 'message': 'User registered successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'status': False, 'error': str(e)}, 500

class UserDashboardResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"error": "user not found."}, 404

        active_campaigns = CampaignRequest.query.filter_by(user_id=username, status='Active').all()
        renegotiated_requests = CampaignRequest.query.filter(
            CampaignRequest.user_id == username,
            CampaignRequest.last_negotiated_by != username,
            CampaignRequest.status == 'Pending'
        ).all()

        active_campaigns_data = [campaign.serialize() for campaign in active_campaigns]
        renegotiated_requests_data = [req.serialize() for req in renegotiated_requests]
        return {"active_campaigns": active_campaigns_data, "renegotiated_requests": renegotiated_requests_data}, 200

    def put(self, username):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "unauthorized"}, 401

        data = request.json
        print(f"Data: {data}")
        action = data.get('action')
        campaign_id = data.get('campaign_id')
        # if not campaign_id:
        #     return {"error": "Campaign ID is required."}, 400

        if action == 'accept':
            print("Accepting campaign.")
            return self.accept_campaign(username, campaign_id)
        elif action == 'reject':
            return self.reject_campaign(username, campaign_id)
        elif action == 'renegotiate':
            new_price = data.get('new_price')
            print(f"New Price: {new_price}")
            campaign_req_id = data.get('campaign_req_id')

            if not new_price:
                return {"error": "new price is required for renegotiation"}, 400
            return self.renegotiate_campaign(username, campaign_req_id, new_price)
        elif action == 'cancel':
            return self.cancel_campaign(username, campaign_id)
        else:
            return {"error": "Invalid action."}, 400

    def renegotiate_campaign(self, username, campaign_req_id, new_price):
        new_price = float(new_price)
        print(f"New Price: {new_price}")
        campaign = CampaignRequest.query.filter_by(campaign_req_id=campaign_req_id, user_id=username, status='Pending').first()
        print(f"Campaign: {campaign}")
        if not campaign:
            print("campaign not found.")
            return {"error": "campaign not found."}, 404

        if campaign.status != 'Pending':
            print("Campaign is not in a negotiable state.")
            return {"error": "campaign is not in negotiable state."}, 400
        

        campaign.negotiated_price = new_price
        campaign.last_negotiated_by = username
        db.session.commit()

        return {"message": "price renegotiated."}, 200

    def accept_campaign(self, username, campaign_id):
        campaign = CampaignRequest.query.filter_by(campaign_req_id=campaign_id,status='Pending', user_id=username).first()
        print(f"Campaign: {campaign}")
        if not campaign:
            return {"error": "not found or not pending."}, 404

        campaign.status = 'Active'
        db.session.commit()

        return {"message": "status updated to active."}, 200

    def reject_campaign(self, username, campaign_id):
        campaign = CampaignRequest.query.filter_by(campaign_req_id=campaign_id, user_id=username, status='Pending').first()
        if not campaign:
            return {"error": "not found."}, 404
        campaign.status = 'Cancelled'
        db.session.commit()

        return {"message": "request rejected."}, 200

    def cancel_campaign(self, username, campaign_id):
        campaign = CampaignRequest.query.filter_by(campaign_req_id=campaign_id, user_id=username, status='Active').first()
        if not campaign:
            return {"error": "not found."}, 404

        campaign.status = 'Cancelled'
        db.session.commit()

        return {"message": "canceled successfully."}, 200

class ProfileResource(Resource):
    @cache.cached(timeout=10, key_prefix='profile')
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        user_data = user.serialize()
        if user_data.get('profilePicUrl'):
            user_data['profilePicUrl'] = user_data['profilePicUrl']

        return jsonify(user_data)

    def put(self, username):
        data = request.json
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        if 'profilePicUrl' in data:
            profile_pic_data = data['profilePicUrl']
            if profile_pic_data is not None:
                user.profilePicUrl = profile_pic_data

        user.userhandle = data.get('userhandle', user.userhandle)
        user.bio = data.get('bio', user.bio)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.instagram = data.get('socialMedia', {}).get('instagram', user.instagram)
        user.youtube = data.get('socialMedia', {}).get('youtube', user.youtube)
        user.twitter = data.get('socialMedia', {}).get('twitter', user.twitter)
        user.niche = data.get('niche', user.niche)
        user.reach = data.get('reach', user.reach)

        db.session.commit()
        cache.clear()
        return jsonify(user.serialize())

class UserFindResource(Resource):
    def get(self, username):
        users = User.query.filter_by(is_banned=0).all()
        sponsors = Sponsor.query.filter_by(is_banned=False).all()

        valid_niches = ['Fashion', 'Beauty', 'Fitness', 'Food', 'Travel', 'Gaming', 'Technology', 'Lifestyle', 'Education', 'Health']
        filtered_users = [self.serialize_user(user) for user in users if user.niche in valid_niches]

        serialized_sponsors = [self.serialize_sponsor(sponsor) for sponsor in sponsors]

        return jsonify({
            'users': filtered_users,
            'sponsors': serialized_sponsors
        })

    def serialize_user(self, user):
        return {
            'id': user.id,
            'username': user.username,
            'userhandle': user.userhandle or user.username,
            'email': user.email,
            'bio': user.bio,
            'phone': user.phone,
            'socialMedia': {
                'instagram': self.ensure_http_prefix(user.instagram),
                'youtube': self.ensure_http_prefix(user.youtube),
                'twitter': self.ensure_http_prefix(user.twitter)
            },
            'profilePicUrl': self.decode_base64(user.profilePicUrl),
            'niche': user.niche,
            'is_banned': user.is_banned
        }

    def serialize_sponsor(self, sponsor):
        return {
            'sponsor_id': sponsor.sponsor_id,
            'sponsor_name': sponsor.sponsor_name,
            'email': sponsor.email,
            'industry': sponsor.industry,
            'companyName': sponsor.companyName,
            'companyWebsite': self.ensure_http_prefix(sponsor.companyWebsite),
            'contactNumber': sponsor.contactNumber,
            'profilePicUrl': self.decode_base64(sponsor.profilePicUrl),
            'is_banned': sponsor.is_banned
        }

    def decode_base64(self, base64_string):
        if not base64_string:
            return None
        try:
            if base64_string.startswith("data:image"):
                return base64_string
            return f"data:image/png;base64,{base64_string}"
        except Exception as e:
            print(f"Error decoding base64: {e}")
            return None

    def ensure_http_prefix(self, url):
        if url and not url.startswith(('http://', 'https://')):
            return f"http://{url}"
        return url

class UserStatsResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        # print(f"user: {user}")
        if not user:
            return jsonify({"error": "User not found."}), 404

        userreach = user.reach
        user_earnings = user.earnings
        negotiated_prices = [campaign.negotiated_price for campaign in CampaignRequest.query.filter_by(user_id=user.username, status='Active').all()]
        print(user_earnings, negotiated_prices)
        userearning = user_earnings + sum(negotiated_prices)
        usercampaigns = CampaignRequest.query.filter_by(user_id=user.username, status='Active').all()
        serialized_campaigns = [campaign.serialize() for campaign in usercampaigns]
        print(f"User campaigns: {usercampaigns}")


        stats_data = {
            "reach": userreach,
            "expectedearning": userearning,
            "campaigns": serialized_campaigns,
            "earning": user_earnings
        }
        response = jsonify(stats_data)
        return response

class FindCampaignsResource(Resource):
    def get(self, username):
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                return {'message': 'User not found'}, 404
            
            campaigns = Campaign.query.filter_by(is_active=True).all()
            serialized_campaigns = []
            for campaign in campaigns:
                print(campaign.sponsor_id)
                sponsor = Sponsor.query.filter_by(sponsor_name = campaign.sponsor_id).first()
                print(sponsor)
                sponsor_data = {
                    'sponsor_id': sponsor.sponsor_id if sponsor else None,
                    'sponsor_name': sponsor.sponsor_name if sponsor else None,
                    'email': sponsor.email if sponsor else None,
                    'industry': sponsor.industry if sponsor else None,
                    'companyName': sponsor.companyName if sponsor else None,
                    'companyWebsite': sponsor.companyWebsite if sponsor else None,
                    'contactNumber': sponsor.contactNumber if sponsor else None,
                    'profilePicUrl': self.decode_base64(sponsor.profilePicUrl) if sponsor else None  # Decode base64 URL
                }

                serialized_campaigns.append({
                    'campaign_id': campaign.campaign_id,
                    'campaign_name': campaign.campaign_name,
                    'progress': campaign.progress,
                    'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                    'end_date': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
                    'ad_title': campaign.ad_title,
                    'ad_description': campaign.ad_description,
                    'terms_and_conditions': campaign.terms_and_conditions,
                    'payment': campaign.payment,
                    'user_id': campaign.user_id,
                    'sponsor': sponsor_data,
                    'flagged': campaign.flagged,
                    'is_private': campaign.is_private,
                    'is_active': campaign.is_active
                })

            return jsonify({'campaigns': serialized_campaigns})

        except Exception as e:
            print(f"Error: {e}") 
            return {'error': str(e)}, 500


    def post(self, username):
        try:
            data = request.get_json()
            print(f"Received data: {data}")

            campaign_id = data.get('campaign_id')
            proposed_price = data.get('proposed_price')
            influencer_id = data.get('influencer_id')

            print(f"Campaign ID: {campaign_id}, Proposed Price: {proposed_price}, Influencer ID: {influencer_id}")

            if not isinstance(campaign_id, int):
                return {'message': 'Invalid campaign_id type'}, 400
            if proposed_price is not None and not isinstance(proposed_price, (int, float)):
                return {'message': 'Invalid proposed_price type'}, 400
            if not isinstance(influencer_id, str):
                return {'message': 'Invalid influencer_id type'}, 400

            if not campaign_id or not influencer_id:
                return {'message': 'Missing required fields'}, 400

            campaign = Campaign.query.filter_by(campaign_id=campaign_id).first()
            if not campaign:
                return {'message': 'Campaign not found'}, 404

            campaign_request = CampaignRequest.query.filter_by(campaign_req_id=campaign_id, user_id=influencer_id, status='Pending').first()

            if proposed_price is not None:
                if campaign_request:
                    campaign_request.negotiated_price = proposed_price
                    campaign_request.payment = campaign.payment  
                    campaign_request.last_negotiated_by = influencer_id
                else:
                    campaign_request = CampaignRequest(
                        campaign_req_id=campaign_id,
                        campaign_name=campaign.campaign_name,
                        ad_title=campaign.ad_title,
                        ad_description=campaign.ad_description,
                        terms_and_conditions=campaign.terms_and_conditions,
                        start_date=campaign.start_date,
                        end_date=campaign.end_date,
                        payment=campaign.payment,  
                        negotiated_price=proposed_price,
                        user_id=influencer_id,
                        sponsor_id=campaign.sponsor_id,
                        last_negotiated_by=influencer_id
                    )
                    db.session.add(campaign_request)
            else:
                if campaign_request:
                    campaign_request.negotiated_price = campaign.payment
                    campaign_request.payment = campaign.payment 
                    campaign_request.last_negotiated_by = influencer_id
                else:
                    campaign_request = CampaignRequest(
                        campaign_req_id=campaign_id,
                        campaign_name=campaign.campaign_name,
                        ad_title=campaign.ad_title,
                        ad_description=campaign.ad_description,
                        terms_and_conditions=campaign.terms_and_conditions,
                        start_date=campaign.start_date,
                        end_date=campaign.end_date,
                        payment=campaign.payment,  
                        negotiated_price=campaign.payment,
                        user_id=influencer_id,
                        sponsor_id=campaign.sponsor_id,
                        last_negotiated_by=influencer_id
                    )
                    db.session.add(campaign_request)
            db.session.commit()

            return {'message': 'Request submitted successfully'}, 200

        except Exception as e:
            print(f"Error processing request: {e}")
            return {'error': str(e)}, 500

    def decode_base64(self, base64_string):
        if not base64_string:
            return None
        try:
            if base64_string.startswith("data:image"):
                return base64_string
            return f"data:image/png;base64,{base64_string}"
        except Exception as e:
            print(f"Error decoding base64: {e}")
            return None

class LogoutUserResource(Resource):
    @jwt_required()
    def post(self):
        return jsonify({"message": "Logout successful"}), 200
    

# <----------------------------------Sponsor Resources------------------------------------->

from flask import jsonify, Response
import json
from .auth import create_jwt_token
from flask import request, Response
import logging
class LoginSponsorResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            print(f"Data: {data}")
            sponsorname = data.get('sponsorname')
            password = data.get('password')

            if not sponsorname or not password:
                return jsonify({'status': False, 'error': 'Missing sponsorname or password'}), 400

            sponsor = Sponsor.query.filter_by(sponsor_name=sponsorname).first()
            print(f"Sponsor: {sponsor}")
            if sponsor and sponsor.check_password(password):
                access_token = create_jwt_token(sponsor)
                response_data = {
                    'status': True,
                    'role_id': sponsor.role_id,
                    'username': sponsor.sponsor_name,
                    'access_token': access_token,
                    'is_banned': sponsor.is_banned
                }
                logging.debug(f'Response Data: {response_data}')
                return jsonify(response_data)
            else:
                return jsonify({'status': False, 'error': 'Invalid sponsorname or password'}), 400
        except Exception as e:
            logging.error(f'Exception occurred: {e}')
            return jsonify({'status': False, 'error': 'Internal server error'}), 500

class SponsorRegisterResource(Resource):
    def post(self):
        data = request.get_json()

        required_fields = ['sponsorname', 'email', 'password', 'industry', 'companyName', 'companyWebsite', 'contactNumber']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing field: {field}'}, 400

        sponsorname = data['sponsorname']
        email = data['email']

        sponsor_exists = Sponsor.query.filter_by(sponsor_name=sponsorname).first() or Sponsor.query.filter_by(email=email).first()

        print(f"Sponsor Exists: {sponsor_exists}")
        user_exists = User.query.filter_by(username=sponsorname).first()

        if sponsor_exists:
            return {'error': 'Sponsor name or email already exists.'}, 400
        if user_exists:
            return {'error': 'Username already exists.'}, 400

        new_application = SponsorApplication(
            sponsor_name=sponsorname,
            email=email,
            password=data['password'],
            industry=data['industry'],
            companyName=data['companyName'],
            companyWebsite=data['companyWebsite'],
            contactNumber=data['contactNumber']
        )

        try:
            db.session.add(new_application)
            db.session.commit()
            return {'message': 'Application submitted successfully!'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': 'An error occurred while processing your request.'}, 500

def allowed_file(filename):
    # this checks if the file extension is allowed or not!! 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

class SponsorDashboardResource(Resource):
    def get(self, sponsorname, campaign_id=None, user_id=None):
        sponsor = Sponsor.query.filter_by(sponsor_name=sponsorname).first()
        if not sponsor:
            return {"error": "Sponsor not found."}, 404

        if campaign_id:
            campaign = CampaignRequest.query.filter_by(id=campaign_id, sponsor_id=sponsor.sponsor_name).first()
            if not campaign:
                return {"error": "Campaign not found."}, 404
            return {'campaign': campaign.serialize()}

        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return {"error": "User not found."}, 404
            return {'user': user.serialize()}

        active_requests = CampaignRequest.query.filter_by(sponsor_id=sponsor.sponsor_name, status='Active').all()
        new_requests = CampaignRequest.query.filter(
            CampaignRequest.sponsor_id == sponsor.sponsor_name,
            CampaignRequest.status == 'Pending',
            CampaignRequest.last_negotiated_by != sponsor.sponsor_name
        ).all()
        sent_requests = CampaignRequest.query.filter(
            CampaignRequest.sponsor_id == sponsor.sponsor_name,
            CampaignRequest.status == 'Pending',
            CampaignRequest.last_negotiated_by == sponsor.sponsor_name
        ).all()

        new_requests_with_user = []
        for request in new_requests:
            user = User.query.filter_by(id=request.user_id).first()
            user_data = user.serialize() if user else {}
            request_data = request.serialize()
            request_data['user'] = user_data
            new_requests_with_user.append(request_data)

        response_data = {
            'activeRequests': [request.serialize() for request in active_requests],
            'newRequests': new_requests_with_user,
            'sentRequests': [request.serialize() for request in sent_requests]
        }
        return response_data, 200

    def post(self, sponsorname):
        try:
            action = request.json.get('action')
            request_id = request.json.get('request_id')
            new_price = request.json.get('new_price')
            new_strt_date = request.json.get('new_start_date')
            new_end_date = request.json.get('new_end_date')
            user_id = request.json.get('user_id')
            print(f"Action: {action}, Request ID: {request_id}, New Price: {new_price}, User ID: {user_id}")
            print(f"New Start Date: {new_strt_date}, New End Date: {new_end_date}")

            campaign_request = CampaignRequest.query.filter_by(campaign_req_id=request_id, sponsor_id=sponsorname, user_id=user_id, status='Pending').first()
            print(f"Campaign Request: {campaign_request}")

            # if not campaign_request:
            #     return {"error": "Request not found."}, 404

            if action == 'renegotiate':
                if new_price is None or not isinstance(new_price, (int, float)):
                    return {"error": "Invalid new price."}, 400
                campaign_request.negotiated_price = new_price
                campaign_request.payment = new_price
                if new_strt_date:
                    campaign_request.start_date = datetime.strptime(new_strt_date, '%Y-%m-%d')
                if new_end_date:
                    campaign_request.end_date = datetime.strptime(new_end_date, '%Y-%m-%d')
                campaign_request.status = 'Pending'
                campaign_request.last_negotiated_by = sponsorname
            elif action == 'accept':
                campaign_request.status = 'Active'
            elif action == 'reject':
                campaign_request.status = 'Cancelled'


            elif action == 'delete':
                db.session.delete(campaign_request)
            else:
                campaign = CampaignRequest.query.filter(CampaignRequest.campaign_req_id == request_id, CampaignRequest.sponsor_id == sponsorname, CampaignRequest.status == 'Active', CampaignRequest.user_id == user_id).first()
                print(f"Campaign: {campaign}")
                if action == 'cancel':
                    campaign.status = 'Cancelled'
                elif action == 'complete':
                    campaign.status = 'Completed'
                    user = User.query.filter_by(username=user_id).first()
                    user.earnings += campaign.negotiated_price
                    user.reach += 100

            db.session.commit()

            active_requests = CampaignRequest.query.filter_by(sponsor_id=sponsorname, status='Active').all()
            sent_requests = CampaignRequest.query.filter_by(sponsor_id=sponsorname, status='Pending', last_negotiated_by=sponsorname).all()

            response_data = {
                'activeRequests': [req.serialize() for req in active_requests],
                'sentRequests': [req.serialize() for req in sent_requests],
                'newRequests': [req.serialize() for req in sent_requests]
            }

            return response_data, 200

        except Exception as e:
            print(f"Exception: {e}")
            return {"error": "An unexpected error occurred."}, 500

class SponsorProfileResource(Resource):
    @cache.cached(timeout=10)
    def get(self, sponsorname):
        sponsor = Sponsor.query.filter_by(sponsor_name=sponsorname).first()
        if not sponsor:
            return {'message': 'Sponsor not found'}, 404

        sponsor_data = sponsor.serialize()
        if sponsor_data.get('profilePicUrl'):
            sponsor_data['profilePicUrl'] = sponsor_data['profilePicUrl']
        
        return jsonify(sponsor_data)

    def put(self, sponsorname):
        data = request.json
        sponsor = Sponsor.query.filter_by(sponsor_name=sponsorname).first()
        if not sponsor:
            return {'message': 'Sponsor not found'}, 404

        if 'profilePicUrl' in data:
            profile_pic_data = data['profilePicUrl']
            if profile_pic_data is not None:
                sponsor.profilePicUrl = profile_pic_data


        sponsor.companyName = data.get('companyName', sponsor.companyName)
        sponsor.companyWebsite = data.get('companyWebsite', sponsor.companyWebsite)
        sponsor.email = data.get('email', sponsor.email)
        sponsor.contactNumber = data.get('contactNumber', sponsor.contactNumber)
        sponsor.industry = data.get('industry', sponsor.industry)

        db.session.commit()
        cache.clear()
        return jsonify(sponsor.serialize())

from flask import jsonify
from base64 import b64encode, b64decode

class SponsorFindResource(Resource):
    def get(self, sponsorname):

        users = User.query.filter_by(is_banned=False, role_id=2).all()
        serialize_users = [self.serialize_user(user) for user in users]
        sponsors = Sponsor.query.filter_by(is_banned=False).all()

        valid_niches = ['Fashion', 'Beauty', 'Fitness', 'Food', 'Travel', 'Gaming', 'Technology', 'Lifestyle', 'Education', 'Health']
        serialized_sponsors = [self.serialize_sponsor(sponsor) for sponsor in sponsors]
        campaigns = Campaign.query.filter_by(sponsor_id=sponsorname).all()
        serialized_campaigns = [self.serialize_campaign(campaign) for campaign in campaigns]
        # print(f"users: {filtered_users}")
        return jsonify({
            'users':serialize_users,
            'sponsors': serialized_sponsors,
            'campaigns': serialized_campaigns
        })

    def post(self, sponsorname):
        data = request.get_json()
        influencer_username = data.get('influencer')
        campaign_id = data.get('campaign_id')

        user = User.query.filter_by(username=influencer_username).first()
        campaign = Campaign.query.filter_by(campaign_id=campaign_id, sponsor_id=sponsorname).first()

        if not user or not campaign:
            return {'message': 'User or campaign not found'}, 404

        existing_request = CampaignRequest.query.filter_by(
            campaign_req_id=campaign_id,
            sponsor_id=sponsorname,
            user_id=influencer_username
        ).first()

        if existing_request:
            existing_request.campaign_name = campaign.campaign_name
            existing_request.ad_title = campaign.ad_title
            existing_request.ad_description = campaign.ad_description
            existing_request.terms_and_conditions = campaign.terms_and_conditions
            existing_request.payment = campaign.payment
            existing_request.start_date = campaign.start_date
            existing_request.end_date = campaign.end_date
            existing_request.negotiated_price = campaign.payment
            existing_request.status = 'Pending'
            existing_request.user_id = user.username
            existing_request.last_negotiated_by = sponsorname
        else:
            campaign_request = CampaignRequest(
                campaign_req_id=campaign_id,
                campaign_name=campaign.campaign_name,
                ad_title=campaign.ad_title,
                ad_description=campaign.ad_description,
                terms_and_conditions=campaign.terms_and_conditions,
                payment=campaign.payment,
                start_date=campaign.start_date,
                end_date=campaign.end_date,
                negotiated_price=campaign.payment,
                status='Pending',
                user_id=user.username,
                sponsor_id=sponsorname,
                last_negotiated_by=sponsorname
            )
            db.session.add(campaign_request)
        db.session.commit()

        response_data = existing_request.serialize() if existing_request else campaign_request.serialize()
        return {
            'message': 'Request processed successfully!',
            'campaign_request': response_data
        }, 201

    def serialize_user(self, user):
        return {
            'id': user.id,
            'username': user.username,
            'userhandle': user.userhandle or user.username,
            'email': user.email,
            'bio': user.bio,
            'phone': user.phone,
            'socialMedia': {
                'instagram': self.ensure_http_prefix(user.instagram),
                'youtube': self.ensure_http_prefix(user.youtube),
                'twitter': self.ensure_http_prefix(user.twitter)
            },
            'profilePicUrl': self.decode_base64(user.profilePicUrl),
            'niche': user.niche,
            'reach': user.reach,
            'is_banned': user.is_banned
        }

    def serialize_sponsor(self, sponsor):
        return {
            'sponsor_id': sponsor.sponsor_id,
            'companyName': sponsor.companyName,
            'email': sponsor.email,
            'industry': sponsor.industry,
            'companyWebsite': self.ensure_http_prefix(sponsor.companyWebsite),
            'contactNumber': sponsor.contactNumber,
            'profilePicUrl': self.decode_base64(sponsor.profilePicUrl),
            'is_banned': sponsor.is_banned
        }
    
    def serialize_campaign(self, campaign):
        return {
            'campaign_id': campaign.campaign_id,
            'campaign_name': campaign.campaign_name,
            'ad_title': campaign.ad_title,
            'ad_description': campaign.ad_description,
            'terms_and_conditions': campaign.terms_and_conditions,
            'payment': campaign.payment,
            'sponsor_id': campaign.sponsor_id,
            'is_active': campaign.is_active,
            'is_private': campaign.is_private,
            'flagged': campaign.flagged,
            'negotiated_price': campaign.negotiated_price,
            'start_date': campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else None,
            'end_date': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
        }

    def decode_base64(self, base64_string):
        if not base64_string:
            return None
        try:
            if base64_string.startswith("data:image"):
                return base64_string
            return f"data:image/png;base64,{base64_string}"
        except Exception as e:
            print(f"Error decoding base64: {e}")
            return None

    def ensure_http_prefix(self, url):
        if url and not url.startswith(('http://', 'https://')):
            return f"http://{url}"
        return url
    
from flask_restful import Resource, reqparse

class SponsorCampaignResource(Resource):
    def get(self, sponsorname):
        if not sponsorname:
            return {'error': 'Sponsor name is required'}, 400
        
        try:
            campaigns = Campaign.query.filter_by(sponsor_id=sponsorname).all()
            if not campaigns:
                return {'message': 'No campaigns found for this sponsor'}, 404
            
            flagged_campaigns = request.args.get('flagged', default=None, type=str)
            if flagged_campaigns:
                campaigns = [campaign for campaign in campaigns if campaign.flagged]
                
            serialized_campaigns = [
                {
                    'campaign_id': campaign.campaign_id,
                    'campaign_name': campaign.campaign_name,
                    'progress': campaign.progress,
                    'start_date': campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else None,
                    'end_date': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
                    'ad_title': campaign.ad_title,
                    'ad_description': campaign.ad_description,
                    'terms_and_conditions': campaign.terms_and_conditions,
                    'payment': campaign.payment,
                    'user_id': campaign.user_id,
                    'sponsor_id': campaign.sponsor_id,
                    'flagged': campaign.flagged,
                    'is_private': campaign.is_private,
                    'is_active': campaign.is_active
                }
                for campaign in campaigns
            ]
            
            return jsonify(serialized_campaigns)
        
        except Exception as e:
            print(f"Error retrieving campaigns: {e}")
            return {'error': 'An error occurred while retrieving campaigns'}, 500

    # def get(self, sponsorname):
    #     if not sponsorname:
    #         return {'error': 'Sponsor name is required'}, 400
        
    #     # Check for query parameter
    #     flagged = request.args.get('flagged', default=None, type=str)
        
    #     try:
    #         query = Campaign.query.filter_by(sponsor_id=sponsorname)
    #         if flagged == 'true':
    #             query = query.filter_by(flagged=True)
    #         elif flagged == 'false':
    #             query = query.filter_by(flagged=False)
            
    #         campaigns = query.all()
    #         if not campaigns:
    #             return {'message': 'No campaigns found for this sponsor'}, 404
            
    #         serialized_campaigns = [
    #             {
    #                 'campaign_id': campaign.campaign_id,
    #                 'campaign_name': campaign.campaign_name,
    #                 'progress': campaign.progress,
    #                 'start_date': campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else None,
    #                 'end_date': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
    #                 'ad_title': campaign.ad_title,
    #                 'ad_description': campaign.ad_description,
    #                 'terms_and_conditions': campaign.terms_and_conditions,
    #                 'payment': campaign.payment,
    #                 'user_id': campaign.user_id,
    #                 'sponsor_id': campaign.sponsor_id,
    #                 'flagged': campaign.flagged,
    #                 'is_private': campaign.is_private,
    #                 'is_active': campaign.is_active
    #             }
    #             for campaign in campaigns
    #         ]
            
    #         return jsonify(serialized_campaigns)
        
    #     except Exception as e:
    #         print(f"Error retrieving campaigns: {e}")
    #         return {'error': 'An error occurred while retrieving campaigns'}, 500

    def post(self, sponsorname):
        if not sponsorname or sponsorname == "undefined":
            return {'error': 'Sponsor name is required and cannot be "undefined"'}, 400
        
        data = request.get_json()
        print(f"Received data: {data}")
        required_fields = ['campaign_name', 'ad_niche', 'ad_description', 'terms_and_conditions', 'payment']
        if not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}, 400
        
        user_id = data.get('user_id')  # Can be None if not provided
        start_date = data.get('start_date')  # Can be None if not provided
        end_date = data.get('end_date')  # Can be None if not provided
        
        # Convert date strings to date objects if they are not None
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        try:
            new_campaign = Campaign(
                campaign_name=data['campaign_name'],
                ad_title=data['ad_niche'],
                ad_description=data['ad_description'],
                terms_and_conditions=data['terms_and_conditions'],
                payment=data['payment'],
                sponsor_id=sponsorname,  # Use the sponsorname
                user_id=user_id,
                start_date=start_date,
                end_date=end_date
            )
            db.session.add(new_campaign)
            db.session.commit()
            
            return {'message': 'Campaign created successfully', 'campaign_id': new_campaign.campaign_id}, 201
        
        except Exception as e:
            print(f"Error creating campaign: {e}")
            return {'error': 'An error occurred while creating the campaign'}, 500

       
        
    def put(self, sponsorname):
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        
        if not sponsorname or not campaign_id:
            return {'error': 'Sponsor name and campaign ID are required'}, 400
        
        try:
            campaign = Campaign.query.filter_by(campaign_id=campaign_id, sponsor_id=sponsorname).first()
            if not campaign:
                return {'error': 'Campaign not found'}, 404
            
            campaign.campaign_name = data.get('campaign_name', campaign.campaign_name)
            campaign.ad_title = data.get('ad_niche', campaign.ad_title)
            campaign.ad_description = data.get('ad_description', campaign.ad_description)
            campaign.terms_and_conditions = data.get('terms_and_conditions', campaign.terms_and_conditions)
            campaign.payment = data.get('payment', campaign.payment)
            campaign.user_id = data.get('user_id', campaign.user_id)
            campaign.is_active = data.get('is_active', campaign.is_active)
            campaign.is_private = data.get('is_private', campaign.is_private)
            
            db.session.commit()
            return {'message': 'Campaign updated successfully'}, 200
        
        except Exception as e:
            print(f"Error updating campaign: {e}")
            return {'error': 'An error occurred while updating the campaign'}, 500

    def delete(self, sponsorname):
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        
        if not sponsorname or not campaign_id:
            return {'error': 'Sponsor name and campaign ID are required'}, 400
        
        try:
            campaign = Campaign.query.filter_by(campaign_id=campaign_id, sponsor_id=sponsorname).first()
            if not campaign:
                return {'error': 'Campaign not found'}, 404
            
            db.session.delete(campaign)
            db.session.commit()
            return {'message': 'Campaign deleted successfully'}, 200
        
        except Exception as e:
            print(f"Error deleting campaign: {e}")
            return {'error': 'An error occurred while deleting the campaign'}, 500

class SponsorStatsResource(Resource):
    # @cache.cached(timeout=60)
    def get(self, sponsorname):
        cache_key = f'sponsor_stats_{sponsorname}'
        print(f"Cache key: {cache_key}")

        cached_result = cache.get(cache_key)
        if cached_result:
            print(f"Returning cached result: {cached_result}")
            return cached_result
        
        result = self.get_stats(sponsorname)
        cache.set(cache_key, result)
        print(f"setting cache with key: {cache_key} and result: {result}")
        return result
        return self.get_stats(sponsorname)

    def get_stats(self, sponsorname):
        sponsor = Sponsor.query.filter_by(sponsor_name=sponsorname).first()
        if not sponsor:
            return {'message': 'Sponsor not found'}, 404

        active_requests = CampaignRequest.query.filter_by(sponsor_id=sponsor.sponsor_name, status='Active').all()
        expected_budget = sum(request.negotiated_price for request in active_requests)
        allotted_requests = CampaignRequest.query.filter_by(sponsor_id=sponsor.sponsor_name).all()
        allotted_campaigns = Campaign.query.filter_by(sponsor_id=sponsor.sponsor_name).all()
        total_negotiated_price = sum(float(request.negotiated_price) for request in allotted_requests if request.negotiated_price is not None)
        total_payment = sum(float(campaign.payment) for campaign in allotted_campaigns if campaign.payment is not None)
        allotted_budget = total_negotiated_price + total_payment

        total_campaigns = Campaign.query.filter_by(sponsor_id=sponsor.sponsor_name).all()
        total_campaigns_count = len(total_campaigns)

        active_campaigns = Campaign.query.filter_by(sponsor_id=sponsor.sponsor_name, is_active=True).all()
        total_active_campaigns_count = len(active_campaigns)

        campaigns_allotted_to_users_count = len(active_requests)

        return jsonify({
            'expected_budget': expected_budget,
            'total_campaigns': total_campaigns_count,
            'total_active_campaigns': total_active_campaigns_count,
            'campaigns_allotted_to_users': campaigns_allotted_to_users_count,
            'allotted_budget': allotted_budget
        })

    def post(self, sponsorname):
        data = request.get_json()
        action = data.get('action')
        print(f"Action: {action}")
        print(f"Data: {data}")
        print(f"Sponsorname: {sponsorname}")
        if action == 'export':
            sponsor = Sponsor.query.filter_by(sponsor_name=sponsorname).first()
            if not sponsor:
                return {'message': 'Sponsor not found'}, 404

            print(f"Exporting CSV for sponsor: {sponsor.sponsor_name}")
            export_campaign_csv(sponsor.sponsor_id, sponsor.sponsor_name)
            return {'message': 'Export initiated successfully. Check your email shortly for the CSV.'}, 202
        else:
            return {'message': 'Invalid action'}, 400
        




# <----------------------------------Admin Resources------------------------------------->
import uuid

class AdminDashboardResource(Resource):
    @cache.cached(timeout=10)
    def get(self, username):
        cached_result = cache.get('admin_dashboard')
        if cached_result:
            print(f"Returning cached result: {cached_result}")
            return cached_result
        try:
            total_users = User.query.count()
            total_users = total_users - 1
            total_sponsors = Sponsor.query.count()
            total_campaigns = Campaign.query.count()

            ongoing_campaigns = [campaign.serialize() for campaign in Campaign.query.all()]
            new_requests = [request.serialize() for request in User.query.filter_by(is_banned=True).all()]
            sponsor_action = [sponsor.serialize() for sponsor in Sponsor.query.filter_by(is_banned=True).all()]

            response_data = {
                'totalUsers': total_users,
                'totalSponsors': total_sponsors,
                'totalCampaigns': total_campaigns,
                'ongoingCampaigns': ongoing_campaigns,
                'newRequests': new_requests,
                'sponsor_action': sponsor_action
            }
            return response_data, 200

        except Exception as e:
            return {'error': str(e)}, 500

    def post(self, username):
        data = request.get_json()
        item_id = data.get('id')
        item_type = data.get('type')
        action = data.get('action')

        if item_type not in ['user', 'sponsor', 'campaign']:
            return {'message': 'Invalid type'}, 400

        if action not in ['ban', 'unban', 'flag', 'unflag']:
            return {'message': 'Invalid action'}, 400

        if item_type == 'user':
            item = User.query.get(item_id)
            if not item:
                return {'message': 'User not found'}, 404
            item.is_banned = action == 'ban'
        elif item_type == 'sponsor':
            item = Sponsor.query.get(item_id)
            if not item:
                return {'message': 'Sponsor not found'}, 404
            item.is_banned = action == 'ban'
        elif item_type == 'campaign':
            item = Campaign.query.get(item_id)
            if not item:
                return {'message': 'Campaign not found'}, 404
            item.flagged = action == 'flag'

        db.session.commit()
        cache.clear()
        return {'message': f'{item_type.capitalize()} has been {action}ned successfully'}, 200

    def delete(self, username):
        data = request.get_json()
        item_id = data.get('id')
        item_type = data.get('type')

        if item_type not in ['user', 'sponsor', 'campaign']:
            return {'message': 'Invalid type'}, 400

        if item_type == 'user':
            item = User.query.get(item_id)
        elif item_type == 'sponsor':
            item = Sponsor.query.get(item_id)
        elif item_type == 'campaign':
            item = Campaign.query.get(item_id)

        if not item:
            return {'message': f'{item_type.capitalize()} not found'}, 404

        db.session.delete(item)
        db.session.commit()

        return {'message': f'{item_type.capitalize()} deleted successfully'}, 200

    def put(self, username):
        data = request.get_json()
        campaign_id = data.get('id')
        flag = data.get('flag')

        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {'message': 'Campaign not found'}, 404

        campaign.flagged = flag
        db.session.commit()
        cache.clear()
        return {'message': 'Campaign updated successfully'}, 200

    def serialize_campaign(self, campaign):
        return {
            'campaign_id': campaign.campaign_id,
            'campaign_name': campaign.campaign_name,
            'ad_title': campaign.ad_title,
            'ad_description': campaign.ad_description,
            'terms_and_conditions': campaign.terms_and_conditions,
            'start_date': campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else None,
            'end_date': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
            'payment': campaign.payment,
            'sponsor_id': campaign.sponsor_id,
            'is_active': campaign.is_active,
            'is_private': campaign.is_private,
            'flagged': campaign.flagged,
            'negotiated_price': campaign.negotiated_price,
        }

class AdminApplicationsResource(Resource):
    def get(self, username):
        try:
            applications = SponsorApplication.query.all()
            applications_data = [
                {
                    "id": app.id,
                    "sponsor_name": app.sponsor_name,
                    "email": app.email,
                    "industry": app.industry,
                    "companyName": app.companyName,
                    "companyWebsite": app.companyWebsite,
                    "contactNumber": app.contactNumber
                } for app in applications
            ]
            return jsonify(applications_data)
        except Exception as e:
            print(f"error error error bro error stupid errors: {e}")
            return jsonify({
                "error": "error occurred while fetching stupid applications.",
                "details": str(e)
            }), 500

    def post(self, username):
        data = request.get_json()
        application_id = data.get('application_id')
        action = data.get('action')
        
        if not application_id or not action:
            return {'message': 'Missing application_id or action'}, 400

        try:
            application = SponsorApplication.query.get(application_id)
            if not application:
                return {'message': 'not found'}, 404

            if action == 'approve':
                new_sponsor = Sponsor(
                    sponsor_id=str(uuid.uuid4()),
                    sponsor_name=application.sponsor_name,
                    email=application.email,
                    password=generate_password_hash(application.password, method='pbkdf2:sha256'),
                    industry=application.industry,
                    companyName=application.companyName,
                    companyWebsite=application.companyWebsite,
                    contactNumber=application.contactNumber
                )
                db.session.add(new_sponsor)
                db.session.commit()
                
                db.session.delete(application)
                db.session.commit()
                return {'message': 'Application approved and added to sponsors'}, 200
            elif action == 'reject':
                db.session.delete(application)
                db.session.commit()
                return {'message': 'Application rejected and removed'}, 200
            else:
                return {'message': 'Invalid action'}, 400
            
        except Exception as e:
            return {'message': str(e)}, 500
  
class AdminFindResource(Resource):
    def get(self, username):
        users = User.query.filter(User.username != 'admin').all()
        sponsors = Sponsor.query.all()  # Retrieve all sponsors

        filtered_users = [self.serialize_user(user) for user in users]
        serialized_sponsors = [self.serialize_sponsor(sponsor) for sponsor in sponsors]

        return jsonify({
            'users': filtered_users,
            'sponsors': serialized_sponsors
        })

    def post(self, username):
        data = request.get_json()
        item_id = data.get('id')
        item_type = data.get('type')
        action = data.get('action')

        if item_type not in ['user', 'sponsor']:
            return {'message': 'Invalid type'}, 400

        if action not in ['ban', 'unban']:
            return {'message': 'Invalid action'}, 400

        if item_type == 'user':
            item = User.query.get(item_id)
            if not item:
                return {'message': 'User not found'}, 404
        elif item_type == 'sponsor':
            item = Sponsor.query.get(item_id)
            if not item:
                return {'message': 'Sponsor not found'}, 404

        if action == 'ban':
            item.is_banned = True
        elif action == 'unban':
            item.is_banned = False

        db.session.commit()

        return {'message': f'{item_type.capitalize()} has been {action}ned successfully'}, 200

    def serialize_user(self, user):
        return {
            'id': user.id,
            'username': user.username,
            'userhandle': user.userhandle or user.username,
            'email': user.email,
            'bio': user.bio,
            'phone': user.phone,
            'socialMedia': {
                'instagram': self.ensure_http_prefix(user.instagram),
                'youtube': self.ensure_http_prefix(user.youtube),
                'twitter': self.ensure_http_prefix(user.twitter)
            },
            'profilePicUrl': self.decode_base64(user.profilePicUrl),
            'niche': user.niche,
            'is_banned': user.is_banned
        }

    def serialize_sponsor(self, sponsor):
        return {
            'sponsor_id': sponsor.sponsor_id,
            'sponsor_name': sponsor.sponsor_name,
            'email': sponsor.email,
            'industry': sponsor.industry,
            'companyName': sponsor.companyName,
            'companyWebsite': self.ensure_http_prefix(sponsor.companyWebsite),
            'contactNumber': sponsor.contactNumber,
            'profilePicUrl': self.decode_base64(sponsor.profilePicUrl),
            'is_banned': sponsor.is_banned
        }
    
    def decode_base64(self, base64_string):
        if not base64_string:
            return None
        try:
            if base64_string.startswith("data:image"):
                return base64_string
            return f"data:image/png;base64,{base64_string}"
        except Exception as e:
            print(f"Error decoding base64: {e}")
            return None

    def ensure_http_prefix(self, url):
        if url and not url.startswith(('http://', 'https://')):
            return f"http://{url}"
        return url

def test_serialization():
    active_requests = CampaignRequest.query.filter_by(sponsor_id='sponsor1', status='Active').all()
    new_requests = CampaignRequest.query.filter_by(sponsor_id='sponsor1', status='Pending').all()
    try:
            test_data = {
                'activeRequests': [req.serialize() for req in active_requests],
                'newRequests': [req.serialize() for req in new_requests],
            }
            import json
            json.dumps(test_data)
            print("Serialization successful")
    except Exception as e:
            print("Serialization failed:", e)

class AdminStatsResource(Resource):
    def get(self, username):
        try:
            total_users = User.query.count() or 0
            total_users = (total_users - 1) if total_users > 0 else 0
            total_sponsors = Sponsor.query.count() or 0
            total_campaigns = Campaign.query.count() or 0
            active_campaigns = Campaign.query.filter_by(is_active=True).count() or 0
            user_niche_distribution = self.get_user_niche_distribution()
            sponsor_industry_distribution = self.get_sponsor_industry_distribution()
            banned_users = User.query.filter_by(is_banned=True).count() or 0
            banned_sponsors = Sponsor.query.filter_by(is_banned=True).count() or 0
            topusername = User.query.order_by(User.reach.desc()).first()
            topusername = f"{topusername.userhandle} ({topusername.reach})" if topusername else None
            topearningusername = User.query.order_by(User.earnings.desc()).first()
            topearningusername = f"{topearningusername.userhandle} (${topearningusername.earnings})" if topearningusername else None
            average_earning = User.query.filter_by(role_id=2).with_entities(func.avg(User.earnings)).scalar()
            average_earning = f"${average_earning:.2f}" if average_earning else None

            return jsonify({
                'total_users': total_users,
                'total_sponsors': total_sponsors,
                'total_campaigns': total_campaigns,
                'active_campaigns': active_campaigns,
                'user_niche_distribution': user_niche_distribution,
                'sponsor_industry_distribution': sponsor_industry_distribution,
                'banned_users': banned_users,
                'banned_sponsors': banned_sponsors,
                'topusername': topusername,
                'topearningusername': topearningusername,
                'average_earning': average_earning
            })
        except Exception as e:
            print(f"Error generating stats: {e}")
            return jsonify({'error': 'Failed to generate stats'}), 500

    def get_user_niche_distribution(self):
        niche_counts = db.session.query(User.niche, func.count(User.id)).group_by(User.niche).all()
        print(niche_counts)
        return {niche if niche is not None else 'Admin Niche :)': count for niche, count in niche_counts}

    def get_sponsor_industry_distribution(self):
        industry_counts = db.session.query(Sponsor.industry, func.count(Sponsor.sponsor_id)).group_by(Sponsor.industry).all()
        return {industry if industry is not None else 'Unknown': count for industry, count in industry_counts}

    def get_export(self, username):
        try:
            total_users = User.query.count() or 0
            total_sponsors = Sponsor.query.count() or 0
            total_campaigns = Campaign.query.count() or 0
            active_campaigns = Campaign.query.filter_by(is_active=True).count() or 0
            user_niche_distribution = self.get_user_niche_distribution()
            sponsor_industry_distribution = self.get_sponsor_industry_distribution()
            banned_users = User.query.filter_by(is_banned=True).count() or 0
            banned_sponsors = Sponsor.query.filter_by(is_banned=True).count() or 0
            topusername = User.query.order_by(User.reach.desc()).first()
            topusername = f"{topusername.userhandle} ({topusername.reach})" if topusername else None
            topearningusername = User.query.order_by(User.earnings.desc()).first()
            topearningusername = f"{topearningusername.userhandle} (${topearningusername.earnings})" if topearningusername else None
            average_earning = User.query.with_entities(func.avg(User.earnings)).scalar()
            average_earning = f"${average_earning:.2f}" if average_earning else None

            df = pd.DataFrame({
                'Metric': ['Total Users', 'Total Sponsors', 'Total Campaigns', 'Active Campaigns', 'Banned Users', 'Banned Sponsors', 'Top Username', 'Top Earning Username', 'Average Earning'],
                'Value': [total_users, total_sponsors, total_campaigns, active_campaigns, banned_users, banned_sponsors, topusername, topearningusername, average_earning]
            })

            csv = df.to_csv(index=False)

            return send_file(io.StringIO(csv), mimetype='text/csv', as_attachment=True, attachment_filename='sponsornetdata.csv')

        except Exception as e:
            print(f"Error generating CSV: {e}")
            return jsonify({'error': 'Failed to generate CSV'}), 500

from flask import request, jsonify
from celery.result import AsyncResult
from flask import request, jsonify, send_file
from .tasks import export_campaign_csv
from flask import request, jsonify

class CampaignResource(Resource):
    def post(self):
        data = request.json
        new_campaign = Campaign(
            name=data['name'],
            description=data['description'],
            budget=data['budget'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            visibility=data['visibility'],
            goals=data['goals'],
            sponsor_id=data['sponsor_id']
        )
        db.session.add(new_campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign created successfully'}), 201

    def put(self, campaign_id):
        data = request.json
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        if 'name' in data:
            campaign.name = data['name']
        if 'description' in data:
            campaign.description = data['description']
        if 'budget' in data:
            campaign.budget = data['budget']
        if 'start_date' in data:
            campaign.start_date = data['start_date']
        if 'end_date' in data:
            campaign.end_date = data['end_date']
        if 'visibility' in data:
            campaign.visibility = data['visibility']
        if 'goals' in data:
            campaign.goals = data['goals']

        db.session.commit()
        return jsonify({'message': 'Campaign updated successfully'}), 200

    def delete(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        db.session.delete(campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign deleted successfully'}), 200

class CampaignRequestResource(Resource):
    def post(self):
        data = request.json
        new_request = CampaignRequest(
            campaign_id=data['campaign_id'],
            influencer_id=data['influencer_id'],
            sponsor_id=data['sponsor_id'],
            messages=data['messages'],
            requirements=data['requirements'],
            payment_amount=data['payment_amount'],
            status='Pending'
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Campaign request submitted successfully'}), 201

    def put(self, request_id):
        data = request.json
        request_obj = CampaignRequest.query.get(request_id)
        if not request_obj:
            return jsonify({'error': 'Request not found'}), 404

        if 'status' in data:
            request_obj.status = data['status']

        db.session.commit()
        return jsonify({'message': 'Request updated successfully'}), 200

    def delete(self, request_id):
        request_obj = CampaignRequest.query.get(request_id)
        if not request_obj:
            return jsonify({'error': 'Request not found'}), 404

        db.session.delete(request_obj)
        db.session.commit()
        return jsonify({'message': 'Request deleted successfully'}), 200

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sqlalchemy import func
from flask import jsonify
from flask_restful import Resource
from sqlalchemy import func
from flask import current_app as app
import pandas as pd
from flask import send_from_directory