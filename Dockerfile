FROM python:3.12

WORKDIR /app

RUN  pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "app/app.py"]