from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='thisissecretkey'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Vendor.query.get(int(user_id))


#db.ForeignKey('request.id')
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/petdb'
db=SQLAlchemy(app)

class Breed(db.Model):
    __tablename__ = 'breed'
    bid=db.Column(db.Integer,primary_key=True)
    breed_name=db.Column(db.String(100))

class Pet(db.Model):
    __tablename__ = 'pet'
    pid=db.Column(db.Integer,primary_key=True)
    pet_name=db.Column(db.String(100))
    bid=db.Column(db.Integer, db.ForeignKey('breed.bid'))
    gender=db.Column(db.String())
    age=db.Column(db.Integer())
    height=db.Column(db.Integer())
    weight=db.Column(db.Integer())
    description=db.Column(db.String())


class Records(db.Model):
    __tablename__ = 'records'
    rid=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.String(100),db.ForeignKey('pet.pid'))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class Vendor(UserMixin,db.Model):
    __tablename__ = 'vendor'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Vaccination(db.Model):
    __tablename__ = 'vaccination'
    vid = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer,db.ForeignKey('pet.pid'))
    vaccine_date=db.Column(db.String(100))

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/petdetails')
def petdetails():
    query=db.engine.execute(f"SELECT * FROM `pet`,`breed` WHERE pet.bid = breed.bid") 
    return render_template('petdetails.html',query=query)

@app.route('/records')
def triggers():
    query=db.engine.execute(f"SELECT * FROM `records`") 
    return render_template('records.html',query=query)

@app.route('/breed',methods=['POST','GET'])
def breed():
    if request.method=="POST":
        bname=request.form.get('breed_name')
        query=Breed.query.filter_by(breed_name=bname).first()
        if query:
            flash("Dog Breed Already Exist","warning")
            return redirect('/breed')
        breed_=Breed(breed_name=bname)
        db.session.add(breed_)
        db.session.commit()
        flash("Dog breed Added Successfully","success")
    return render_template('breed.html')

@app.route('/addvaccine',methods=['POST','GET'])
def addvaccine():
    query=db.engine.execute(f"SELECT * FROM `pet`") 
    if request.method=="POST":
        petid=request.form.get('pid')
        vaccinedate=request.form.get('vaccine_date')
        petquery=Vaccination.query.filter_by(pid=petid).first()
        if petquery:
            flash("Dog has been vaccinated and new date updated ","info")
            query1=db.engine.execute(f"UPDATE `vaccination` SET `vaccine_date`='{vaccinedate}' WHERE `pid` = {petid}")
            db.session.commit()
        else:
            vaccinate=Vaccination(pid=petid,vaccine_date=vaccinedate)
            db.session.add(vaccinate)
            db.session.commit()
            flash("Last Vaccine Date Added","warning")

        
    return render_template('vaccine.html',query=query)

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        petid=request.form.get('pid')
        bio=Pet.query.filter_by(pid=petid).first()
        vaccine=Vaccination.query.filter_by(pid=petid).first()
        return render_template('search.html',bio=bio,vaccine=vaccine)
        
    return render_template('search.html')

@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    db.engine.execute(f"DELETE FROM `pet` WHERE `pet`.`pid`={id}")
    flash("Pet details deleted Successfully","danger")
    return redirect('/petdetails')


@app.route("/edit/<string:id>",methods=['POST','GET'])
@login_required
def edit(id):
    breed=db.engine.execute("SELECT * FROM `breed`")
    posts=Pet.query.filter_by(pid=id).first()
    if request.method=="POST":
        pet_name=request.form.get('pet_name')
        gender=request.form.get('gender')
        age=request.form.get('age')
        weight=request.form.get('weight')
        height=request.form.get('height')
        description=request.form.get('description')
        bid=request.form.get('breed')
        query=db.engine.execute(f"UPDATE `pet` SET `pet_name`='{pet_name}',`bid`={bid},`gender`='{gender}',`age`='{age}',`weight`='{weight}',`height`='{height}',`description`='{description}' where `pid`={id}")
        flash("Pet details Updated Successfully","success")
        return redirect('/petdetails')
    
    return render_template('edit.html',posts=posts,breed=breed)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=Vendor.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `vendor` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=Vendor.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addpet',methods=['POST','GET'])
@login_required
def addpet():
    breed=db.engine.execute("SELECT * FROM `breed`")
    if request.method=="POST":
        pet_name=request.form.get('pet_name')
        bid=request.form.get('breed')
        gender=request.form.get('gender')
        age=request.form.get('age')
        weight=request.form.get('weight')
        height=request.form.get('height')
        description=request.form.get('description')
        query=db.engine.execute(f"INSERT INTO `pet` (`pet_name`,`bid`,`gender`,`age`,`weight`,`height`,`description`) VALUES ('{pet_name}',{bid},'{gender}',{age},{weight},{height},'{description}')")
    

        flash("Pet Details Added","info")


    return render_template('pet.html',breed=breed)



app.run(debug=True)    