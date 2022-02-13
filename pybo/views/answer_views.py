from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from pybo import db
from pybo.models import Question, Answer
from pybo.forms import AnswerForm
from ..views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(question=question, content=content, create_date=datetime.now(), user=g.user)
        db.session.add(answer)
        db.session.commit()
        # return redirect(url_for('question.detail', question_id=question_id))
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id))
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question_id))
    if request.method == 'POST':
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now() # 답변 수정일시 저장
            db.session.commit()
            # return redirect(url_for('question.detail', question_id=answer.question.id))
            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    # 데이터베이스에서 삭제할 답변을 얻어온다.
    answer = Answer.query.get_or_404(answer_id)
    # 답변을 삭제한 후 삭제된 답변이 달려있던 질문글을 화면에 표시해야 하므로 질문글 id를 얻어온다.
    question_id = answer.question_id
    if g.user != answer.user:
        flash('삭제 권한이 없습니다.')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

















