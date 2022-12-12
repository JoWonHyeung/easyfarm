# 이지팜

![image](https://user-images.githubusercontent.com/57468223/206992311-6ea46bb2-61f2-4dd5-bf1f-331911e32221.png)


### 아키텍처(Version 7)
![image](https://user-images.githubusercontent.com/57468223/204259888-e6db6a58-e876-4af1-aa9d-02dbc2d2d67c.png)

### 클라우드 

- GCP 크레딧을 사용하여 서버 구축

![Untitled](https://user-images.githubusercontent.com/57468223/196968817-2ae6e683-8a5f-4c5d-a9e9-cb6b7d1eaf23.png)


### 모델 성능 지표

![image](https://user-images.githubusercontent.com/57468223/205545463-8947b240-6d86-4e8a-94e2-3cd70487abf1.png)
![image](https://user-images.githubusercontent.com/57468223/205545482-80b3a08f-36e3-4be7-a2eb-7b11192a5153.png)


### oracle 서버 실행 순서 

```linux
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5000 -j ACCEPT #서버 재부팅시, reset된다.

sudo netfilter-persistent save

mkvirtualenv capstone(가상환경 실행) 

flask run -h 0.0.0.0
```

### docker container 실행 순서

```linux
docker-compose build web

docker ps # 없으면 -a 붙여서 status확인

docker-compose up -d
```
### Dockerfile build 명령어

```linux
docker build -f ./Dockerfile .
```




---
### 서버 관련

```
#백그라운드 명령어 & log파일 생성 명령어

nohup python3 -u connect.py >> output.log & 

tail -f output_disable.log
tail -f output_carnum.log

#프로그램 확인 명령어
ps -ef | grep connect.py

#프로그램 다운 명령어
kill -9 7930

#jupyter notebook 생성 명령어
nohup jupyter-notebook --ip=0.0.0.0 --no-browser --port=8928 &

#linux cpu 확인
grep -c processor /proc/cpuinfo

```

#### Stateful vs Stateless

stateful : server side에 client와 server의 동작, 상태정보를 저장하는 형태, 세션 상태에 기반하여 server의 응답이 달라짐, 예를 들어 TCP가 있다.

stateless : server side에 client와 server의 동작, 상태정보를 저장하지 않는 형태, server의 응답이 client와의 세션 상태와 독립적이다. 예를 들어, UDP/HTTP가 있다.
![화면 캡처 2022-10-10 123959](https://user-images.githubusercontent.com/57468223/194796265-d2adb4ef-ef8c-4355-86a4-bf82457c1462.png)

#### WSGI

파이썬에서 어플리케이션, 즉 파이썬 스크립트(웹 어플리케이션)가 웹 서버와 통신하기 위한 인터페이스입니다. 프로토콜 개념으로 이해할 수도 있습니다. WSGI는 서버와 앱 양단으로 나뉘어져 있습니다. WSGI 리퀘스트를 처리하려면 서버에서 환경정보와 콜백함수를 앱에 제공해야 합니다. 앱은 그 요청을 처리하고 콜백함수를 통해 서버에 응답합니다.
