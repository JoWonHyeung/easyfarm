FROM ubuntu:latest

#Labeling
LABEL maintainer = "JWH <mesh153@naver.com>"
LABEL title = "S3 connect"
LABEL description = "S3 file download test"

#python,pip install
RUN apt update -y
RUN apt install -y python3
RUN apt-get -y install python3-pip

#Library install
WORKDIR /Al_Flask_API_Server
COPY requirements.txt /Al_Flask_API_Server/requirements.txt

#Library install
RUN pip3 install --user --upgrade tensorflow
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#AWS CLI install
RUN pip install awscli

#S3 bucket key,value input
RUN sh -c '/bin/echo -e "AKIASVHMEE4QKE2UCJ4Z\nT13Tx4eOxZV80LeLcsIsJjmqEwh5xPWnyBF7Be7x\n\n" | aws configure'

#COPY
COPY / /Al_Flask_API_Server

#CNN model download from s3
RUN aws s3 cp s3://capstonedataimage/xception_epoch10_fine_tuning.h5 /Al_Flask_API_Server/model

#Server execute
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
