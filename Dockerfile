FROM debian

WORKDIR /usr/src/app

COPY . .

RUN apt-get -y update && apt-get -y upgrade && apt install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "myscript.sh"]
