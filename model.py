'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import random
import sql
from flask import *

# Initialise our views, all arguments are defaults for the template
database_args = "e2eMessaging.db"
sql_db = sql.SQLDatabase(database_args)

page = {}                           # Determines the page information

app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""
#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------
def check_session(request):
    session_id = request.cookies.get("session_id")
    if session_id is None:
        return False
    else:
        current_username = sql_db.check_session_id(session_id)
        if current_username == []:
            return False
        else:
            current_username = current_username[0]['username']
            user_details = sql_db.get_user_info(current_username)[0]
            course_details = sql_db.get_course_info()
            return {"user_details":user_details, "course_details":course_details}

# Allow image loading
@app.route('/img/<path:path>')
def serve_pictures(path):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return send_from_directory('static/img/', path)

#-----------------------------------------------------------------------------

# Allow CSS
@app.route('/css/<path:path>')
def serve_css(path):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return send_from_directory('static/css', path)

#-----------------------------------------------------------------------------

# Allow javascript
@app.route('/js/<path:path>')
def serve_js(path):
    '''
        serve_js

        Serves js from static/js/

        :: path :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return send_from_directory('static/js', path)

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    '''
        index
        Returns the view for the index
    '''
    session_info = check_session(request)
    user_details = {}
    course_details = {}
    session = {}
    if session_info == False:
        session["logged_in"] = False
    else:
        session["logged_in"] = True
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
    return render_template('index.html', session=session, page=page, user=user_details, course=course_details)

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------
@app.route('/login', methods=['GET'])
def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        session["logged_in"] = False
        return render_template("login.html", session=session, page=page, user=user_details)
    else:
        return redirect(url_for('index'))

#-----------------------------------------------------------------------------

# Check the login credentials
@app.route('/login', methods=['POST'])
def login_check():
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    username = request.form['username']
    password = request.form['password']
    login = sql_db.check_credentials(username, password)
    user_details = {}
    session["logged_in"] = False
    if login:
        session["logged_in"] = True
        user_details = sql_db.get_user_info(username)[0]
        course_details = sql_db.get_course_info()
        res = make_response(render_template('index.html', session=session, page=page, user=user_details, course=course_details))
        res.set_cookie('session_id', user_details['session_id'])
        return res
    else:
        flash("Login Failed, Invalid Username or Password.")
        return render_template("index.html", session=session, page=page, user=user_details)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------
@app.route('/about', methods=['GET'])
def about():
    '''
        about
        Returns the view for the about page
    '''
    session_info = check_session(request)
    user_details = {}
    course_details = {}
    session = {}
    if session_info == False:
        session["logged_in"] = False
    else:
        session["logged_in"] = True
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
    return render_template("about.html", garble=about_garble(), session=session, page=page, user=user_details, course=course_details)



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return render_template("error.html", error_type=error_type, error_msg=error_msg)

@app.route('/register', methods=['GET'])
def register_form():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        session["logged_in"] = False
        return render_template("register.html", session=session, page=page, user=user_details)
    else:
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info != False:
        return redirect(url_for("index"))
    else:
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username.strip() == "":
            flash("Empty Username, Please Try Again.")
            return render_template("register.html",session=session, page=page, user=user_details)
        if password == "":
            flash("Empty Password, Please Try Again.")
            return render_template("register.html",session=session, page=page, user=user_details)
        if password != confirm_password:
            flash("Password Confirmation Failed, Please Try Again.")
            return render_template("register.html",session=session, page=page, user=user_details)
        state = sql_db.add_user(username, password)
        if state == True:
            session["logged_in"] = True
            user_details = sql_db.get_user_info(username)[0]
            course_details = sql_db.get_course_info()
            res = make_response(render_template('validRegister.html', session=session, page=page, user=user_details, course=course_details))
            res.set_cookie('session_id', user_details['session_id'])
            return res
        else:
            flash("Username Already Existed, Please Try Again")
            return redirect(url_for('register_form'))

@app.route('/logout', methods=['GET'])
def logout():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        username = user_details["username"]
        sql_db.log_out(username)
        flash('You have been logged out')
        return redirect(url_for("index"))

@app.route('/friendsList', methods=['GET'])
def friendsList():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        session["logged_in"] = True
        course_details = session_info["course_details"]
        friends = sql_db.get_user_friends_name(user_details["username"])
        print(friends)
        return render_template('friendsList.html', session=session, page=page, user=user_details, friends = friends, course=course_details)

@app.route('/addFriends', methods=['POST', 'GET'])
def addFriends():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        if request.method == 'GET':
            return render_template("addFriends.html", session=session, page=page, user=user_details, course=course_details)
        else:
            friend_username = request.form["username"]
            sql_db.add_friends(user_details["username"], friend_username)
            return redirect(url_for("friendsList"))

@app.route('/messaging/<friend_username>', methods=['GET'])
def messaging(friend_username):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        message_history = sql_db.get_message_history(user_details["username"], friend_username)
        friend_details = sql_db.get_user_info(friend_username)[0]
        print(user_details["signaturePublicKey"])
        return render_template('messaging.html', session=session, page=page, user=user_details, messages=message_history, friend=friend_details, course=course_details)

@app.route('/sendMessage/<friend_username>', methods=['POST'])
def sendMessage(friend_username):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        message = request.cookies.get(user_details["username"] + '_cipherText')
        iv = request.cookies.get(user_details["username"] + '_iv')
        signature = request.cookies.get(user_details["username"] + '_signature')
        if message is None or iv is None or signature is None:
            print("nononononoonnoon")
            return redirect(url_for("messaging", friend_username=friend_username))
        else:
            print(message)
            print(iv)
            print(signature)
            state = sql_db.send_message(user_details["username"], friend_username, message, iv, signature)
            return redirect(url_for("messaging", friend_username=friend_username))

@app.route('/storePublicKey', methods=['GET'])
def storePublicKey():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        print("Storing Public Key")
        username = user_details["username"]
        public_Key = request.cookies.get(username + '_publicKey')
        public_Key = public_Key.replace("new_line", "\n")

        signature_public_key = request.cookies.get(username + '_signaturePublicKey')
        signature_public_key = signature_public_key.replace("new_line", "\n")

        print(public_Key)
        print(signature_public_key)
        state = sql_db.updateUserPublicKey(username, public_Key, signature_public_key)
        return redirect(url_for("index"))

@app.route('/removeFriendList', methods=['GET'])
def removeFriendList():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        friends = sql_db.get_user_friends_name(user_details["username"])
        return render_template('removeFriends.html', session=session, page=page, user=user_details, friends = friends, course=course_details)

@app.route('/removeFriend', methods=['GET'])
def removeFriend():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        return redirect(url_for("removeFriendList"))

@app.route('/viewFriendProfile/<friend_username>', methods=['GET'])
def viewFriendProfile(friend_username):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        friends = sql_db.get_user_friends_name(user_details["username"])
        return render_template('viewFriendProfile.html', session=session, page=page, user=user_details, friend_username=friend_username, course=course_details)

@app.route('/selectCourse/<course_name>', methods=['GET'])
def selectCourse(course_name):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        return render_template('courseOption.html', session=session, page=page, user=user_details, course=course_details, course_name=course_name)

@app.route('/courseGuide/<course_name>', methods=['GET'])
def courseGuide(course_name):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        for c in course_details:
            if c["course_name"] == course_name:
                course_guide = c["course_guide"]
        return render_template('viewCourseGuide.html', session=session, page=page, user=user_details, course=course_details, course_name=course_name, course_guide=course_guide)

@app.route('/changePersonalProfile', methods=['GET'])
def changePersonalProfile():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        return render_template('changePersonalProfile.html', session=session, page=page, user=user_details, course=course_details)

@app.route('/changePassword', methods=['GET'])
def changePassword():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        return render_template('changePassword.html', session=session, page=page, user=user_details, course=course_details)

@app.route('/deleteUser', methods=['GET'])
def deleteUser():
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        users_list = sql_db.get_user_list(user_details["username"])
        return render_template('deleteUser.html', session=session, page=page, user=user_details, course=course_details, users_list=users_list)

@app.route('/viewPost/<course_name>', methods=['GET'])
def viewPost(course_name):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        post_details = sql_db.get_post(course_name)
        comment_details = sql_db.get_comment()
        return render_template('viewPost.html', session=session, page=page, user=user_details, course=course_details, post = post_details, course_name=course_name, comment=comment_details)

@app.route('/createPost/<course_name>', methods=['GET', 'POST'])
def createPost(course_name):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        if request.method == 'GET':
            return render_template('createPost.html', session=session, page=page, user=user_details, course=course_details, course_name=course_name)
        else:
            content = request.form["content"]
            title = request.form["title"]
            sql_db.create_post(course_name, title, content)
            return redirect(url_for("viewPost", course_name=course_name))

@app.route('/createComment/<post_id>/<course_name>', methods=['POST'])
def createComment(post_id, course_name):
    session_info = check_session(request)
    user_details = {}
    session = {}
    if session_info == False:
        return redirect(url_for("index"))
    else:
        user_details = session_info["user_details"]
        course_details = session_info["course_details"]
        session["logged_in"] = True
        comment = request.form["comment"]
        sql_db.create_comment(post_id, comment)
        return redirect(url_for("viewPost", course_name=course_name))

