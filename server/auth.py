from flask import Flask, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .model import User, CurrentUser
from . import db
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user:
            if check_password_hash(user.password, data['password']):

                current_user = CurrentUser.query.filter_by(id=1).first()
                if current_user:        
                    db.session.delete(current_user)
                    db.session.commit()

                new_current_user = CurrentUser(current_user=user.id)
                print(new_current_user)
                db.session.add(new_current_user)
                db.session.commit()
                print("current user trying to maintain")

                return jsonify([{'success': 'Logged In Successfully', 'currentUser': user.id}])
            else:
                return jsonify([{'failure': "Wrong Password."}])
        else:
            return jsonify([{'failure': "Email doesn't exist."}])
        
    return jsonify([{'failure': "Something went wrong."}])


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == "POST":
        current_user = CurrentUser.query.filter_by(id=1).first()
        if current_user:        
            db.session.delete(current_user)
            db.session.commit()
            return jsonify([{'success': 'User Logged out Successfully.'} ])
        else:
            return jsonify([{'failure': 'User not logged in.'} ])

    return jsonify([{'failure': 'POST method'} ])



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json

        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify([{'failure': 'Email Already Exists.'}])
        
        if data['password'] != data['confirmPassword']:
            return jsonify([{'failure':'Passwords do not match.'}])
        
        new_user = User(email=data['email'],username=data['username'], password=generate_password_hash(data['password']))
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=data['email']).first()
        new_current_user = CurrentUser(current_user=user.id)
        print(new_current_user)
        db.session.add(new_current_user)
        db.session.commit()
        print("current user trying to maintain")

        print("successful commit")
        return jsonify([{'success': 'Account Created.'}])
    
    return jsonify([{'failure': 'Something went wrong.'}])