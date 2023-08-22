from asyncio.windows_events import NULL
from flask import Flask, render_template, redirect, request, flash,url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import pymongo
from bson.objectid import ObjectId  
from forms import  RegistrationForm,LoginForm,req,priceToPlane

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

#database
client= pymongo.MongoClient('mongodb://localhost:27017')
db=client['Agency_test3']

#login
login_manager = LoginManager(app)

#bcrypt
bcrypt = Bcrypt(app)

#user_login
class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return str(self.user_id)

    @staticmethod
    def get(user_id):
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_id=user_data['_id'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


##########################
# route home -- index.html

@app.route('/')
def index():
    return render_template("index.html")

# route price -- price.html

@app.route('/price', methods=['GET', 'POST'])
def price():
    form=priceToPlane()
    if form.validate_on_submit():
        return render_template("index.html")
    return render_template("price.html", form=form)

# # route to plane 1
@app.route('/price/<value>', methods=['GET', 'POST'])
def innerPrice(value):
    
    if value == "plane_1":
        return render_template("plane_1.html")
    if value == "plane_2":
        return render_template("plane_2.html")
    if value == "plane_3":
        return render_template("plane_3.html")  
################################################

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/price/<value>/billing', methods=['GET', 'POST'])
@login_required
def bill(value):
    id=current_user.user_id 
    x=db.users.find_one(id)    
    if current_user.is_authenticated and x['role']=='guest':
        if value == "plane_1":
            return render_template("plane_1_bill.html")
        elif value == "plane_2":
            return render_template("plane_2_bill.html")
        elif value == "plane_3":
            return render_template("plane_3_bill.html")
    return redirect (url_for('user_dashboard'))      
@app.route("/plane_1")
def plane_1():
    pass

# route login -- login.html

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_data = db.users.find_one({'email': form.email.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user = User(user_data['_id'])
            login_user(user)
            id=current_user.user_id 
            x=db.users.find_one(id)
            if x['role']=='user':
                return render_template('user_dashboard.html')
            if x['role']=='admin':
                return render_template('admin_dashboard.html')
            if x['role']=='guest':
                return render_template("index.html")
        else:
            flash('Invalid username or password!', 'error')
    return render_template('login.html', form=form)


# route admin dashboard -- admin_dashboard.html

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    id=current_user.user_id
    x=db.users.find_one(id)
    if x['role']=='admin':
        return render_template('admin_dashboard.html')
    return render_template('invalid.html')

# route user dashboard -- user_dashboard.html

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    id=current_user.user_id
    x=db.users.find_one(id)
    if x['role']=='user':
        collection_names = db.list_collection_names()
        return render_template('user_dashboard.html')
    return render_template('invalid.html')

# route register -- register.html

@app.route('/register', methods=['GET', 'POST'])
def register():
    collection=db['users']
    form = RegistrationForm()
    if form.validate_on_submit():
        if db.users.find_one({'email': form.email.data}):
            flash('email already exists!', 'error')
        else:
            password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            data={'firstname': form.firstname.data,'lastname': form.lastname.data,'email': form.email.data,'password': password_hash,"role":"guest","active plan":'0'}
            flash('Registration successful! You can now login.', 'success')
            collection.insert_one(data)
            # db.create_collection(form.email.data) --- create a database for every one
            return redirect('/login')
    return render_template('register.html', form=form)
    
   
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# running appmon
if __name__ == '__main__':
    app.run(debug=True)
