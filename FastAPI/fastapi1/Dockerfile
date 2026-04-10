FROM python:3.12-slim

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN adduser --disabled-password --gecos '' fastapi_user && chown -R fastapi_user:fastapi_user /fastapi_app
USER fastapi_user

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]