FROM alpine:3.23

WORKDIR /mydir

RUN apk add --no-cache bash curl

COPY todo-cronjob.sh .

RUN chmod +x todo-cronjob.sh

CMD ["/mydir/todo-cronjob.sh"]