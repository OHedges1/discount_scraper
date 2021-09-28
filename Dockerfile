FROM alpine

WORKDIR /usr/src/app

COPY . .

RUN apk update && apk add python3 && apk add py3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "myscript.sh"]
