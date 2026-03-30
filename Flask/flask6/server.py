from flask import Flask,redirect,url_for,\
    render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "MJ"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self,name,email):
        self.name = name
        self.email = email

@app.route('/home')
def home():
    return render_template('index.html',var1=1,var2="ram",var="dsf")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        session.permanent = True
        name = request.form.get('Name','am')
        session['user']=name
        flash("You have been successfully logged in..")
        return redirect(url_for('userprofile'))
    else:
        if 'user' in session:
            return redirect(url_for('userprofile'))
        return render_template('login.html')

@app.route('/userprofile',methods=["POST","GET"])
def userprofile():
    email = None
    if 'user' in session:
        user = session['user']
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        elif "email" in session:
            email = session["email"]

        return render_template('user.html',email=email)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f"Successfully logged out, {user}!","info")
    session.pop('user',None)
    session.pop('email',None)
    return redirect(url_for('login'))

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)