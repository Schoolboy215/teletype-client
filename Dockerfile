FROM resin/rpi-raspbian:latest

# Install dependencies
RUN apt-get update
RUN apt-get -qy install python

#RUN pip install pyserial

ADD test.py /
ADD const.py /
ADD thermalPrinter.py /
ADD wordWrap.py /

CMD ["python", "./test.py"]
