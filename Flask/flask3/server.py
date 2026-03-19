from flask import Flask,redirect, \
    url_for,render_template,request

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('index.html',var1=1,var2="ram",var="dsf")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name = request.form.get('Name','ram')
        return redirect(url_for('userprofile',name=name))
    return render_template('login.html')

@app.route('/<name>')
def userprofile(name):
    return f"My name is {name}"

if __name__=='__main__':
    # app.run(debug=True)
    app.run(debug=False)