
1>Create & activate venv (windows)

python -m venv .venv
.venv\Scripts\activate

2>Install packages

pip install -r requirements.txt

3>Configuration — .env file & app/core/config.py

DATABASE_URL=mysql+pymysql://fastapi_user:YourDbPassword@localhost:3306/fastapi_db

4>Create the MySQL database & user

CREATE DATABASE fastapi_db;
CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY 'YourDbPassword';
GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'localhost';
FLUSH PRIVILEGES;

Update .env credentials accordingly.

5>Initialize Alembic

Initialize Alembic

6>Create migration
From project root>>

alembic revision --autogenerate -m "create users and todos"

7>Apply migration
alembic upgrade head

8>Runn th app
uvicorn app.main:app --reload


