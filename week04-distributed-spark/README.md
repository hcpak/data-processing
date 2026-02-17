# Week 04 - Spark 분산 처리

## 학습 개념
- 분산 처리의 필요성
- Apache Spark 기본 (Driver, Executor, DataFrame)
- Lazy Evaluation, Partitioning 전략

## 실습 과제
1. FlowLog 100만 건 데이터 생성
2. PySpark 분석:
   - 시간대 x protocol 피벗 테이블
   - 이상 탐지 (3-sigma)
   - Partitioned Parquet 저장
3. Spark UI로 실행 계획 분석

## 실행 방법
```bash
pip install pyspark
python generate_large_flowlog.py
python spark_analysis.py
```

## 디렉토리 구조
```
week04-distributed-spark/
├── generate_large_flowlog.py
├── spark_analysis.py
├── output/
│   └── partitioned_parquet/
└── README.md
```
