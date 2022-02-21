FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY givenergy/ ./givenergy/
COPY server.py ./

EXPOSE 5000
ENV USERNAME ""
ENV PASSWORD ""

CMD [ "python", "server.py" ]
