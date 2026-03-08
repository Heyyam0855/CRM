FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ /app/requirements/
RUN pip install --upgrade pip \
    && pip install -r requirements/base.txt \
    && pip install -r requirements/production.txt

COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

RUN useradd --create-home --shell /bin/bash lmsuser \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R lmsuser:lmsuser /app

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
