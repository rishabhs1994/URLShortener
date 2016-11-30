from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,redirect, request, url_for
import os
from sqlalchemy.orm import sessionmaker
from models import *
import cgi
import re
from Base_Conversion import *
from helper_email import *
import pyperclip
import urllib
import validators
from raven.contrib.flask import Sentry
import clipboard
import signal 
from validate_email_address import validate_email
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
app = Flask(__name__)

sentry = Sentry(app, dsn='https://eb55c3ac68e6469e802d809658f096ec:349c9252e3a94e1184b63cee8e4646ce@sentry.io/107862')

FLAG = 1 
Session = sessionmaker(bind=engine)
s = Session()
signal.signal(signal.SIGPIPE, signal.SIG_DFL) 
@app.route('/home', methods=['GET', 'POST'])
def home(error1="",error2=""):
    if( request.method == 'GET'):
        if not session.get('logged_in'):
            return render_template('login.html', error1=error1, error2=error2)
        else:
            return "Hello Boss!  <a href='/logout'>Logout</a>"
 
    if( request.method == 'POST'):
        if("submit1" in request.form): 
            POST_USERNAME = str(request.form['username'])
            POST_PASSWORD = str(request.form['password'])
            query = s.query(User).filter(User.username.in_([POST_USERNAME]))
            result = query.first()
            if result and result.verify_password(POST_PASSWORD):
                CURRENT_USER = POST_USERNAME
                CURRENT_USER_ID = result.id
                session['user_id'] = result.id
                session['logged_in'] = True
                session['user-name'] = POST_USERNAME
                return redirect('/login/1/3')
            else:
                return render_template('login.html', error1="INVALID USERNAME AND / OR PASSWORD", error2="", uname=POST_USERNAME)

        if("submit2" in request.form):
            C_U = str(request.form['username1'])
            C_P = str(request.form['password1'])
            C_P2 = str(request.form['password2'])
            C_E = str(request.form['emaill'])
            query = s.query(User).filter(User.username.in_([C_U]))
            result = query.first()
            if(result):
                return render_template('login.html', error1="", error2="USERNAME ALREADY TAKEN!", uname2=C_U)
            elif(re.match("^[a-zA-Z0-9]+$", C_U) is None):
                return render_template('login.html', error1="", error2="USERNAME CAN ONLY CONTAIN a-z, A-Z, 0-9.", uname2=C_U)
            elif(len(C_U)<6 or len(C_U)>12):
                return render_template('login.html', error1="", error2="USERNAME MUST HAVE 6-12 CHARACTER ONLY!", uname2=C_U)
            elif(C_P != C_P2):
                return render_template('login.html', error1="", error2="PASSWORDS DONT MATCH!", uname2=C_U)
            elif(len(C_P)<6 or len(C_P)>12):
                return render_template('login.html', error1="", error2="PASSWORDS MUST HAVE 6-12 CHARACTER ONLY!", uname2=C_U)
            elif(re.match("^[a-zA-Z0-9]+$", C_P) is None):
                return render_template('login.html', error1="", error2="PASSWORD CAN ONLY CONTAIN a-z, A-Z, 0-9.", uname2=C_U)
            elif(not validate_email(C_E)):
                return render_template('login.html', error1="", error2="INVALID EMAIL", uname2=C_U)
            else:
                user = User(username = C_U, email= C_E)
                user.hash_password(C_P)
                s.add(user)
                s.commit()
                return redirect('/login/1/3')
     
