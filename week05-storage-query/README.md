# Week 05 - Data Storage & Query

## 학습 개념
- OLTP vs OLAP
- Columnar Storage (Parquet)
- DuckDB 로컬 OLAP 엔진
- 데이터 레이크 패턴

## 실습 과제
1. DuckDB로 Parquet 쿼리 분석 (Python)
   - Top talker, 포트 스캔 탐지, 시계열 트렌드
2. Go Query API 서버 구축
   - `GET /api/top-talkers?date=2025-01-01`

## 실행 방법
```bash
# Python 분석
pip install duckdb
python analysis/duckdb_analysis.py

# Go API 서버
cd api-server && go build -o api-server && ./api-server
```

## 디렉토리 구조
```
week05-storage-query/
├── analysis/
│   └── duckdb_analysis.py
├── api-server/
│   ├── main.go
│   ├── handler.go
│   └── query.go
├── data/
└── README.md
```
