FROM python:3.7
COPY . /src
WORKDIR /src
RUN pip install numpy
RUN pip install flask
RUN pip install flask_restful
RUN pip install sklearn
RUN pip install pandas
EXPOSE 5000
CMD ["python3", "src/app.py"]