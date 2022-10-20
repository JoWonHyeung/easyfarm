FROM python:3.9

WORKDIR /Al_Flask_API_Server

COPY ./Al_Flask_API_Server/requirements.txt /Al_Flask_API_Server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /Al_Flask_API_Server/requirements.txt

COPY ./Al_Flask_API_Server /Al_Flask_API_Server

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
