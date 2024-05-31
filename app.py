from flask import *
from flask_restful import Api

app = Flask( __name__ )

api = Api( app )

from datetime import timedelta
from flask_jwt_extended  import JWTManager

# set up KWT
app.secret_key = "1q2w3e4r5t"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] =  timedelta( days = 1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] =  timedelta( days = 30)
jwt = JWTManager (app)
# endpoints /routes 
from views.views import MemberSignup,MemberSignin,Memberprofile,AddDependant,ViewDependant,Laboratories,LabTests,MakeBooking,MyBookings,Payment
from views.views_dashboard import LabSignUp,LabSignIn,ViewLabProfile,AddLabTest,ViewLabTest
api.add_resource(MemberSignup, '/api/member_signup')
api.add_resource( MemberSignin, '/api/member_signin' )
api.add_resource(Memberprofile,'/api/member_profile')
api.add_resource(AddDependant,'/api/add_dependant')
api.add_resource( ViewDependant,'/api/view_dependant')
api.add_resource(Laboratories,'/api/laboratories')
api.add_resource(LabTests,'/api/lab_tests')
api.add_resource(MakeBooking,'/api/make_booking')
api.add_resource(MyBookings,'/api/my_bookings')
api.add_resource(Payment,'/api/payment')
api.add_resource(LabSignUp,'/api/lab_signup')
api.add_resource(LabSignIn,'/api/lab_signin')
api.add_resource(ViewLabProfile, '/api/lab_profile')
api.add_resource(AddLabTest,'/api/add_lab_test')
api.add_resource(ViewLabTest,'/api/view_labtest')

if __name__== '__main__':
    


    app.run(debug=True)

