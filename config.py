import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
# CSRF 토큰을 사용하기 위해 SECRET_KEY 환경 변수를 추가하자.
SECRET_KEY = "dev"