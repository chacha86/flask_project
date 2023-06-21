from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):

    question = Question.query.get_or_404(question_id)

    content = request.form['content']

    answer = Answer(content=content, create_date=datetime.now())
    question.answer_set.append(answer) # 특정 질문에 달린 답변 리스트에 추가 등록한다.

    db.session.commit() # db에 내용 반영
    return redirect(url_for('question.detail', question_id=question_id))