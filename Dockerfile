FROM centos:7

RUN yum install -y python3 mesa-libGL

COPY requirements.txt .
RUN python3 -mvenv venv && venv/bin/pip install -U pip && venv/bin/pip install -r requirements.txt

COPY convert.py .
