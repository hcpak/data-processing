# Week 02 - Go 로그 수집기

## 학습 개념
- 로그 수집기(Collector) 설계 원칙
- Go 동시성 모델 (goroutine, channel)
- 구조화된 로그와 JSON Lines 포맷
- 버퍼링과 배치 쓰기

## 실습 과제
1. Go UDP syslog 수신기 구현 (receiver -> parser -> batchWriter)
2. 설정 옵션: `--batch-size`, `--flush-interval`, `--output-dir`
3. Python DNS 로그 sender 작성

## 실행 방법
```bash
# Go 수집기 빌드 및 실행
cd collector && go build -o collector && ./collector --batch-size=1000 --flush-interval=5s

# Python sender 실행
python sender/send_dns_logs.py
```

## 디렉토리 구조
```
week02-log-collector/
├── collector/
│   ├── main.go
│   ├── receiver.go
│   ├── parser.go
│   └── writer.go
├── sender/
│   └── send_dns_logs.py
├── output/
└── README.md
```
