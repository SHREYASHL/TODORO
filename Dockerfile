FROM python:3.10-slim
# working directory 
WORKDIR /app

#system dependencies for MySQL client and build
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    libssl-dev \
    build-essential \
    python3-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*


#requirements
COPY requirements.txt .
#dependencies

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#app directory
COPY ./app ./app
# FastAPI port
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
