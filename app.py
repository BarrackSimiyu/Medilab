from flask import *
from flask_restful import Api

app = Flask( __name__ )

api = Api( app )
# endpoints /routes 
from views.views import MemberSignup

api.add_resource(MemberSignup, '/api/member_signup')

if __name__== '__main__':
    


    app.run(debug=True)

