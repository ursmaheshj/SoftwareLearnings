from flask import Flask,redirect,url_for,render_template


app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('index.html',var1=1,var2="ram",var="dsf")




if __name__=='__main__':
    app.run(debug=True)