FROM ubuntu:latest
LABEL authors="gabi0"

ENTRYPOINT ["top", "-b"]