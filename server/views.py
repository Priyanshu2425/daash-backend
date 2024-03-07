from flask import Flask, Blueprint

views = Blueprint('views', __name__)

@views.route('/<test>')
def home(test):
    return f"backend {test} working"