FROM python:3.12

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH=/app

COPY ./src ./src

CMD ["python", "-m", "src.main"]
