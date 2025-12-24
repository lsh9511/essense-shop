# 운영 판단 시스템 (Operations Decision System)
# ESSENCE - 편집샵

> **개발 시기**: Phase 4 (Week 14-16)
> **전제 조건**: MVP, Phase 2, Phase 3 완료 (판매 데이터 축적 필요)

---

## 1. 시스템 개요

### 1.1 목적
편집샵 운영자가 데이터 기반으로 **상품 소싱 방식**(직매입 vs 위탁)을 판단하고, 운영 효율성을 높이기 위한 의사결정 지원 시스템

### 1.2 핵심 기능
1. **상품 입력 자동화**: 브랜드/공급처로부터 상품 정보 자동 수집
2. **직매입 vs 위탁 판단**: 수익성, 회전율, 리스크 분석
3. **운영 리포트 출력**: 의사결정에 필요한 핵심 지표 시각화

---

## 2. 기능 상세

### 2.1 상품 입력 자동화

#### 목표
수작업 상품 등록 시간을 80% 단축

#### 기능
- **CSV/Excel 일괄 업로드**: 브랜드에서 제공하는 상품 정보 파일 업로드
- **이미지 자동 처리**: URL 또는 로컬 파일 일괄 업로드
- **상품 정보 검증**: 필수 필드, 가격 형식, 재고 수량 자동 검증
- **중복 상품 감지**: 상품명, SKU 기반 중복 체크

#### 입력 필드
```csv
브랜드명, 상품명, 카테고리, 원가, 판매가, 사이즈, 색상, 재고수량, 이미지URL, SKU
```

#### API 엔드포인트
```
POST /admin/products/bulk-import
- CSV/Excel 파일 업로드
- 검증 후 상품 일괄 등록
- 성공/실패 리포트 반환
```

---

### 2.2 직매입 vs 위탁 판단 알고리즘

#### 판단 기준 지표

| 지표 | 직매입 유리 | 위탁 유리 |
|------|-----------|---------|
| **예상 판매량** | 높음 (월 10개 이상) | 낮음 (월 5개 이하) |
| **마진율** | 40% 이상 | 30% 이하 |
| **재고 회전율** | 빠름 (30일 이내) | 느림 (60일 이상) |
| **반품률** | 낮음 (5% 이하) | 높음 (10% 이상) |
| **초기 투자금** | 여유 있음 | 부족함 |
| **브랜드 신뢰도** | 검증됨 (판매 실적 있음) | 신규 브랜드 |

#### 점수 계산 알고리즘

```python
def calculate_purchase_score(product_data):
    """
    직매입 점수 계산 (0-100점)
    70점 이상: 직매입 추천
    30-70점: 신중 검토
    30점 미만: 위탁 추천
    """
    score = 0

    # 1. 예상 판매량 (30점)
    if product_data['estimated_monthly_sales'] >= 10:
        score += 30
    elif product_data['estimated_monthly_sales'] >= 5:
        score += 15

    # 2. 마진율 (25점)
    margin_rate = product_data['margin_rate']
    if margin_rate >= 0.45:
        score += 25
    elif margin_rate >= 0.35:
        score += 15
    elif margin_rate >= 0.25:
        score += 5

    # 3. 재고 회전율 (20점)
    if product_data['inventory_turnover_days'] <= 30:
        score += 20
    elif product_data['inventory_turnover_days'] <= 60:
        score += 10

    # 4. 반품률 (15점)
    if product_data['return_rate'] <= 0.05:
        score += 15
    elif product_data['return_rate'] <= 0.10:
        score += 7

    # 5. 브랜드 신뢰도 (10점)
    if product_data['brand_verified']:
        score += 10

    return score
```

#### 판단 결과 예시

```json
{
  "product_name": "미니멀 코튼 셔츠",
  "brand": "NEWBRAND",
  "purchase_score": 75,
  "recommendation": "직매입 추천",
  "reasons": [
    "예상 월 판매량 12개 (높음)",
    "마진율 45% (우수)",
    "재고 회전율 25일 (빠름)"
  ],
  "risks": [
    "신규 브랜드로 검증 필요"
  ],
  "estimated_profit": {
    "monthly": "540,000원",
    "yearly": "6,480,000원"
  }
}
```

---

### 2.3 운영 리포트 출력

#### 2.3.1 상품 수익성 분석 리포트

**주요 지표**:
- 상품별 판매량, 매출, 순이익
- 재고 회전율
- 마진율 (평균, 최고, 최저)
- ROI (Return on Investment)

**출력 형식**:
- PDF 리포트
- Excel 다운로드
- 대시보드 시각화

#### 2.3.2 재고 분석 리포트

**주요 지표**:
- 총 재고 금액
- 장기 재고 (90일 이상 미판매)
- 품절 임박 상품
- 재고 회전율 (Fast/Slow Mover 분류)

#### 2.3.3 브랜드별 성과 리포트

**주요 지표**:
- 브랜드별 매출 순위
- 브랜드별 평균 마진율
- 브랜드별 반품률
- 신규 브랜드 vs 기존 브랜드 성과 비교

