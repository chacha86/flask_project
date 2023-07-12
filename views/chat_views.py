from flask import Blueprint, render_template
import requests
import json

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/test')
def test() :
    res = requests.get("http://127.0.0.1:8099/iris/get-data")
    data = res.json()

    return render_template('chat/data_test.html', data=data)
