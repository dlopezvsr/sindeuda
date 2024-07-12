FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy

COPY . /app

RUN chmod +x scripts/start.sh

# Adjusted CMD to the correct path
CMD ["scripts/start.sh"]