---

## 3. 데이터 모델

### 3.1 소싱 판단 기록 (sourcing_decisions)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-----------|------|
| id | SERIAL | PK |
| product_id | INTEGER | 상품 ID (FK) |
| decision_type | VARCHAR(20) | 직매입/위탁 |
| purchase_score | INTEGER | 판단 점수 (0-100) |
| estimated_monthly_sales | INTEGER | 예상 월 판매량 |
| margin_rate | DECIMAL(5,2) | 마진율 |
| inventory_turnover_days | INTEGER | 재고 회전일 |
| return_rate | DECIMAL(5,2) | 예상 반품률 |
| decision_date | TIMESTAMP | 판단 일시 |
| notes | TEXT | 비고 |

### 3.2 운영 리포트 (operation_reports)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-----------|------|
| id | SERIAL | PK |
| report_type | VARCHAR(50) | 리포트 유형 |
| period_start | DATE | 집계 시작일 |
| period_end | DATE | 집계 종료일 |
| data | JSONB | 리포트 데이터 (JSON) |
| created_at | TIMESTAMP | 생성 일시 |
| created_by | INTEGER | 생성자 (FK) |

---

## 4. API 명세

### 4.1 상품 일괄 등록

```
POST /api/v1/admin/products/bulk-import
Content-Type: multipart/form-data

Request:
- file: CSV/Excel 파일

Response (200):
{
  "success": true,
  "total": 100,
  "imported": 95,
  "failed": 5,
  "errors": [
    {
      "row": 12,
      "reason": "중복 SKU"
    }
  ]
}
```

### 4.2 소싱 판단 분석

```
POST /api/v1/admin/sourcing/analyze
Content-Type: application/json

Request:
{
  "product_id": 123,
  "estimated_monthly_sales": 10,
  "cost_price": 50000,
  "selling_price": 89000,
  "brand_verified": true
}

Response (200):
{
  "purchase_score": 75,
  "recommendation": "직매입 추천",
  "reasons": [...],
  "risks": [...],
  "estimated_profit": {...}
}
```

### 4.3 운영 리포트 생성

```
POST /api/v1/admin/reports/generate
Content-Type: application/json

Request:
{
  "report_type": "profitability",  // profitability, inventory, brand
  "period_start": "2024-01-01",
  "period_end": "2024-01-31",
  "format": "pdf"  // pdf, excel, json
}

Response (200):
{
  "report_id": 456,
  "download_url": "https://s3.../report_456.pdf",
  "expires_at": "2024-02-01T00:00:00Z"
}
```

---

## 5. 개발 일정 (Week 14-16)

### Week 14: 데이터 모델 및 상품 입력 자동화

**Day 1-2**: 데이터 모델 설계
- [ ] `sourcing_decisions` 테이블 생성
- [ ] `operation_reports` 테이블 생성
- [ ] Alembic 마이그레이션

**Day 3-5**: 상품 일괄 등록 기능
- [ ] CSV/Excel 파서 구현
- [ ] 상품 검증 로직
- [ ] 일괄 등록 API 엔드포인트
- [ ] 어드민 UI (파일 업로드)

**Day 6-7**: 테스트 및 버그 수정
- [ ] 100개 상품 테스트 데이터 업로드
- [ ] 에러 핸들링 개선

### Week 15: 소싱 판단 알고리즘

**Day 1-3**: 판단 알고리즘 구현
- [ ] 점수 계산 로직
- [ ] 추천 생성 로직
- [ ] 과거 데이터 기반 예측 모델

**Day 4-5**: API 및 UI
- [ ] 소싱 분석 API 엔드포인트
- [ ] 어드민 판단 페이지 UI

**Day 6-7**: 실제 데이터 테스트
- [ ] 기존 상품 데이터로 검증
- [ ] 알고리즘 정확도 평가

### Week 16: 운영 리포트

**Day 1-3**: 리포트 생성 엔진
- [ ] 수익성 분석 리포트
- [ ] 재고 분석 리포트
- [ ] 브랜드 성과 리포트

**Day 4-5**: PDF/Excel 출력
- [ ] PDF 생성 (ReportLab)
- [ ] Excel 생성 (openpyxl)
- [ ] 다운로드 링크 생성

**Day 6-7**: 대시보드 통합
- [ ] 리포트 대시보드 UI
- [ ] 자동 리포트 스케줄링 (주간/월간)

---

## 6. 성공 지표

- **상품 등록 시간**: 수작업 대비 80% 단축
- **판단 정확도**: 직매입 추천 상품의 70% 이상 흑자
- **리포트 활용도**: 주간 리포트 열람률 90% 이상
- **ROI 개선**: 재고 회전율 20% 향상

---

## 7. 향후 확장 계획

- **AI 기반 수요 예측**: 머신러닝으로 판매량 예측 정확도 향상
- **자동 발주 시스템**: 재고 부족 시 자동 발주
- **공급처 통합**: 여러 브랜드 API 연동
- **시뮬레이션 기능**: "만약 이 상품을 직매입하면?" 시뮬레이션