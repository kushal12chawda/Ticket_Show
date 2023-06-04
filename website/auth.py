from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Admin 
from . import db
from flask_login import login_user, login_required,logout_user,current_user
import bcrypt

auth = Blueprint('auth', __name__)

@auth.route("/")
def login_get_user():
    return render_template("login.html")

@auth.route('/user/login', methods=['GET','POST'])
def login_post_user():
    try:
        if request.method == 'POST':
            user_name = request.form['username']
            password = request.form['password']
            
            print(user_name)
            user = User.query.filter_by(user_name = user_name).first()
            
            if user:
                if bcrypt.checkpw(password.encode('utf-8'),user.password):
                    print('step1')
                    login_user(user,remember=True)
                    flash("Logged in Successfully ✅")
                    return redirect(url_for('views.city_user'))
                else:
                    flash("Incorrect Password ❌")
            else:
                print("step2")
                flash("User does not Exists, SIGN IN !!!") 
    except:
        flash("Something went wrong, please TRY AGAIN.")
        return redirect(url_for('views.login_failed'))
    
    return render_template("login.html")

@auth.route('/admin/login', methods=['GET','POST'])
def login_post_admin():
    try:
        if request.method == 'POST':
            admin_name = request.form['username']
            password = request.form['password']
            
            print(admin_name)
            admin = Admin.query.filter_by(admin_name = admin_name).first()
            
            if admin:
                if bcrypt.checkpw(password.encode('utf-8'),admin.password):
                    print('step1')
                    login_user(admin,remember=True)
                    flash("Logged in Successfully ✅")
                    return redirect(url_for('views.city_admin'))
                else:
                    flash("Incorrect Password ❌")
            else:
                print("step2")
                flash("Admin does not Exists, please SIGN IN !!!") 
    except:
          flash("Something went wrong, please TRY AGAIN.")
          return redirect(url_for('views.login_failed'))

    return render_template("login.html")

@auth.route("/signup")
def signup_get_admin():
    return render_template("signup.html")    


@auth.route('/user/signup', methods=['GET', 'POST'])
def signup_user():
    try:
        if request.method == 'POST':
            user_name = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            if len(user_name) < 3:
                flash('Username cannot be less than 3 characters', category='error')
            elif len(password) < 5:
                flash('Password must be greater than 5 characters', category='error')
            else:
                hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
                new_user = User(user_name = user_name, user_email = email, password = hash)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created Successfully ✅', category='success')
                return redirect(url_for('views.sign_up_success')) 
    except:
        flash('Either USERNAME or EMAIL already exists, please TRY AGAIN.')
        return redirect(url_for('views.signup_failed'))           

    return render_template("signup.html" , user=current_user)

@auth.route('/admin/signup', methods=['GET', 'POST'])
def signup_admin():
    try:
        if request.method == 'POST':
            admin_name = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            if len(admin_name) < 3:
                flash('Username cannot be less than 3 characters', category='error')
            elif len(password) < 5:
                flash('Password must be greater than 5 characters', category='error')
            else:
                hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
                new_admin = Admin(admin_name = admin_name, admin_email = email, password = hash)
                db.session.add(new_admin)
                db.session.commit()
                flash('Account created Successfully ✅', category='success')
                return redirect(url_for('views.sign_up_success'))    
    except:
        flash('Either USERNAME or EMAIL already exists, please TRY AGAIN.')
        return redirect(url_for('views.signup_failed'))    


    return render_template("signup.html") 

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been Logged out from our APPLICATION.', category='success')
    return redirect(url_for('auth.login_get_user'))   
