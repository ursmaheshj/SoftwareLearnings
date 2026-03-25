from flask import Flask,redirect,url_for,\
    render_template,request,session,flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "MJ"
app.permanent_session_lifetime = timedelta(minutes=5)

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

@app.route('/userprofile')
def userprofile():
    if 'user' in session:
        user = session['user']
        return render_template('user.html',user=user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f"Successfully logged out, {user}!","info")
    session.pop('user',None)
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)