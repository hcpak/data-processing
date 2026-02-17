# Network Log Data Pipeline

네트워크 로그(FlowLog, DNS Log)를 수집, 처리, 분석하는 End-to-End 데이터 파이프라인 프로젝트

> Data Processing / Data Engineering 실습 중심 8주 학습 커리큘럼

## Architecture

```
[Go Collector] --> [Kafka] --> [Python Consumer] --> [DuckDB] --> [Go API Server]
      |                              |
      v                              v
[Prometheus] <-------------------- [Metrics]
      |
      v
[Grafana Dashboard]
```

## Tech Stack

| Category | Technology |
|----------|-----------|
| Collection | Go (custom collector) |
| Messaging | Apache Kafka |
| Batch Processing | Python (pandas), PySpark |
| Stream Processing | Python (kafka-python) |
| Storage & Query | DuckDB, Parquet |
| Orchestration | Apache Airflow |
| Observability | Prometheus, Grafana |

## Project Structure

```
.
├── week01-batch-basics/          # Batch Processing - pandas, Parquet
├── week02-log-collector/         # Go 로그 수집기 - goroutine, channel
├── week03-streaming-kafka/       # Kafka 기반 실시간 파이프라인
├── week04-distributed-spark/     # PySpark 분산 처리
├── week05-storage-query/         # DuckDB + Go API 서버
├── week06-orchestration-airflow/ # Airflow DAG 워크플로우
├── week07-observability/         # Prometheus + Grafana 모니터링
└── week08-integration/           # 전체 통합 및 정리
```

## Weekly Curriculum

| Week | Topic | Language | Key Tech |
|------|-------|----------|----------|
| 1 | Batch Processing | Python | pandas, Parquet |
| 2 | Data Collection | Go | goroutine, channel, UDP |
| 3 | Streaming Processing | Go + Python | Kafka |
| 4 | Distributed Processing | Python | PySpark |
| 5 | Storage & Query | Python + Go | DuckDB, REST API |
| 6 | Workflow Orchestration | Python | Airflow |
| 7 | Observability | Go + Python | Prometheus, Grafana |
| 8 | Integration | All | Docker Compose |

## How to Run

각 주차 디렉토리의 README.md를 참고하세요.

## License

MIT
