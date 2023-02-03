FROM python:3.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1


COPY requirement.txt .
RUN python -m pip install -r requirement.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]