FROM resin/rpi-raspbian:jessie
MAINTAINER James McKay version: 0.1

# Install dependencies
RUN apt-get install -y \
    python \
    python-pip

RUN pip install pyserial

ADD test.py /
ADD const.py /
ADD thermalPrinter.py /
ADD wordWrap.py /

CMD ["python", "./test.py"]
