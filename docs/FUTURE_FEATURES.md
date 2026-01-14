# 향후 추가 기능 (Future Features)

향후 추가 예정인 기능들을 정리한 문서입니다.

---

## 1. 3DLook AI 바디 스캔 (Phase 2-3)

### 개요
AI 기반 신체 치수 측정 및 사이즈 추천 시스템

### 주요 기능
1. **바디 스캔**
   - 정면 + 측면 사진 2장으로 3D 스캔
   - AI가 자동으로 20개 이상의 신체 치수 측정

2. **사이즈 추천**
   - 상품별 최적 사이즈 추천
   - 브랜드별 핏 차이 반영

3. **반품률 감소**
   - 사이즈 불만족으로 인한 반품 최소화
   - 고객 만족도 향상

### 기술 스택
- **3DLook API** (https://3dlook.ai/)
- 프론트: 카메라 촬영 또는 사진 업로드
- 백엔드: 3DLook API 연동 및 데이터 저장

### API 연동 플로우
```
1. 사용자가 정면/측면 사진 업로드
2. 백엔드에서 3DLook API 호출
3. AI가 신체 치수 측정 (30초~1분)
4. 측정 결과를 DB에 저장
5. 상품 조회 시 사이즈 추천 제공
```

### 데이터베이스 변경사항

#### 1) User 모델 변경
```python
# app/models/user.py에 추가될 필드들

class User(Model):
    # ... 기존 필드들 ...

    # 3DLook 관련 필드
    body_scan_id = fields.CharField(max_length=255, null=True)  # 3DLook 스캔 ID
    last_scanned_at = fields.DatetimeField(null=True)  # 마지막 스캔 일시
```

#### 2) 새로운 모델: BodyMeasurement (신체 치수)
```python
# app/models/body_measurement.py

class BodyMeasurement(Model):
    """신체 치수 모델 (3DLook)"""

    id = fields.IntField(pk=True)

    # 외래키: User
    user = fields.ForeignKeyField("models.User", related_name="body_measurements", on_delete=fields.OnDelete.CASCADE)

    # 3DLook 데이터
    scan_id = fields.CharField(max_length=255, unique=True)  # 3DLook 스캔 ID
    front_image_url = fields.CharField(max_length=500)  # 정면 사진
    side_image_url = fields.CharField(max_length=500)  # 측면 사진

    # 신체 치수 (단위: cm)
    height = fields.IntField()  # 키
    weight = fields.IntField(null=True)  # 몸무게 (선택)

    chest = fields.DecimalField(max_digits=5, decimal_places=1)  # 가슴둘레
    waist = fields.DecimalField(max_digits=5, decimal_places=1)  # 허리둘레
    hips = fields.DecimalField(max_digits=5, decimal_places=1)  # 엉덩이둘레

    shoulder_width = fields.DecimalField(max_digits=5, decimal_places=1, null=True)  # 어깨너비
    arm_length = fields.DecimalField(max_digits=5, decimal_places=1, null=True)  # 팔 길이
    inseam = fields.DecimalField(max_digits=5, decimal_places=1, null=True)  # 다리 안쪽 길이

    # 전체 측정 데이터 (JSON)
    raw_data = fields.JSONField()  # 3DLook의 모든 측정값

    # 활성 상태
    is_active = fields.BooleanField(default=True)  # 최신 측정값만 활성화

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "body_measurements"
        ordering = ["-created_at"]
```

#### 3) SizeRecommendation 모델 (선택사항)
```python
# app/models/size_recommendation.py

class SizeRecommendation(Model):
    """사이즈 추천 로그"""

    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="size_recommendations", on_delete=fields.OnDelete.CASCADE)
    product = fields.ForeignKeyField("models.Product", related_name="size_recommendations", on_delete=fields.OnDelete.CASCADE)
    body_measurement = fields.ForeignKeyField("models.BodyMeasurement", related_name="recommendations", on_delete=fields.OnDelete.CASCADE)

    # 추천 결과
    recommended_size = fields.CharField(max_length=20)  # 추천 사이즈
    confidence_score = fields.DecimalField(max_digits=5, decimal_places=2)  # 신뢰도 (0-100)

    # 피드백
    was_helpful = fields.BooleanField(null=True)  # 추천이 도움됐는지
    actual_purchased_size = fields.CharField(max_length=20, null=True)  # 실제 구매 사이즈

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "size_recommendations"
```

### API 엔드포인트 (예정)

```python
# app/routes/body_scan.py

POST   /body-scan/upload        # 사진 업로드 및 스캔 요청
GET    /body-scan/status/{id}   # 스캔 진행 상태 확인
GET    /body-scan/result/{id}   # 스캔 결과 조회
GET    /body-scan/my            # 내 신체 치수 조회
DELETE /body-scan/{id}          # 스캔 데이터 삭제

GET    /products/{id}/size-recommendation  # 상품별 사이즈 추천
POST   /size-recommendation/feedback       # 추천 피드백
```

### 기존 모델 변경 요약

#### ✅ 변경 필요 없는 모델
- **Product**: 그대로 유지
- **ProductOption**: 그대로 유지
- **Review**: 이미 user_height, user_weight 필드 있음 (재사용 가능)

#### ➕ 추가할 모델
1. **BodyMeasurement** (필수) - 신체 치수 저장
2. **SizeRecommendation** (선택) - 추천 이력 및 피드백

#### 🔧 수정할 모델
1. **User** (최소한의 변경)
   - `body_scan_id` 필드 추가 (nullable)
   - `last_scanned_at` 필드 추가 (nullable)

### 장점

1. **기존 시스템에 영향 최소화**
   - 새 테이블만 추가
   - 기존 코드 수정 거의 없음

2. **점진적 추가 가능**
   - 먼저 BodyMeasurement만 추가
   - 나중에 SizeRecommendation 추가

3. **선택적 기능**
   - 사용자가 스캔 안 해도 쇼핑 가능
   - 스캔한 사용자만 추천 받음

### 예상 비용
- 3DLook API: 스캔당 $0.50 ~ $2.00 (플랜에 따라)
- 월 구독: $500 ~ $2000+ (사용량 기반)

### 구현 우선순위
- **Priority**: Medium-High
- **Phase**: Phase 2-3
- **예상 개발 기간**: 2-3주
- **의존성**:
  - User 인증 완료
  - Product/Order 시스템 완료
  - 이미지 업로드 시스템 (S3 등)

### 참고 링크
- 3DLook 공식: https://3dlook.ai/
- API 문서: https://docs.3dlook.ai/
- 데모: https://3dlook.ai/demo/

---

## 2. 소셜 로그인 (Phase 2)

### 개요
카카오, 네이버, 구글 소셜 로그인 지원

### 구현 예정
- 카카오 로그인
- 네이버 로그인
- 구글 로그인

### 데이터베이스 변경
User 모델에 이미 `provider`, `provider_id` 필드 존재 - 변경 불필요

---

## 3. 실시간 재입고 알림 (Phase 2)

### 개요
품절 상품 재입고 시 알림 발송

### 기능
- 품절 상품 "알림 신청"
- 재입고 시 이메일/푸시 알림
- Notification 모델 활용

---

## 4. AI 상품 추천 (Phase 3)

### 개요
구매 이력 기반 개인화 추천

### 기능
- 유사 상품 추천
- 스타일 기반 추천
- 협업 필터링

---

## 5. 이미지 업로드 시스템 (Phase 2)

### 개요
AWS S3 또는 Cloudinary 연동

### 용도
- 상품 이미지
- 리뷰 이미지
- 3DLook 사진
- 반품 이미지

---

## 6. 어드민 대시보드 (Phase 3)

### 개요
관리자 전용 대시보드

### 기능
- 매출 통계
- 재고 현황
- 주문 관리
- 고객 관리
- 정산 관리

---

이 문서는 지속적으로 업데이트됩니다.