# Import the required modules
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors


# JWT packages
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required
# lab signup resource 

class  LabSignUp(Resource):
    def post(self):
        data = request.json
        lab_name = data["lab_name"]
        email = data["email"]
        phone = data["phone"]
        permit_id = data["permit_id"]
        password = data["password"]

        connection = connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        cursor = connection.cursor()
        # sql = "INSERT INTO `laboratories` (lab_name,email,phone,permit_id,password) VALUES (%s, %s, %s, %s,%s)"

        # data = (lab_name,email,phone,permit_id,hash_password(password))

        # try:
        #     cursor.execute(sql,data)
        #     connection.commit()
        #     return jsonify({"message":"Lab Inserted Successfully"})
        # except:
        #     return jsonify({"message":"Lab Insertion failed .Try Again"})


        # Check password validity

        response = password_validity(password)
        if response:
            if check_phone(phone):
                # phone is correct
                sql = "INSERT INTO `laboratories` (lab_name,email,phone,permit_id,password) VALUES (%s, %s, %s, %s,%s)"
                data = (lab_name,email,encrypt_data(phone),permit_id,hash_password(password))

                try:
                   cursor.execute(sql,data)
                   connection.commit()
                   code = gen_random()
                   send_sms(phone, '''Thank You for joining MediLab.
                            Your secret number: {}. Do not share.''' .format(code))
                   return jsonify({"message":"Lab Inserted Successfully"})
                except:
                    return jsonify({"message":"Lab Insertion failed .Try Again"})

            else:
                # Phone is note in correct format
                return jsonify ({"message":"Phone number is not in correct format"})
            


        else:
            return jsonify({"message": response})
        

class LabSignIn(Resource):
    def post(self):
        data = request.json
        email = data["email"]
        password = data["password"]

        connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        
         # check if email exists
        sql = "SELECT * FROM `laboratories` WHERE `email` = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute( sql, email )

        if cursor.rowcount == 0:
            return  jsonify( { "message" : "Email does not exist" } )
        else:
            # check password
            lab = cursor.fetchone()
            hashed_password = lab["password"]
            is_matchpassword = verify_password(password, hashed_password)
            if is_matchpassword == True:
                # create token
                access_token = create_access_token(identity=lab, fresh=True)
                return jsonify( { "access_token": access_token,'Lab': lab} )
            elif is_matchpassword == False:
                return jsonify({"message": "Login Failed"})
            else:
                return jsonify({"message":"Something went wrong"})





























































































