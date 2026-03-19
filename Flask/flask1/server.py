from flask import Flask,redirect,url_for


app = Flask(__name__)

@app.route('/home/')
def home():
    return f"Welcome <i><b>flask</b></i>"

@app.route('/<ab>/<ngh>')
def name(ngh,ab):
    return f"My name is {ab} {ngh}!"

@app.route('/anotherHome')
def home2():
    return redirect(url_for('home'))


if __name__=='__main__':
    app.run(debug=True)