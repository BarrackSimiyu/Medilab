import pymysql
from flask_restful import Resource
from flask import *
from functions import *
# import JWT packages
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required
# Add a member class

# member_signup and member_signin

class MemberSignup( Resource ):
    def  post( self ):
        # Get data from client
        data = request.json
        surname = data["surname"]
        others = data["others"]
        gender = data["gender"]
        email = data["email"]
        contact_no = data["contact_no"]
        dob = data["dob"]
        status=  data["status"]
        password = data["password"]
        location_id = data["location_id"]
        
        # check if password is valid
        response = password_validity(password)
        if  response == True:
            # connect to db
            connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
            cursor = connection.cursor()
            # insert into database
            sql = "INSERT INTO `members` (`surname`, `others`, `gender`, `email`, `contact_no`, `dob`, `status`, `password`, `location_id`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (surname, others, gender, email, contact_no, dob, status, hash_password(password), location_id)
            try:
                cursor.execute( sql, data )
                connection.commit()
                send_sms( contact_no, "Registration Successful" )
                return { "message": "Post Successful.Member saved" }

            except:
                connection.rollback()
                return jsonify( { "message" : "Post failed.Member not saved. Try again" } )
            
        else:
            return jsonify({"message": response})
        
class MemberSignin(Resource):
    def post(self):
        # get request from client
        data =  request.json
        email = data["email"]
        password = data["password"]

        # connect to db
        connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        
        # check if email exists
        sql = "SELECT * FROM `members` WHERE `email` = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute( sql, email )
        if cursor.rowcount == 0:
            return  jsonify( { "message" : "Email does not exist" } )
        else:
            # check password
            member = cursor.fetchone()
            hashed_password = member["password"]
            is_matchpassword = verify_password(password, hashed_password)
        if is_matchpassword == True:
                # create token
                access_token = create_access_token(identity=member, fresh=True)
                return jsonify( { "access_token": access_token,'member': member} )
        elif is_matchpassword == False:
           return jsonify({"message": "Login Failed"})
        else:
            return jsonify({"message":"Something went wrong"})
        


class Memberprofile(Resource):
    @jwt_required( fresh=True )
    def post(self):
        data = request.json
        member_id=data["member_id"]
    # connect to db
        connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        sql = "SELECT * FROM `members` WHERE `member_id` = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute( sql, member_id )
        count = cursor.rowcount
        if count == 0:
            return jsonify ( { "message" : "Member does not exist" } )
        else:
            member = cursor.fetchone()
            return jsonify ({"message":  member})
        


class AddDependant(Resource):
    @jwt_required( fresh=True )
    def post(self):
        data = request.json
        member_id = data["member_id"]
        surname = data["surname"]
        others = data["others"]
        dob = data["dob"]

        connection =  pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        cursor = connection.cursor()
        # insert into dependants table.
        sql = "INSERT INTO `dependants` (`member_id`, `surname`, `others`, `dob`) VALUES (%s, %s, %s, %s)"
        data = (member_id, surname, others, dob)
        try:
            cursor.execute(sql, data)
            connection.commit()
            return jsonify ( { "message" : "Post Successful.Dependant Saved" } )

        except:
            connection.rollback()
            return jsonify ( { "message" : "Post Failed.Dependant not saved." } )
        

class ViewDependant(Resource):
    @jwt_required( fresh=True )
    def post(self):
         data = request.json
         member_id=data["member_id"]
    # connect to db
         connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
         sql = "SELECT * FROM `dependants` WHERE `member_id` = %s"
         cursor = connection.cursor(pymysql.cursors.DictCursor)
         cursor.execute( sql, member_id )
         count = cursor.rowcount
         if count == 0:
                return jsonify ( { "message" : "Member does not exist" } )
         else:
                member = cursor.fetchall()
                return jsonify ({"message":  member})
         


class Laboratories(Resource):
    def get(self):
        connection =  pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        sql = "SELECT * FROM `laboratories`"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return jsonify({"message":"No laboratories"})
        else:
            labs = cursor.fetchall()
            return jsonify ({"message": labs})
        

class LabTests(Resource):
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        connection =  pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        sql = "SELECT * FROM `lab_tests` WHERE `lab_id` = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, lab_id)
        if cursor.rowcount == 0:
            return jsonify({"message":"No lab test found."})
        else:
            lab = cursor.fetchall()
            return jsonify({"message": lab})

        
        
        



        


        
        
