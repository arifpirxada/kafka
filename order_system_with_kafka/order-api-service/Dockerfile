from python:3.14

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src .

CMD ["fastapi", "run", "src/main.py", "--port", "8080"]