@app.route("/login/<int:page>/<int:page_size>",methods=['GET', 'POST'])
def login(page,page_size):
    if(request.method == 'GET'):
        #session['logged_in'] = True
        query = s.query(Weburl).order_by(desc(Weburl.created_date)).filter_by(user_id = session.get('user_id'))
        results = query.offset((page-1)*page_size).limit(page_size)
        query = s.query(Weburl).filter_by(user_id = session.get('user_id'))
        result1 = query.offset((page)*page_size).limit(page_size).count()
        global FLAG
        if(FLAG==0):
            return render_template("table.html",results=results, page=page, result1 = result1, CURRENT_USER = session.get('user-name'), page_size=page_size,error3="INAVALID URL")
            global FLAG
            FLAG=1
        else:
            return render_template("table.html",results=results, page=page, result1 = result1, CURRENT_USER = session.get('user-name'), page_size=page_size)


    if(request.method == 'POST'):
        obj = s.query(Weburl).order_by(Weburl.id.desc()).first()
        to_be = 1
        if(obj):
            to_be = obj.id+1

        current_word = toBase62(to_be)
        current_word = current_word.lower()
        if(validators.url(request.form['url_entered'])):            
            if(current_word in ["anus","ass","arse","clit","cock","cum","dick","cunt","fuck","gay","shit","tit","tits","vag"]):
                weburl = Weburl(original_url=request.form['url_entered'], shortened_url = toBase62(to_be), user_id=0)
                to_be+=1
                s.add(weburl)
                s.commit()
            weburl = Weburl(original_url=request.form['url_entered'], shortened_url = toBase62(to_be), user_id=session.get('user_id'))
            s.add(weburl) 
            s.commit()
            ggg = 'login/1/' + str(page_size)
            FLAG = 1
            return redirect(ggg)
        else:
            ggg = 'login/1/' + str(page_size)
            global FLAG
            FLAG = 0
            return redirect(ggg)


@app.route("/delete/<int:del_id>/<int:page_size>", methods=['GET','Post'])
def delete(del_id, page_size):
    if(request.method == 'POST'):
        query = s.query(Weburl).filter_by(id=del_id).first()
        s.delete(query)
        s.commit()
        sss = '/login/1/' + str(page_size)
        return redirect(sss)

@app.route("/visit/<short_url>")
def visit(short_url):
    req_id = toBase10(short_url)
    query = s.query(Weburl).filter_by(id=req_id).first()
    browser = request.user_agent.browser
    query.no_of_click+=1
    if(browser == "chrome"):
        query.visits_in_chrome+=1
    elif(browser == "safari"):
        query.visits_in_safari +=1
    elif(browser == "firefox"):
        query.visits_in_firefox +=1
    elif(browser == "internet_explorer"):
        query.visits_in_internet_explorer +=1

    platform = request.user_agent.platform
    if(platform == "android"):
        query.visits_in_android +=1

    if(platform == "iphone" or platform=="ios"):
        query.visits_in_ios +=1

    s.commit()
    if(query.original_url.startswith("http")):
        final_req = query.original_url
    else:
        final_req = "http://" + query.original_url
    return redirect(final_req)

@app.route("/temp/<int:page_number>/<content>/<int:page_size>")
def temp(page_number, content, page_size):
    clipboard.copy("52.15.140.132:5000/visit/" + content)
    to_be = '/login/' + str(page_number) +'/' + str(page_size)
    return redirect(to_be)

@app.route("/temp3/<int:page_number>/<content>/<int:page_size>")
def temp3(page_number, content, page_size):
    to_be_sent = "52.15.140.132:5000/visit/" + content
    query = s.query(User).filter(User.id.in_([session.get('user_id')]))
    result = query.first()
    emm = result.email
    func(emm, to_be_sent)
    to_be = '/login/' + str(page_number) +'/' + str(page_size)
    return redirect(to_be)

@app.route("/temp2/<int:page_number>" ,methods=['GET','Post'])
def temp2(page_number):
    page_size = str(request.form['q'])
    to_be = '/login/' + str(1) +'/' + str(page_size)
    return redirect(to_be)

@app.route("/analyse/<req_id>/<int:page_num>/<int:page_size>")
def analyse(req_id, page_num, page_size):
    result = s.query(Weburl).filter_by(id=req_id).first()
    return render_template("analysis.html",result=result, page_num=page_num, page_size=page_size)

@app.route("/logout")
def logout():
    global FLAG
    FLAG = 1
    session['user_id']  = 0
    session['user-name'] = ""
    session['logged_in'] = False
    return redirect('/home')
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)