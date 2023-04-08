FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple && \
    pip cache purge

ADD . /app

CMD ["python", "main.py"]