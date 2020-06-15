FROM python:3.7-slim
COPY ./app ./app
RUN pip install --no-cache-dir -r ./app/requirements.txt
ENV PYTHONUNBUFFERED 1
WORKDIR ./app
CMD ["uvicorn", "project.wsgi:application", "--host", "0.0.0.0", "--port", "8002"]