from flask import Flask , render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',title='WI Spare Part System')

@app.route('/partregis/')
def partregis():
    return render_template('partregis.html',title='Part Registeration')

@app.route('/partused/')
def partused():
    return render_template('partused.html',title='Part Used')

@app.route('/partcheck/')
def partcheck():
    return render_template('partcheck.html',title='Part Check System')

if __name__ == '__main__':
    # website_url = 'part.wi:5000'
    # app.config['SERVER_NAME'] = website_url
    # app.run()
    app.run(host= '0.0.0.0',port=5000, debug=True)