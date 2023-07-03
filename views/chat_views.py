from flask import Blueprint, render_template, request
from pybo.forms import ChatMessageForm
from pybo.models import ChatMessage, User
from datetime import datetime
from .. import db

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('list', methods=('POST', 'GET'))
def _list() :
    form = ChatMessageForm()
    if request.method == "POST" and form.validate_on_submit() :
        content = form.content.data

        user = User.query.get(3)

        chat = ChatMessage(content=content, create_date=datetime.now(), user=user)
        db.session.add(chat)
        db.session.commit()

    message_list = ChatMessage.query.all()

    return render_template('chat/index.html', form=form, message_list=message_list)