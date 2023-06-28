# create web server
# import related modules 
# import flask related modules
# create driver class with id, name, mobile_number properties
# create routes for add driver , generate related views, html pages and templates
# create html form view for add driver
# create delete driver by  id or driver id
# create list driver , paginate
# searh  driver by id or name or mobile number
# run server, run flask object
# save the student with sqlite, use sqlalchemy
# seperate db related, models into seperate file 
# organise routes related things to seperate file, load in app.py
# create base.html common for list driver, add driver, search driver, delete driver

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

#RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
# set secret key


app = Flask(__name__)
app.secret_key = 'allah rahman hai'


# generate flask db init ,migration, upgrade commands
# flask db init
# flask db migrate -m "driver table"
# flask db upgrade
# do i need to some setup as flask db init is not working


# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///driving_school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create database object
db = SQLAlchemy(app)

# create hello world route temporarily, later we will remove it 
@app.route('/')
def hello_world():
    return 'Hello, World!'

# create driver class with id, name, mobile_number properties
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Driver %r>' % self.name
    
# create routes for add driver , generate related views, html pages and templates
# create html form view for add driver
@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if request.method == 'POST':
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        # print name, mobile numbe to console
        print("name: " + name +", mobile_number:" + mobile_number)
        driver = Driver(name=name, mobile_number=mobile_number)
        db.session.add(driver)
        db.session.commit()
        flash('Driver added successfully')
        return redirect(url_for('list_driver'))
    return render_template('add_driver.html')


# create delete driver by  id or driver id
@app.route('/delete_driver/<int:id>')
def delete_driver(id):
    driver = Driver.query.get_or_404(id)
    db.session.delete(driver)
    db.session.commit()
    flash('Driver deleted successfully')
    return redirect(url_for('list_driver'))

# create list driver , paginate
@app.route('/list_driver')
def list_driver():
    driver_list = Driver.query.paginate(per_page=5)
    return render_template('list_driver.html', driver_list=driver_list)

# searh  driver by id or name or mobile number
@app.route('/search_driver', methods=['GET', 'POST'])
def search_driver():
    if request.method == 'POST':
        search_value = request.form['search_value']
        search_value = "%{}%".format(search_value)
        driver_list = Driver.query.filter(Driver.name.like(search_value)).paginate(per_page=5)
        # support pagination , page 1, 2, 3, first, last ,next , previous
        # pass page number, page size also the list_driver.html, render template



        return render_template('list_driver.html', driver_list=driver_list)
    return render_template('search_driver.html')


# run flask object
if __name__ == '__main__':
    app.run(debug=True)
