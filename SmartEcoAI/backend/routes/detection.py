from flask import Blueprint, render_template

detection_bp = Blueprint("detection", __name__)


@detection_bp.route("/detection")
def detection():
    return render_template("index.html", page_title="Detection")
