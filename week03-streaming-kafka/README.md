# Week 03 - Kafka 기반 Streaming Processing

## 학습 개념
- Batch vs Streaming 트레이드오프
- Apache Kafka 기본 (Topic, Partition, Consumer Group, Offset)
- Producer / Consumer 패턴

## 실습 과제
1. Docker Compose로 Kafka 환경 구축
2. Go Producer: FlowLog -> Kafka Topic
3. Python Consumer: 5분 윈도우 집계 (tumbling window)

## 실행 방법
```bash
docker-compose up -d
cd producer && go build -o producer && ./producer
python consumer/aggregate_consumer.py
```

## 디렉토리 구조
```
week03-streaming-kafka/
├── docker-compose.yml
├── producer/
│   └── main.go
├── consumer/
│   └── aggregate_consumer.py
├── scripts/
│   └── topic_setup.sh
└── README.md
```
