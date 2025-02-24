FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#CMD alembic upgrade head && python3 src/main.py
CMD ["python3", "src/main.py"]