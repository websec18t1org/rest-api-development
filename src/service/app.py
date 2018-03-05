#!/usr/bin/python

from flask import Flask
from flask_cors import CORS
import json
import os
import sqlite3
from flask import g, request
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from mydb import *
from datetime import datetime


app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members' , '/users/register', \
    '/users/authenticate', '/users/expire', '/users', '/diary', '/diary/create', \
    '/diary/delete', '/diary/permission']

init_db(app)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def make_json_response(data, status=True, code=200, token=None, username=None, fullname=None, age=None, result=None):
    """Utility function to create the JSON responses."""

    to_serialize = {}
    if status:
        to_serialize['status'] = True
        if data is not None:
            to_serialize['result'] = data
        if token is not None:
            to_serialize['token'] = token
        if username is not None:
            to_serialize['username'] = username
        if fullname is not None:
            to_serialize['fullname'] = fullname
        if age is not None:
            to_serialize['age'] = age
        if result is not None:
            to_serialize['result'] = result
    else:
        to_serialize['status'] = False
        to_serialize['error'] = data
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response

def set_password(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)

@app.route("/", methods = ['GET'])
def index():
    """Returns a list of implemented endpoints."""
    return make_json_response(ENDPOINT_LIST, status=True)


@app.route("/meta/heartbeat", methods = ['GET'])
def meta_heartbeat():
    """Returns true"""
    return make_json_response(None, status=True)


@app.route("/meta/members", methods = ['GET'])
def meta_members():
    """Returns a list of team members"""
    with open("./team_members.txt") as f:
        team_members = f.read().strip().split("\n")
    return make_json_response(team_members, status=True)

#testcommand:  curl -i -X POST -d '{"username": "AzureDiamond",  "password": "hunter2",  "fullname": "Joey Pardella",  "age": 15}' http://localhost:8080/users/register -H "Content-Type":application/json
@app.route("/users/register", methods = ['POST'])
def users_register():
    if request.content_type == 'application/json':
        print request.headers
        print request.data

        #content = [{'abc':'xyz'}]
#         {
#     "username": "AzureDiamond",
#     "fullname": "Joey Pardell",
#     "password": "hunter2",
#     "age": 15
# }
        content = request.get_json()
        print json.dumps(content, indent=4)
        print json.dumps(content['username'])
        print json.dumps(content['fullname'])
        print json.dumps(content['password'])
        print json.dumps(content['age'])

        who = content['username']
        who_full = content['fullname']
        who_pass = set_password(content['password'])
        print who_pass
        who_age = content['age']
        #select sql statement
        cur=get_db().cursor()
        cur.execute("select * from diary_users where username=:who",{"who":who})
        first_match = cur.fetchone()
        print "retrieving a single matching row where username=%s: %s" %(who, first_match)
        if  first_match == None:
            cur.execute('INSERT INTO diary_users(username, password, fullname, age) VALUES(?,?,?,?)',(who, who_pass, who_full, who_age))
            get_db().commit()
            return make_json_response(None, code=201, status=True)
        #else if user already exists, return 200 with status=False
        else:
            error_code = "User already exists!"
            return make_json_response(error_code, status=False, code=200)

    else:
        return make_json_response(None, status=False)

@app.route("/users/authenticate", methods = ['POST'])
def users_authenticate():
    rand_token = None
    userid = None
    if request.content_type == 'application/json':
        content = request.get_json()
        #print json.dumps(content, indent=4)
        print json.dumps(content['username'])
        print json.dumps(content['password'])

        #check if user exists in database, if yes return 201 and status=true
        who = content['username']
        who_pass = set_password(content['password'])
        cur=get_db().cursor()
        cur.execute("select password, id from diary_users where username=? ",(who,))
        first_match = cur.fetchone()
        authenticateSuccessful = False
        if first_match != None:
            userid = first_match[1]
            #Check is there existing token.
            #if token exist return it
            #if token doesn't exist create and save in db
            if check_password(first_match[0],content['password']):
                authenticateSuccessful = True


        if authenticateSuccessful == True:
            cur.execute("select token from user_token where userid=? ",(userid,))
            first_match = cur.fetchone()
            if first_match != None:
                rand_token = first_match[0]

            else:
                rand_token = uuid4()
                cur.execute('INSERT INTO user_token(userid, token) VALUES(?,?)',(userid, str(rand_token)))
                get_db().commit()

        print rand_token
        dict = {}
        dict['token'] = str(rand_token)
        if authenticateSuccessful == True:
            return make_json_response(dict, code=200, status=True)
        else :
            return make_json_response(None,code=200, status=False)

