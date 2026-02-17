# Week 06 - Airflow 워크플로우 오케스트레이션

## 학습 개념
- 워크플로우 오케스트레이션의 필요성
- Airflow 기본 (DAG, Task, Operator, Schedule)
- Task 의존성, Backfill, 멱등성

## 실습 과제
1. Docker Compose로 Airflow 환경 구축
2. 일간 배치 DAG: generate -> validate -> transform -> load -> notify
3. 실패 유도 후 재실행으로 멱등성 확인

## 실행 방법
```bash
docker-compose up -d
# Airflow UI: http://localhost:8080
```

## 디렉토리 구조
```
week06-orchestration-airflow/
├── docker-compose.yml
├── dags/
│   └── daily_flowlog_pipeline.py
├── scripts/
│   ├── generate.py
│   ├── validate.py
│   ├── transform.py
│   └── load.py
└── README.md
```
