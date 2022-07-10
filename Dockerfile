FROM ubuntu

RUN apt update && \
    apt-get install -y python3 libjsoncpp-dev libprotobuf-dev
