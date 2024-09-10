FROM python
WORKDIR /your-parts
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["./manage.py", "runserver"]

