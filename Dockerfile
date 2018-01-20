FROM arm32v7/python:2.7-slim
MAINTAINER James McKay version: 0.1

RUN apt-get update && apt-get install -y \
    python-pip

RUN pip install pyserial

ADD test.py /
ADD const.py /
ADD thermalPrinter.py /
ADD wordWrap.py /

CMD ["python", "./test.py"]
