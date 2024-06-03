# NurseSignin Resource
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors


# JWT packages
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required

class NurseSignin(Resource):

    def post(self):
        data = request.json
        surname = data["surname"]
        password =data ["password"]

        connection = connection = connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM nurses WHERE surname= %s"
        cursor.execute(sql,surname)

        count = cursor.rowcount
        if count == 0:
            return jsonify({"message":"Invalid username input."})
        else:
            nurse = cursor.fetchone()
            hashed_password = nurse["password"]
            is_matchpassword = verify_password(password, hashed_password)
            if is_matchpassword == True:
                # create token
                access_token = create_access_token(identity=nurse, fresh=True)
                return jsonify( { "access_token": access_token,'message':'sign in successful'} )
            elif is_matchpassword == False:
                return jsonify({"message": "Login Failed"})
            else:
                return jsonify({"message":"Something went wrong"})
            

# Change password resource
# request method -PUT
class ChangePassword(Resource):
    @jwt_required(fresh=True)
    def put(self):
        data = request.json
        nurse_id=data["nurse_id"]
        old_password = data["old_password"]
        new_password = data["new_password"]
        confirm_password = data["confirm_password"]

        sql = "SELECT * FROM nurses WHERE nurse_id = %s"


        connection = connection = connection = pymysql.connect( host = "localhost", user = "root",password="",database="Medilab")
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,nurse_id)
        if cursor.rowcount == 0:
            return jsonify({"message":"nurse does not exist"})
        else:
            nurse = cursor.fetchone()
            hashed_password=nurse["password"]
            is_matchpassword = verify_password(old_password, hashed_password)
            if is_matchpassword:
                if new_password == confirm_password:
                    # Password match
                    sql = "update nurses set password = %s where nurse_id = %s"
                    cursor1=connection.cursor()
                    data = (hash_password(new_password),nurse_id)
                    try:
                        cursor1.execute(sql,data)
                        connection.commit()
                        return jsonify({"message":"Password changed successfully"})
                    except:
                        connection.rollback()
                        return jsonify({"message":"Password not changed"})

                else:
                    # password dont match
                    return jsonify ({"message":"New password and confirm password does not match"})


            else:
                return jsonify({"message": "old password is incorrect"})




        



            
