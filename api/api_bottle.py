from bottle import Bottle
from api.utils import error_response

class ApiBottle(Bottle):
    '''
    Extend default implementation to handle every error in a more
    suitable way for a REST API.
    '''
    def default_error_handler(self, res):
        '''
        Handle any/every error with a custom JSON response.
        '''
        return error_response(
            reason=res.body,
            status_code=res.status_code
        )