from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/howtouse')
def howtouse():
    return render_template('howtouse.html')  
@app.route('/moreaboutyou')
def moreaboutyou():
    return render_template('moreaboutyou.html')  

