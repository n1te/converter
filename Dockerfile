FROM python:3.6

RUN mkdir -p /app
WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD ./ /app

EXPOSE 80

CMD python run.py