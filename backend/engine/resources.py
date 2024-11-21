from .auth import AuthResource
def initialize_resources(api):
    from .api import (
    RegisterUserResource,
    LoginSponsorResource,
    SponsorRegisterResource,
    SponsorDashboardResource,
    UserDashboardResource,
    FindCampaignsResource,
    ProfileResource,
    AdminDashboardResource,
    AdminFindResource,
    AdminStatsResource,
    AdminApplicationsResource,
    UserFindResource,
    UserStatsResource,
    SponsorProfileResource,
    SponsorFindResource,
    SponsorCampaignResource,
    SponsorStatsResource
    )

    # logni endpoints stuffs
    api.add_resource(AuthResource, '/api/login')
    api.add_resource(RegisterUserResource, '/api/register')
    api.add_resource(LoginSponsorResource, '/api/sponsorlogin')
    api.add_resource(SponsorRegisterResource, '/api/sponsorconfirm')
    # api.add_resource(SponsorRegisterResource, '/api/banned/:sponsorname')

    # influencer endpoints
    api.add_resource(UserFindResource, '/api/u/<string:username>/find')
    api.add_resource(UserStatsResource, '/api/u/<string:username>/stats')
    api.add_resource(ProfileResource, '/api/u/<string:username>/profile')
    api.add_resource(UserDashboardResource, '/api/u/dashboard/<string:username>')
    api.add_resource(FindCampaignsResource, '/api/u/<string:username>/findcampaigns')

    #sponsor endpoints stuff
    api.add_resource(SponsorDashboardResource, '/api/s/<string:sponsorname>/dashboard')
    api.add_resource(SponsorProfileResource, '/api/s/<string:sponsorname>/profile')
    api.add_resource(SponsorFindResource, '/api/s/<string:sponsorname>/find')
    api.add_resource(SponsorCampaignResource, '/api/s/<string:sponsorname>/campaigns')
    api.add_resource(SponsorStatsResource, '/api/s/<string:sponsorname>/stats')
    # api.add_resource(SponsorStatsResource, '/api/s/<string:sponsorname>/stats')
    # api.add_resource(SponsorStatsResource, '/api/s/<string:sponsorname>/stats/export/<string:task_id>')

    #admin endpoints
    api.add_resource(AdminDashboardResource, '/api/a/dashboard/<string:username>')
    api.add_resource(AdminFindResource, '/api/a/<string:username>/find')
    api.add_resource(AdminStatsResource, '/api/a/<string:username>/stats')
    api.add_resource(AdminApplicationsResource, '/api/a/<string:username>/applications')