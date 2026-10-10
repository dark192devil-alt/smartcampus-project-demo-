from flask import Blueprint, jsonify, redirect, url_for
from flask_login import current_user


main_bp = Blueprint("main", __name__)


@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"})


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for(f"{current_user.role}.dashboard"))
    return redirect(url_for("auth.login"))
