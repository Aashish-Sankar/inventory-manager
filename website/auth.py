from turtle import delay
from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import db, User

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = db.session.query(User).filter_by(username=username).first()

            if user and check_password_hash(user.hash, password):
                session["user_id"] = user.id
                flash('Logged In Successfully', 'success')
                return redirect("/")
            else:
                flash('Invalid username or password', 'error')
                return redirect(request.url)
        
        return render_template("login.html")

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect("/login")

@auth.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            fullname = request.form.get("fullname")

            if db.session.query(User).filter_by(username=username).first():
                flash('Username already exists', 'error')
                return redirect(request.url)
            
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, hash=hashed_password, fullname=fullname)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect("/login")
        
        return render_template("register.html")

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect("/register")

@auth.route("/logout")
def logout():
    try:
        session.clear()
        flash('Logged out successfully', 'success')
        return redirect("/login")

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect("/login")

@auth.route("/change", methods=["GET", "POST"])
def change():
    try:
        if request.method == "POST":
            new_pwd = request.form.get("new-pwd")
            new_pwd_again = request.form.get("new-pwd-again")

            if new_pwd != new_pwd_again:
                flash('Passwords do not match', 'error')
                return redirect(request.url)

            hashed_password = generate_password_hash(new_pwd)

            user = User.query.filter_by(id=session["user_id"]).first()

            if not user:
                flash('User not found', 'error')
                return redirect("/")
            
            user.hash = hashed_password
            db.session.commit()

            flash('Password changed successfully', 'success')
            return redirect("/")
        
        return render_template("change.html")

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect("/change")
