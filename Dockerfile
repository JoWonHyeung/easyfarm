FROM python:3.9

WORKDIR /Al_Flask_API_Server

COPY requirements.txt /Al_Flask_API_Server/requirements.txt

RUN pip install --upgrade pip
RUN pip3 install --user --upgrade tensorflow
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

COPY / /Al_Flask_API_Server

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
