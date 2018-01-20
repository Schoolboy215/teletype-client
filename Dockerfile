FROM arm32v7/python:2.7-slim
MAINTAINER James McKay version: 0.1

ADD test.py /

CMD ["python", "./test.py"]
