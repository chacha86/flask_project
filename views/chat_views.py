from flask import Blueprint, render_template, request
from pybo.forms import ChatMessageForm
from pybo.models import ChatMessage, User
from pybo import db
from datetime import datetime
import requests
import json

bp = Blueprint('chat', __name__, url_prefix='/chat')



@bp.route('/iris-data')
def iris_data() :
    sepal_length = int(request.args.get("sepal_length"))
    sepal_width = int(request.args.get("sepal_width"))
    petal_length = int(request.args.get("petal_length"))
    petal_width = int(request.args.get("petal_width"))

    # AI 서버로 전송 (Json)

    ## dictionary로 데이터 구조화
    iris = {}
    iris["sepal_length"] = sepal_length
    iris["sepal_width"] = sepal_width
    iris["petal_length"] = petal_length
    iris["petal_width"] = petal_width

    ## dictionary를 json 문자열로 변환
    json_str = json.dumps(iris, ensure_ascii=False)

    ## json 문자열을 AI서버에 요청할 때 넣어서 보낸다.
    url = "http://127.0.0.1:8099/iris/predict"
    headers = {'Content-type' : 'application/json'}
    res = requests.post(url=url, data=json_str, headers=headers)

    data = res.json()
    print(data["result"])

    return render_template("chat/iris_result.html", data=data)

@bp.route('/iris-form')
def iris_form():

    return render_template("chat/iris_test.html")

@bp.route('/test')
def test() :
    res = requests.get("http://127.0.0.1:8099/iris/get-data")
    data = res.json()

    return render_template('chat/data_test.html', data=data)


def question(msg) :

    # 데이터 딕셔너리 생성
    question = {
        "msg" : msg
    }

    # 딕셔너리를 json 문자열로 변환
    json_str = json.dumps(question)


    # requests 라이브러리를 이용해서 post 요청
    url = "http://127.0.0.1:8033/bot/question"

    headers = {
        "Content-type" : "application/json"
    }

    res = requests.post(url=url, data=json_str, headers=headers) # 챗봇 서버로 데이터 보내기
    data = res.json() # 챗봇 서버가 보내준 데이터 받아서 처리

    return data["msg"]

@bp.route("list", methods=["POST", "GET"])
def _list() :
    form = ChatMessageForm()
    message_list = ChatMessage.query.order_by(ChatMessage.create_date.asc())

    if request.method == 'POST' :
        content = request.form["content"] # 질문 메시지

        ## 챗봇에게 답변 요구
        answer = question(content)

        u1 = User.query.get(1)
        u2 = User.query.get(2)
        c1 = ChatMessage(create_date=datetime.now() ,content=content, user=u1)
        c2 = ChatMessage(create_date=datetime.now(), content=answer, user=u2)

        ## DB에 저장
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

    return render_template('chat/index.html', form=form, message_list=message_list)