@app.route("/users/expire", methods = ['POST'])
def users_expire():
    if request.content_type == 'application/json':
        try:
            content = request.get_json()
            #print json.dumps(content, indent=4)
            print json.dumps(content['token'])
            cur=get_db().cursor()
            cur.execute("delete from user_token where token=:token ",{"token":content['token']})
            get_db().commit()
            if cur.rowcount == 1:
                return make_json_response(None,code=200, status=True)
            else :
                return make_json_response(None,code=200, status=False)
        except sqlite3.Error as e:
            return make_json_response(None,code=200, status=False)

@app.route("/users", methods = ['POST'])
def users():
    if request.content_type == 'application/json':
        content = request.get_json()
        #print json.dumps(content, indent=4)
        print json.dumps(content['token'])
        cur=get_db().cursor()
        cur.execute("select userid from user_token where token=:token ",{"token":content['token']})
        first_row = cur.fetchone()
        if first_row == None:
            return make_json_response("Invalid authentication token.",code=200, status=False)
        else:
            cur.execute("select username, fullname, age from diary_users where id=:userid ",{"userid":first_row[0]})
            first_row = cur.fetchone()
            if first_row == None:
                return make_json_response("Can't find associated user",code=200, status=False)
            else :
                dict = {}
                dict['username'] = str(first_row[0])
                dict['fullname'] = first_row[1]
                dict['age'] = first_row[2]
                return make_json_response(dict,code=200, status=True)

    return make_json_response("Other errors",code=200, status=False)

@app.route("/diary", methods = ['GET', 'POST'])
def diary():
    # check Content-Type: application/json

    if request.method == 'GET':
        cur=get_db().cursor()
        cur.execute("select diary_entries.id, diary_entries.title, diary_users.fullname, diary_entries.publish_date, diary_entries.public, diary_entries.text from diary_entries inner join diary_users on diary_users.id == diary_entries.userid where public=:public ",{"public":1})

        allrow = cur.fetchall()
        print allrow
        # makes the row into list of dictionaries

        content = []
        for row in allrow:
            info = {}
            info['id'] = row[0]
            info['title'] = row[1]
            info['author'] = row[2]
            info['publish_date'] = row[3]
            info['public'] = row[4]
            info['text'] = row[5]
            print info
            content.append(info)

        return make_json_response(content, code=200, status=True)
    if request.content_type == 'application/json':
        if request.method == 'POST':
            content = request.get_json()
            print json.dumps(content['token'])
            cur=get_db().cursor()
            cur.execute("select userid from user_token where token=:token ",{"token":content['token']})
            onerow = cur.fetchone()
            if onerow == None :
                return make_json_response("Invalid authentication token.", code=200, status=False)
            else :
                userid = onerow[0]
                cur.execute("select fullname from diary_users where id=:userid ",{"userid":onerow[0]})
                onerow = cur.fetchone()
                if onerow == None:
                    return make_json_response('Can not find user associated', code=200, status=False)
                else:
                    author = onerow[0]
                    cur.execute("select id, title, publish_date, public, text from diary_entries where userid=:userid ",{"userid":userid})
                    allrow = cur.fetchall()
                    content = []
                    for row in allrow:
                        info = {}
                        info['id'] = row[0]
                        info['title'] = row[1]
                        info['author'] = author
                        info['publish_date'] = row[2]
                        info['public'] = row[3]
                        info['text'] = row[4]
                        print info
                        content.append(info)

                    return make_json_response(content, code=200, status=True)
            return make_json_response(None, code=200, status=False)

