# used earlier to learn but it's of no use so I made random name of this .py file XD


class Response:
    def __init__(self, message, data=None):
        self.message = message
        self.data = data

    def serialize(self):
        return {
            'message': self.message,
            'data': self.data
        }

class ErrorResponse(Response):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

    def serialize(self):
        return {
            'message': self.message,
            'errors': self.errors
        }

class UserResponse(Response):
    def __init__(self, message, user=None):
        super().__init__(message)
        self.user = user

    def serialize(self):
        return {
            'message': self.message,
            'user': self.user
        }

class SponsorResponse(Response):
    def __init__(self, message, sponsor=None):
        super().__init__(message)
        self.sponsor = sponsor

    def serialize(self):
        return {
            'message': self.message,
            'sponsor': self.sponsor
        }

class CampaignResponse(Response):
    def __init__(self, message, campaign=None):
        super().__init__(message)
        self.campaign = campaign

    def serialize(self):
        return {
            'message': self.message,
            'campaign': self.campaign
        }

class CampaignRequestResponse(Response):
    def __init__(self, message, request=None):
        super().__init__(message)
        self.request = request

    def serialize(self):
        return {
            'message': self.message,
            'request': self.request
        }
