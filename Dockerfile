FROM python:3.11
ENV PYTHONUNBUFFERED=1
RUN mkdir /photolib
WORKDIR /photolib
ADD . /photolib/
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations auction
RUN python manage.py makemigrations users
RUN python manage.py migrate
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
