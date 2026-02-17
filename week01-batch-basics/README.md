# Week 01 - Batch Processing 기초

## 학습 개념
- ETL (Extract, Transform, Load) 파이프라인 기본
- Batch Processing의 개념과 적용 시나리오
- CSV / JSON / Parquet 포맷 비교
- Python pandas 기본 연산

## 실습 과제
1. 가상 VPC FlowLog 데이터 생성 (10만 건 이상)
2. pandas로 배치 분석:
   - 시간대별 트래픽 집계
   - REJECT Top 10 source IP
   - Protocol별 bytes 합계
3. 결과를 Parquet으로 저장

## 실행 방법
```bash
pip install pandas pyarrow
python generate_flowlog.py
python analyze_flowlog.py
```

## 디렉토리 구조
```
week01-batch-basics/
├── generate_flowlog.py    # FlowLog 데이터 생성
├── analyze_flowlog.py     # 배치 분석
├── data/
│   ├── raw/               # 원본 CSV
│   └── processed/         # 변환된 Parquet
└── README.md
```
