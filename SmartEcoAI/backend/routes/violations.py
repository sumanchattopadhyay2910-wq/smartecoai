from flask import Blueprint, render_template

violations_bp = Blueprint("violations", __name__)


@violations_bp.route("/violations")
def violations():
    return render_template("violations.html")
