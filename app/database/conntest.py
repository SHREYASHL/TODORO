from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/fastapi_db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ Connection successful:", conn)
except Exception as e:
    print("❌ Error:", e)


#delete this later