@app.route("/diary/create", methods = ['POST'])
def diary_create():
    # check Content-Type: application/json
    print request.headers
    print request.data
    author = None;
    if request.content_type == 'application/json':
        content = request.get_json()
        cur=get_db().cursor()

        cur.execute("select userid from user_token where token=:token ",{"token":content['token']})
        onerow = cur.fetchone()

        if onerow == None :
            return make_json_response("Invalid authentication token.", code=200, status=False)
        else :
            userid = onerow[0]
            cur.execute("select fullname from diary_users where id=:userid ",{"userid":onerow[0]})
            onerow = cur.fetchone()
            if onerow == None:
                return make_json_response('Can not find user associated', code=200, status=False)
            else:
                author = onerow[0]
                dateStr = datetime.today().isoformat()
                publicvar = 0
                if content['public'] == True:
                    publicvar = 1
                cur.execute("insert into diary_entries(title, publish_date, public, text, userid) values(?,?,?,?,?)",(content['title'], dateStr, publicvar, content['text'], userid))
                get_db().commit()
                onerow = cur.fetchone()
                print(cur.lastrowid)
                dict={}
                dict['id'] = cur.lastrowid
                return make_json_response(dict, code=201, status=True)

        return make_json_response(None, code=200, status=True)

@app.route("/diary/delete", methods = ['POST'])
def diary_delete():
    #check Content-Type: application/json
    print request.headers
    print request.data
    author = None;
    if request.content_type == 'application/json':
        content = request.get_json()
        cur=get_db().cursor()

        cur.execute("select userid from user_token where token=:token ",{"token":content['token']})
        onerow = cur.fetchone()
        userid = onerow[0]
        if onerow == None :
            return make_json_response("Invalid authentication token.", code=200, status=False)
        else :
            cur.execute("select fullname from diary_users where id=:userid ",{"userid":onerow[0]})
            onerow = cur.fetchone()
            if onerow == None:
                return make_json_response('Can not find user associated', code=200, status=False)
            else:
                print content['id']
                cur.execute("select userid from diary_entries where id=:id ",{"id":(content['id'])})
                onerow = cur.fetchone()
                #print onerow[0]+':::'+ userid

                if (onerow[0]) != userid:
                    return make_json_response('Diary entry does not belong to user.', code=200, status=False)
                else:
                    cur.execute("DELETE from diary_entries where id=? and userid=?",(content['id'],userid))
                    get_db().commit()
                    if cur.rowcount == 1:
                        return make_json_response(None, code=200, status=True)

    return make_json_response(None, code=200, status=False)

# UPDATE  diary_entries SET public = 0 WHERE id=?
@app.route("/diary/permission", methods = ['POST'])
def diary_permission():
    # check Content-Type: application/json
    print request.headers
    print request.data
    author = None;
    if request.content_type == 'application/json':
        content = request.get_json()
        cur=get_db().cursor()
        cur.execute("select userid from user_token where token=:token ",{"token":content['token']})
        onerow = cur.fetchone()
        userid = onerow[0]
        #print "userid is " + str(userid)
        if onerow == None :
            return make_json_response("Invalid authentication token.", code=200, status=False)
        else :
            cur.execute("select userid from diary_entries where id=:id ",{"id":(content['id'])})
            onerow = cur.fetchone()
            #print onerow[0]
            if onerow[0] != userid:
                #print "i am at the if part"
                return make_json_response('Diary entry does not belong to user.', code=200, status=False)
            else:
                #print "i am at else now"
                if content['public'] == True:
                    #print "public value is true"
                    cur.execute("UPDATE diary_entries SET public=1 WHERE id=?",([content['id']]))
                    #cur.execute("UPDATE diary_entries SET public=1 WHERE id=? and userid=?",(content['id'],userid))
                else:
                    #print "public value is false"
                    cur.execute("UPDATE diary_entries SET public=0 WHERE id=?",([content['id']]))
                    #cur.execute("UPDATE diary_entries SET public=0 WHERE id=? and userid=?",(content['id'],userid))
                get_db().commit()
                if cur.rowcount == 1:
                    return make_json_response(None, code=200, status=True)

        return make_json_response(None, code=200, status=False)


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    #create the database once only
    if db_exist()==False:
        create_database_and_initialize_tables()

    # Run the application
    app.run(debug=True, port=8080, host="0.0.0.0")
