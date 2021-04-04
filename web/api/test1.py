import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash



bp = Blueprint("test1",__name__,url_prefix="/test1")

@bp.route("/hello2",methods=("GET"))
def hello2():
	return "hello2"