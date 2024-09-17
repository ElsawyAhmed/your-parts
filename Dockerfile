FROM python

# Set environment variables to ensure Python outputs everything to the console
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /your-parts
# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev curl

# Install dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc

COPY . .
RUN pip install -r requirements.txt

# Set up environment variables for Django (optional)
ENV DJANGO_SETTINGS_MODULE your_parts_task.settings
ENV PYTHONPATH /your_parts_task
EXPOSE 8000
CMD ["sh", "-c","python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

