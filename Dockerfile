FROM python

# Set environment variables to ensure Python outputs everything to the console
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /your-parts
# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev curl
COPY . .
RUN pip install -r requirements.txt

# Set up environment variables for Django (optional)
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

