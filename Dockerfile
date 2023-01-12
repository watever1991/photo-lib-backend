FROM python:3.11
ENV PYTHONUNBUFFERED=1
RUN mkdir /photolib
WORKDIR /photolib
ADD . /photolib/
RUN python.exe -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
