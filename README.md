# Al_Flask_API_Server

'장애인 주차구역 서비스' 프로젝트 당시에 Flask api 서버 구축을 시간 관계상 하지 못하여 이번 프로젝트에서 Flask 프레임워크로 AI Serving Server를 구축하고자 한다.

### 서버 실행 명령어
python3 app.py

### ec2 남은 용량 확인 명령어
df

### ec2 Out of memory 관련 해결 방법
https://seungwoolog.tistory.com/m/68

##### swap file
http://www.terms.co.kr/swapfile.htm

cf) ec2 프리티어 가용 메모리 용량 1GB

### 백그라운드 실행

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
```

# class_indics
https://tykimos.github.io/2017/03/08/CNN_Getting_Started/
