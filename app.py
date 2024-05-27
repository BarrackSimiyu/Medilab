from flask import *
from flask_restful import Api

app = Flask( __name__ )

api = Api( app )
# endpoints /routes 
from views.views import MemberSignup,MemberSignin,Memberprofile

api.add_resource(MemberSignup, '/api/member_signup')
api.add_resource( MemberSignin, '/api/member_signin' )
api.add_resource(Memberprofile,'/api/member_profile')

if __name__== '__main__':
    


    app.run(debug=True)

