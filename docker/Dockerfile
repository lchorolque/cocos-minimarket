FROM python:3

ARG ENVIRONMENT=${ENVIRONMENT}

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings.${ENVIRONMENT}

RUN mkdir /backend
WORKDIR /backend
COPY ./requirements requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/requirements.txt

COPY . /backend/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]