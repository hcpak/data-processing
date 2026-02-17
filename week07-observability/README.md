# Week 07 - Observability 모니터링

## 학습 개념
- Observability 3요소: Metrics, Logs, Traces
- 핵심 메트릭: throughput, latency, consumer lag, error rate
- Prometheus + Grafana 스택

## 실습 과제
1. Docker Compose에 Prometheus + Grafana 추가
2. Go 수집기에 메트릭 계측 (Counter, Histogram, Gauge)
3. Python Consumer에 메트릭 추가
4. Grafana 대시보드 구축

## 실행 방법
```bash
docker-compose up -d
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
```

## 디렉토리 구조
```
week07-observability/
├── docker-compose.yml
├── collector/
│   └── metrics.go
├── consumer/
│   └── metrics_consumer.py
├── grafana/
│   └── dashboards/
│       └── pipeline_dashboard.json
├── prometheus/
│   └── prometheus.yml
└── README.md
```
