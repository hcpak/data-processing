# Week 01 - 학습 노트

## Q1. 왜 결과를 Parquet으로 저장하는가?

### 다른 시스템에서 바로 읽을 수 있는 표준 포맷
- Spark, DuckDB, Hive, Athena, BigQuery 등 대부분의 데이터 도구가 Parquet을 네이티브로 지원한다.
- 이번 커리큘럼에서도 Week 4(PySpark), Week 5(DuckDB)에서 이 Parquet 파일을 직접 읽어 사용한다.

### CSV 대비 저장 효율이 압도적
- Parquet은 컬럼 기반(Columnar) 저장 방식으로, 같은 타입의 값이 연속 배치되어 압축률이 높다.
- 예시: FlowLog 15만 건 기준 CSV 10.66MB → 집계 결과 Parquet 8.9KB

### 읽기 성능
- CSV는 전체 파일을 파싱해야 하지만, Parquet은 필요한 컬럼만 골라 읽을 수 있다(컬럼 프루닝).
- `bytes` 컬럼만 필요하면 나머지 컬럼은 디스크에서 아예 읽지 않는다.

### 스키마가 파일에 내장됨
- CSV는 모든 값이 문자열이라 `"123"`이 숫자인지 문자열인지 알 수 없다.
- Parquet은 컬럼 타입(int, string, timestamp 등)이 파일 안에 저장되어 별도 변환 없이 정확한 타입으로 읽힌다.

### 데이터 파이프라인에서의 위치
```
[수집] → CSV/JSON → [변환] → Parquet → [분석/쿼리/시각화]
```
실무에서는 "Raw 데이터는 JSON/CSV로 받고, 가공된 데이터는 Parquet으로 저장"하는 패턴이 공식처럼 쓰인다.

---

## Q2. 왜 데이터 분석을 Python으로 하는가? (Go가 아니라)

### 언어별 역할 분담
| 역할 | 언어 | 이유 |
|------|------|------|
| 데이터 변환/집계/분석 | Python | 데이터 분석 라이브러리 생태계가 압도적 |
| 수집기/스트리밍 파이프라인 | Go | 성능과 동시성 처리에 강점 |

### Python의 데이터 분석 생태계
- **pandas**: DataFrame 기반 변환/집계
- **pyarrow**: Parquet 읽기/쓰기
- **PySpark**: 분산 처리
- **kafka-python**: Kafka Consumer
- **duckdb**: SQL 분석
- **Airflow**: 워크플로우 오케스트레이션 (DAG를 Python으로 작성)

### 생산성 차이 예시
Python 3줄로 끝나는 작업이 Go로는 수십 줄의 직접 구현이 필요하다:
```python
# Python
df = pd.read_csv("flowlog.csv", parse_dates=["timestamp"])
df["hour"] = df["timestamp"].dt.floor("h")
hourly = df.groupby("hour").agg(total_bytes=("bytes", "sum"))
```
Go로 동일 작업 시 CSV 파싱, 타입 변환, 시간 자르기, 맵 기반 집계 로직을 모두 직접 구현해야 한다.

### 실무에서의 분담 사례
```
[Go/Rust/Java]                   [Python]
수집기, 프록시, 게이트웨이        변환, 집계, 분석, ML
높은 처리량, 낮은 레이턴시        빠른 개발, 풍부한 라이브러리
장시간 실행되는 서비스            배치 잡, 스크립트, DAG
```
- Cloudflare: 로그 수집/라우팅은 Go, 분석은 Python
- Uber: 수집 파이프라인은 Go, Spark 잡은 Python(PySpark)
- Datadog: Agent는 Go, 데이터 처리 일부는 Python

### 이번 커리큘럼에서의 분담
| 주차 | 언어 | 역할 |
|------|------|------|
| Week 1 | Python | 배치 분석 (pandas) |
| Week 2 | Go | 로그 수집기 (goroutine, channel) |
| Week 3 | Go + Python | Go가 Kafka로 전송, Python이 소비/집계 |
| Week 4 | Python | PySpark 분산 처리 |
| Week 5 | Python + Go | Python이 DuckDB 분석, Go가 API 서버 |
| Week 6 | Python | Airflow DAG 작성 |
| Week 7 | Go + Python | 양쪽 모두 메트릭 계측 |

### 핵심 정리
Python으로 한 이유는 "이 작업에 가장 적합한 도구이기 때문"이다.
데이터 분석 영역에서는 Python 생태계를 대체할 언어가 현재로서는 없다.
