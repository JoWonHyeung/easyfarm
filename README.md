## 프로젝트 방향성
'장애인 주차구역 서비스' 프로젝트 당시에 Flask api 서버 구축을 시간 관계상 하지 못하여 이번 프로젝트에서 Flask Framework로 Flask API Server를 구축하고자 한다. 또한, 실제 실무에서 ML Service 제공을 위한 워크플로우를 직접 적용해보고자 한다.

![image](https://user-images.githubusercontent.com/57468223/196486402-fda1b143-4ed2-4b37-8b36-f07d47e769b1.png)



oracle 서버 실행 순서 :  mkvirtualenv capstone(가상환경 실행) -> flask run -h 0.0.0.0


---
### 서버 관련


#### 서버 실행 명령어
python3 app.py

#### ec2 남은 용량 확인 명령어
df -h

#### ec2 Out of memory 관련 해결 방법
https://seungwoolog.tistory.com/m/68

##### swap file
http://www.terms.co.kr/swapfile.htm

cf) ec2 프리티어 가용 메모리 용량 1GB

#### 백그라운드 실행

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

#linux cpu 개수 확인
grep -c processor /proc/cpuinfo

```

#### Stateful vs Stateless

stateful : server side에 client와 server의 동작, 상태정보를 저장하는 형태, 세션 상태에 기반하여 server의 응답이 달라짐, 예를 들어 TCP가 있다.

stateless : server side에 client와 server의 동작, 상태정보를 저장하지 않는 형태, server의 응답이 client와의 세션 상태와 독립적이다. 예를 들어, UDP/HTTP가 있다.
![화면 캡처 2022-10-10 123959](https://user-images.githubusercontent.com/57468223/194796265-d2adb4ef-ef8c-4355-86a4-bf82457c1462.png)

#### AWS - S3 연동

https://ritza.co/articles/dvc-s3-set-up-s3-as-dvc-remote/

#### WSGI

파이썬에서 어플리케이션, 즉 파이썬 스크립트(웹 어플리케이션)가 웹 서버와 통신하기 위한 인터페이스입니다. 프로토콜 개념으로 이해할 수도 있습니다. WSGI는 서버와 앱 양단으로 나뉘어져 있습니다. WSGI 리퀘스트를 처리하려면 서버에서 환경정보와 콜백함수를 앱에 제공해야 합니다. 앱은 그 요청을 처리하고 콜백함수를 통해 서버에 응답합니다.

---
### AI 관련

#### class_indics
https://tykimos.github.io/2017/03/08/CNN_Getting_Started/

---
