from pybo import db

# 다대다 관계를 설정할 테이블보다 상위에 생셩해야 한다.
# User 테이블과 Question 테이블의 다대다 관계 설정에 사용할 테이블
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

# User 테이블과 Answer 테이블의 다대다 관계 설정에 사용할 테이블
answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

# 질문 모델
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # user_id, user 필드 추가
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set',))
    # modify_date 필드 추가
    modify_date = db.Column(db.DateTime(), nullable=True)
    # 다대다 관계 설정에 사용할 voter 필드 추가
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))

# 답변 모델
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set',))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # user_id, user 필드 추가
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set', ))
    # modify_date 필드 추가
    modify_date = db.Column(db.DateTime(), nullable=True)
    # 다대다 관계 설정에 사용할 voter 필드 추가
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

# 회원가입 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# 댓글 모델
class Comment(db.Model):
    # 댓글 고유번호
    id = db.Column(db.Integer, primary_key=True)
    # 댓글 작성자(User 모델과 관계를 가진다.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # 댓글 작성자
    user = db.relationship('User', backref=db.backref('comment_set'))
    # 댓글 내용
    content = db.Column(db.Text(), nullable=False)
    # 댓글 작성일시
    create_date = db.Column(db.DateTime(), nullable=False)
    # 댓글 수정일시
    modify_date = db.Column(db.DateTime())
    # 댓글의 질문(Question 모델과 관계를 가진다.)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    # 질문글
    question = db.relationship('Question', backref=db.backref('comment_set'))
    # 댓글의 답변(Answer 모델과 관계를 가진다.)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    # 답변글
    answer = db.relationship('Answer', backref=db.backref('comment_set'))

















