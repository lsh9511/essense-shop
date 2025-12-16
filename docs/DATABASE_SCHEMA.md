# DATABASE SCHEMA
# ESSENCE - 편집샵 데이터베이스 설계

## ERD (Entity Relationship Diagram)

```
┌─────────────┐         ┌──────────────┐         ┌─────────────────┐
│   users     │────1:N──│   addresses  │         │    brands       │
│             │         │              │         │                 │
└──────┬──────┘         └──────────────┘         └────────┬────────┘
       │                                                   │
       │ 1:N                                              │ 1:N
       │                                                   │
┌──────┴──────┐         ┌──────────────┐         ┌────────┴────────┐
│  wishlists  │         │   coupons    │         │    products     │
│             │         │              │         │                 │
└─────────────┘         └──────┬───────┘         └────────┬────────┘
                               │                          │
       ┌───────────────────────┘                          │ 1:N
       │ N:M                                              │
       │                                         ┌────────┴────────┐
┌──────┴────────┐         ┌──────────────┐     │ product_options │
│ user_coupons  │         │  cart_items  │     │                 │
│               │         │              │     └─────────────────┘
└───────────────┘         └──────┬───────┘              │
                                 │                      │ 1:N
       ┌─────────────┐           │ N:1                  │
       │   reviews   │           │              ┌───────┴─────────┐
       │             │    ┌──────┴──────┐       │    inventory    │
       └──────┬──────┘    │    carts    │       │                 │
              │           │             │       └─────────────────┘
              │ 1:N       └─────────────┘
              │                                  ┌─────────────────┐
       ┌──────┴──────┐         ┌──────────┐     │ product_images  │
       │review_images│         │  orders  │     │                 │
       │             │         │          │     └─────────────────┘
       └─────────────┘         └────┬─────┘
                                    │
                                    │ 1:N
                           ┌────────┴────────┐
                           │  order_items    │
                           │                 │
                           └──────┬──────────┘
                                  │
                                  │ 1:1
                           ┌──────┴──────┐
                           │  payments   │
                           │             │
                           └─────────────┘
                                  │
                                  │ 1:N
                           ┌──────┴──────┐
                           │   returns   │
                           │             │
                           └─────────────┘
```

---

## 테이블 상세 설계

### 1. users (사용자)

사용자 정보를 저장하는 테이블입니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 사용자 고유 ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | - | 이메일 (로그인 ID) |
| password_hash | VARCHAR(255) | NULL | - | 비밀번호 해시 (소셜 로그인 시 NULL) |
| name | VARCHAR(50) | NOT NULL | - | 이름 |
| phone | VARCHAR(20) | NOT NULL | - | 전화번호 |
| birth_date | DATE | NULL | - | 생년월일 |
| gender | VARCHAR(10) | NULL | - | 성별 (male, female, other) |
| role | VARCHAR(20) | NOT NULL | 'customer' | 역할 (customer, admin) |
| provider | VARCHAR(20) | NULL | - | 소셜 로그인 제공자 (kakao, naver, google) |
| provider_id | VARCHAR(255) | NULL | - | 소셜 로그인 ID |
| marketing_agree | BOOLEAN | NOT NULL | FALSE | 마케팅 수신 동의 |
| is_active | BOOLEAN | NOT NULL | TRUE | 활성 상태 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 가입일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_users_email` ON email
- `idx_users_phone` ON phone

**샘플 데이터**:
```sql
INSERT INTO users (email, password_hash, name, phone, role) VALUES
('admin@essence.com', '$2b$10$...', '관리자', '010-1234-5678', 'admin'),
('user@example.com', '$2b$10$...', '홍길동', '010-9876-5432', 'customer');
```

---

### 2. addresses (배송지)

사용자의 배송지 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 배송지 고유 ID |
| user_id | INTEGER | FK(users.id), NOT NULL | - | 사용자 ID |
| recipient_name | VARCHAR(50) | NOT NULL | - | 수령인명 |
| phone | VARCHAR(20) | NOT NULL | - | 연락처 |
| postal_code | VARCHAR(10) | NOT NULL | - | 우편번호 |
| address_line1 | VARCHAR(255) | NOT NULL | - | 주소 |
| address_line2 | VARCHAR(255) | NULL | - | 상세 주소 |
| is_default | BOOLEAN | NOT NULL | FALSE | 기본 배송지 여부 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 등록일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_addresses_user_id` ON user_id

**외래키**:
- `fk_addresses_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

---

### 3. brands (브랜드)

입점 브랜드 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 브랜드 고유 ID |
| name | VARCHAR(100) | UNIQUE, NOT NULL | - | 브랜드명 |
| name_en | VARCHAR(100) | NULL | - | 영문 브랜드명 |
| logo_url | VARCHAR(500) | NULL | - | 로고 이미지 URL |
| description | TEXT | NULL | - | 브랜드 소개 |
| story | TEXT | NULL | - | 브랜드 스토리 |
| instagram | VARCHAR(255) | NULL | - | 인스타그램 URL |
| website | VARCHAR(255) | NULL | - | 웹사이트 URL |
| contact_name | VARCHAR(50) | NULL | - | 담당자명 |
| contact_phone | VARCHAR(20) | NULL | - | 담당자 연락처 |
| contact_email | VARCHAR(255) | NULL | - | 담당자 이메일 |
| commission_rate | DECIMAL(5,2) | NOT NULL | 0.00 | 정산 수수료율 (%) |
| is_active | BOOLEAN | NOT NULL | TRUE | 활성 상태 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 등록일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_brands_name` ON name

**샘플 데이터**:
```sql
INSERT INTO brands (name, name_en, description) VALUES
('미니멀웍스', 'Minimal Works', '본질에 집중하는 디자인'),
('플레인스튜디오', 'Plain Studio', '일상의 미학');
```

---

### 4. products (상품)

상품 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 상품 고유 ID |
| brand_id | INTEGER | FK(brands.id), NOT NULL | - | 브랜드 ID |
| name | VARCHAR(255) | NOT NULL | - | 상품명 |
| category | VARCHAR(50) | NOT NULL | - | 카테고리 (tops, bottoms, outerwear, shoes, accessories) |
| price | INTEGER | NOT NULL | - | 정가 (원) |
| sale_price | INTEGER | NULL | - | 할인가 (원) |
| description | TEXT | NULL | - | 상품 설명 |
| material | VARCHAR(255) | NULL | - | 소재 |
| country_of_origin | VARCHAR(50) | NULL | - | 제조국 |
| care_instructions | TEXT | NULL | - | 세탁 방법 |
| model_height | INTEGER | NULL | - | 착용 모델 키 (cm) |
| model_weight | INTEGER | NULL | - | 착용 모델 몸무게 (kg) |
| model_size | VARCHAR(10) | NULL | - | 착용 모델 사이즈 |
| shipping_fee | INTEGER | NOT NULL | 3000 | 배송비 (원) |
| shipping_days | VARCHAR(50) | NULL | '2-3일' | 배송 기간 |
| status | VARCHAR(20) | NOT NULL | 'active' | 상태 (active, sold_out, inactive) |
| view_count | INTEGER | NOT NULL | 0 | 조회수 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 등록일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_products_brand_id` ON brand_id
- `idx_products_category` ON category
- `idx_products_status` ON status
- `idx_products_created_at` ON created_at DESC

**외래키**:
- `fk_products_brand` FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE RESTRICT

**샘플 데이터**:
```sql
INSERT INTO products (brand_id, name, category, price, description) VALUES
(1, '오버핏 코튼 셔츠', 'tops', 89000, '데일리로 입기 좋은 오버핏 셔츠'),
(1, '와이드 슬랙스', 'bottoms', 125000, '편안한 와이드 핏 슬랙스');
```

---

### 5. product_options (상품 옵션)

상품의 사이즈, 컬러 옵션을 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 옵션 고유 ID |
| product_id | INTEGER | FK(products.id), NOT NULL | - | 상품 ID |
| size | VARCHAR(20) | NOT NULL | - | 사이즈 (S, M, L, XL, FREE 등) |
| color | VARCHAR(50) | NOT NULL | - | 컬러명 (블랙, 화이트, 베이지 등) |
| color_code | VARCHAR(7) | NULL | - | 컬러 코드 (#000000) |
| additional_price | INTEGER | NOT NULL | 0 | 추가 가격 (원) |
| is_active | BOOLEAN | NOT NULL | TRUE | 활성 상태 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 등록일시 |

**인덱스**:
- `idx_product_options_product_id` ON product_id
- `idx_product_options_unique` UNIQUE ON (product_id, size, color)

**외래키**:
- `fk_product_options_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE

**샘플 데이터**:
```sql
INSERT INTO product_options (product_id, size, color, color_code) VALUES
(1, 'M', '블랙', '#000000'),
(1, 'M', '화이트', '#FFFFFF'),
(1, 'L', '블랙', '#000000');
```

---

### 6. product_images (상품 이미지)

상품 이미지를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 이미지 고유 ID |
| product_id | INTEGER | FK(products.id), NOT NULL | - | 상품 ID |
| image_url | VARCHAR(500) | NOT NULL | - | 이미지 URL |
| display_order | INTEGER | NOT NULL | 0 | 노출 순서 |
| is_thumbnail | BOOLEAN | NOT NULL | FALSE | 썸네일 여부 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 등록일시 |

**인덱스**:
- `idx_product_images_product_id` ON product_id
- `idx_product_images_order` ON (product_id, display_order)

**외래키**:
- `fk_product_images_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE

---

### 7. inventory (재고)

상품 옵션별 재고를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 재고 고유 ID |
| product_option_id | INTEGER | FK(product_options.id), UNIQUE, NOT NULL | - | 상품 옵션 ID |
| quantity | INTEGER | NOT NULL | 0 | 현재 재고 수량 |
| safe_stock | INTEGER | NOT NULL | 5 | 안전 재고 (최소 유지 수량) |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_inventory_product_option_id` ON product_option_id
- `idx_inventory_low_stock` ON quantity WHERE quantity <= safe_stock

**외래키**:
- `fk_inventory_product_option` FOREIGN KEY (product_option_id) REFERENCES product_options(id) ON DELETE CASCADE

**샘플 데이터**:
```sql
INSERT INTO inventory (product_option_id, quantity, safe_stock) VALUES
(1, 50, 10),
(2, 30, 10),
(3, 20, 5);
```

---

### 8. carts (장바구니)

사용자의 장바구니를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 장바구니 고유 ID |
| user_id | INTEGER | FK(users.id), UNIQUE, NOT NULL | - | 사용자 ID |
| created_at | TIMESTAMP | NOT NULL | NOW() | 생성일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**외래키**:
- `fk_carts_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

---

### 9. cart_items (장바구니 아이템)

장바구니에 담긴 상품을 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 아이템 고유 ID |
| cart_id | INTEGER | FK(carts.id), NOT NULL | - | 장바구니 ID |
| product_option_id | INTEGER | FK(product_options.id), NOT NULL | - | 상품 옵션 ID |
| quantity | INTEGER | NOT NULL | 1 | 수량 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 추가일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_cart_items_cart_id` ON cart_id
- `idx_cart_items_unique` UNIQUE ON (cart_id, product_option_id)

**외래키**:
- `fk_cart_items_cart` FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE
- `fk_cart_items_product_option` FOREIGN KEY (product_option_id) REFERENCES product_options(id) ON DELETE CASCADE

---

### 10. orders (주문)

주문 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 주문 고유 ID |
| order_number | VARCHAR(50) | UNIQUE, NOT NULL | - | 주문번호 (예: ORD-20250101-0001) |
| user_id | INTEGER | FK(users.id), NOT NULL | - | 사용자 ID |
| recipient_name | VARCHAR(50) | NOT NULL | - | 수령인명 |
| recipient_phone | VARCHAR(20) | NOT NULL | - | 수령인 연락처 |
| postal_code | VARCHAR(10) | NOT NULL | - | 우편번호 |
| address_line1 | VARCHAR(255) | NOT NULL | - | 주소 |
| address_line2 | VARCHAR(255) | NULL | - | 상세 주소 |
| delivery_memo | TEXT | NULL | - | 배송 메모 |
| total_product_price | INTEGER | NOT NULL | - | 총 상품 금액 (원) |
| shipping_fee | INTEGER | NOT NULL | 3000 | 배송비 (원) |
| discount_amount | INTEGER | NOT NULL | 0 | 할인 금액 (원, 쿠폰) |
| final_price | INTEGER | NOT NULL | - | 최종 결제 금액 (원) |
| order_status | VARCHAR(20) | NOT NULL | 'pending' | 주문 상태 (pending, paid, preparing, shipping, delivered, confirmed, cancelled) |
| shipping_status | VARCHAR(20) | NULL | - | 배송 상태 (pending, shipped, in_transit, delivered) |
| courier_company | VARCHAR(50) | NULL | - | 택배사 |
| tracking_number | VARCHAR(50) | NULL | - | 송장번호 |
| shipped_at | TIMESTAMP | NULL | - | 발송일시 |
| delivered_at | TIMESTAMP | NULL | - | 배송 완료일시 |
| confirmed_at | TIMESTAMP | NULL | - | 구매 확정일시 |
| cancelled_at | TIMESTAMP | NULL | - | 취소일시 |
| cancel_reason | TEXT | NULL | - | 취소 사유 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 주문일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_orders_order_number` UNIQUE ON order_number
- `idx_orders_user_id` ON user_id
- `idx_orders_status` ON order_status
- `idx_orders_created_at` ON created_at DESC

**외래키**:
- `fk_orders_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT

**주문번호 생성 예시**:
```python
# ORD-YYYYMMDD-NNNN 형식
order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{seq:04d}"
```

---

### 11. order_items (주문 상품)

주문에 포함된 상품을 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 주문 상품 고유 ID |
| order_id | INTEGER | FK(orders.id), NOT NULL | - | 주문 ID |
| product_option_id | INTEGER | FK(product_options.id), NOT NULL | - | 상품 옵션 ID |
| product_name | VARCHAR(255) | NOT NULL | - | 상품명 (주문 시점 스냅샷) |
| brand_name | VARCHAR(100) | NOT NULL | - | 브랜드명 (주문 시점 스냅샷) |
| size | VARCHAR(20) | NOT NULL | - | 사이즈 (주문 시점 스냅샷) |
| color | VARCHAR(50) | NOT NULL | - | 컬러 (주문 시점 스냅샷) |
| price | INTEGER | NOT NULL | - | 상품 가격 (주문 시점 스냅샷) |
| quantity | INTEGER | NOT NULL | 1 | 수량 |
| subtotal | INTEGER | NOT NULL | - | 소계 (price * quantity) |
| created_at | TIMESTAMP | NOT NULL | NOW() | 생성일시 |

**인덱스**:
- `idx_order_items_order_id` ON order_id

**외래키**:
- `fk_order_items_order` FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
- `fk_order_items_product_option` FOREIGN KEY (product_option_id) REFERENCES product_options(id) ON DELETE RESTRICT

---

### 12. payments (결제)

결제 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 결제 고유 ID |
| order_id | INTEGER | FK(orders.id), UNIQUE, NOT NULL | - | 주문 ID |
| payment_key | VARCHAR(255) | UNIQUE, NOT NULL | - | 결제 키 (Toss Payments) |
| payment_method | VARCHAR(50) | NOT NULL | - | 결제 수단 (card, transfer, toss, naverpay, kakaopay) |
| amount | INTEGER | NOT NULL | - | 결제 금액 (원) |
| status | VARCHAR(20) | NOT NULL | 'pending' | 결제 상태 (pending, completed, failed, cancelled, refunded) |
| paid_at | TIMESTAMP | NULL | - | 결제 완료일시 |
| cancelled_at | TIMESTAMP | NULL | - | 취소일시 |
| refunded_at | TIMESTAMP | NULL | - | 환불일시 |
| failure_reason | TEXT | NULL | - | 실패 사유 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 생성일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_payments_order_id` UNIQUE ON order_id
- `idx_payments_payment_key` UNIQUE ON payment_key
- `idx_payments_status` ON status

**외래키**:
- `fk_payments_order` FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE RESTRICT

---

### 13. reviews (리뷰)

상품 리뷰를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 리뷰 고유 ID |
| user_id | INTEGER | FK(users.id), NOT NULL | - | 사용자 ID |
| product_id | INTEGER | FK(products.id), NOT NULL | - | 상품 ID |
| order_item_id | INTEGER | FK(order_items.id), UNIQUE, NOT NULL | - | 주문 상품 ID |
| rating | INTEGER | NOT NULL | - | 별점 (1-5) |
| content | TEXT | NOT NULL | - | 리뷰 내용 |
| user_height | INTEGER | NULL | - | 작성자 키 (cm) |
| user_weight | INTEGER | NULL | - | 작성자 몸무게 (kg) |
| purchased_size | VARCHAR(20) | NULL | - | 구매한 사이즈 |
| size_satisfaction | VARCHAR(20) | NULL | - | 사이즈 만족도 (small, perfect, large) |
| is_visible | BOOLEAN | NOT NULL | TRUE | 노출 여부 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 작성일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_reviews_user_id` ON user_id
- `idx_reviews_product_id` ON product_id
- `idx_reviews_order_item_id` UNIQUE ON order_item_id
- `idx_reviews_created_at` ON created_at DESC

**외래키**:
- `fk_reviews_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- `fk_reviews_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
- `fk_reviews_order_item` FOREIGN KEY (order_item_id) REFERENCES order_items(id) ON DELETE CASCADE

---

### 14. review_images (리뷰 이미지)

리뷰에 첨부된 이미지를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 이미지 고유 ID |
| review_id | INTEGER | FK(reviews.id), NOT NULL | - | 리뷰 ID |
| image_url | VARCHAR(500) | NOT NULL | - | 이미지 URL |
| display_order | INTEGER | NOT NULL | 0 | 노출 순서 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 등록일시 |

**인덱스**:
- `idx_review_images_review_id` ON review_id

**외래키**:
- `fk_review_images_review` FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE

---

### 15. wishlists (찜하기)

사용자의 찜한 상품을 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 찜 고유 ID |
| user_id | INTEGER | FK(users.id), NOT NULL | - | 사용자 ID |
| product_id | INTEGER | FK(products.id), NOT NULL | - | 상품 ID |
| created_at | TIMESTAMP | NOT NULL | NOW() | 추가일시 |

**인덱스**:
- `idx_wishlists_user_id` ON user_id
- `idx_wishlists_unique` UNIQUE ON (user_id, product_id)

**외래키**:
- `fk_wishlists_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- `fk_wishlists_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE

---

### 16. coupons (쿠폰)

쿠폰 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 쿠폰 고유 ID |
| code | VARCHAR(50) | UNIQUE, NOT NULL | - | 쿠폰 코드 |
| name | VARCHAR(100) | NOT NULL | - | 쿠폰명 |
| discount_type | VARCHAR(20) | NOT NULL | - | 할인 타입 (fixed, percent) |
| discount_value | INTEGER | NOT NULL | - | 할인 값 (정액: 원, 정률: %) |
| min_order_amount | INTEGER | NOT NULL | 0 | 최소 주문 금액 (원) |
| max_discount_amount | INTEGER | NULL | - | 최대 할인 금액 (정률일 때, 원) |
| quantity | INTEGER | NULL | - | 발급 수량 (NULL: 무제한) |
| issued_count | INTEGER | NOT NULL | 0 | 발급된 수량 |
| start_date | TIMESTAMP | NOT NULL | - | 사용 시작일 |
| end_date | TIMESTAMP | NOT NULL | - | 사용 종료일 |
| is_active | BOOLEAN | NOT NULL | TRUE | 활성 상태 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 생성일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_coupons_code` UNIQUE ON code
- `idx_coupons_dates` ON (start_date, end_date)

**샘플 데이터**:
```sql
INSERT INTO coupons (code, name, discount_type, discount_value, min_order_amount, start_date, end_date) VALUES
('WELCOME10', '신규 회원 10% 할인', 'percent', 10, 100000, '2025-01-01', '2025-12-31'),
('FREESHIP', '무료 배송', 'fixed', 3000, 50000, '2025-01-01', '2025-12-31');
```

---

### 17. user_coupons (사용자 쿠폰)

사용자에게 발급된 쿠폰을 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 사용자 쿠폰 고유 ID |
| user_id | INTEGER | FK(users.id), NOT NULL | - | 사용자 ID |
| coupon_id | INTEGER | FK(coupons.id), NOT NULL | - | 쿠폰 ID |
| is_used | BOOLEAN | NOT NULL | FALSE | 사용 여부 |
| used_at | TIMESTAMP | NULL | - | 사용일시 |
| order_id | INTEGER | FK(orders.id), NULL | - | 사용한 주문 ID |
| issued_at | TIMESTAMP | NOT NULL | NOW() | 발급일시 |

**인덱스**:
- `idx_user_coupons_user_id` ON user_id
- `idx_user_coupons_unique` UNIQUE ON (user_id, coupon_id) WHERE is_used = FALSE

**외래키**:
- `fk_user_coupons_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- `fk_user_coupons_coupon` FOREIGN KEY (coupon_id) REFERENCES coupons(id) ON DELETE CASCADE
- `fk_user_coupons_order` FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL

---

### 18. returns (교환/반품)

교환/반품 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 교환/반품 고유 ID |
| order_id | INTEGER | FK(orders.id), NOT NULL | - | 주문 ID |
| return_type | VARCHAR(20) | NOT NULL | - | 타입 (return, exchange) |
| reason | VARCHAR(100) | NOT NULL | - | 사유 (단순 변심, 사이즈 불만족, 불량 등) |
| detailed_reason | TEXT | NULL | - | 상세 사유 |
| image_urls | TEXT[] | NULL | - | 첨부 이미지 URL 배열 |
| status | VARCHAR(20) | NOT NULL | 'requested' | 상태 (requested, approved, collecting, collected, completed, rejected) |
| refund_amount | INTEGER | NULL | - | 환불 금액 (원) |
| courier_company | VARCHAR(50) | NULL | - | 수거 택배사 |
| tracking_number | VARCHAR(50) | NULL | - | 수거 송장번호 |
| approved_at | TIMESTAMP | NULL | - | 승인일시 |
| collected_at | TIMESTAMP | NULL | - | 수거 완료일시 |
| completed_at | TIMESTAMP | NULL | - | 처리 완료일시 |
| rejected_reason | TEXT | NULL | - | 거부 사유 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 신청일시 |
| updated_at | TIMESTAMP | NOT NULL | NOW() | 수정일시 |

**인덱스**:
- `idx_returns_order_id` ON order_id
- `idx_returns_status` ON status

**외래키**:
- `fk_returns_order` FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE RESTRICT

---

### 19. notifications (알림)

사용자 및 어드민 알림을 저장합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 알림 고유 ID |
| user_id | INTEGER | FK(users.id), NULL | - | 사용자 ID (NULL: 어드민 알림) |
| type | VARCHAR(50) | NOT NULL | - | 알림 타입 (order, shipping, restock, coupon, review, return) |
| title | VARCHAR(255) | NOT NULL | - | 알림 제목 |
| content | TEXT | NOT NULL | - | 알림 내용 |
| link_url | VARCHAR(500) | NULL | - | 링크 URL |
| is_read | BOOLEAN | NOT NULL | FALSE | 읽음 여부 |
| read_at | TIMESTAMP | NULL | - | 읽은 일시 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 생성일시 |

**인덱스**:
- `idx_notifications_user_id` ON user_id
- `idx_notifications_read` ON (user_id, is_read)
- `idx_notifications_created_at` ON created_at DESC

**외래키**:
- `fk_notifications_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

---

### 20. admin_logs (어드민 로그)

어드민의 주요 작업을 기록합니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 기본값 | 설명 |
|--------|-----------|---------|--------|------|
| id | SERIAL | PK | - | 로그 고유 ID |
| admin_id | INTEGER | FK(users.id), NOT NULL | - | 어드민 ID |
| action | VARCHAR(50) | NOT NULL | - | 작업 (create, update, delete, approve, reject 등) |
| target_type | VARCHAR(50) | NOT NULL | - | 대상 타입 (product, order, return, coupon 등) |
| target_id | INTEGER | NULL | - | 대상 ID |
| description | TEXT | NULL | - | 작업 설명 |
| ip_address | VARCHAR(45) | NULL | - | IP 주소 |
| created_at | TIMESTAMP | NOT NULL | NOW() | 작업일시 |

**인덱스**:
- `idx_admin_logs_admin_id` ON admin_id
- `idx_admin_logs_created_at` ON created_at DESC

**외래키**:
- `fk_admin_logs_admin` FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE RESTRICT

---

## 뷰 (Views)

### 1. product_statistics (상품 통계 뷰)

상품별 판매 통계를 제공합니다.

```sql
CREATE VIEW product_statistics AS
SELECT
    p.id AS product_id,
    p.name AS product_name,
    b.name AS brand_name,
    COUNT(DISTINCT o.id) AS total_orders,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue,
    AVG(r.rating) AS average_rating,
    COUNT(r.id) AS review_count
FROM products p
LEFT JOIN brands b ON p.brand_id = b.id
LEFT JOIN product_options po ON p.id = po.product_id
LEFT JOIN order_items oi ON po.id = oi.product_option_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.order_status NOT IN ('cancelled')
LEFT JOIN reviews r ON p.id = r.product_id
GROUP BY p.id, p.name, b.name;
```

### 2. inventory_alerts (재고 알림 뷰)

안전 재고 이하의 상품을 표시합니다.

```sql
CREATE VIEW inventory_alerts AS
SELECT
    p.id AS product_id,
    p.name AS product_name,
    b.name AS brand_name,
    po.size,
    po.color,
    i.quantity AS current_stock,
    i.safe_stock
FROM inventory i
JOIN product_options po ON i.product_option_id = po.id
JOIN products p ON po.product_id = p.id
JOIN brands b ON p.brand_id = b.id
WHERE i.quantity <= i.safe_stock;
```

---

## 인덱스 전략

### 복합 인덱스
```sql
-- 상품 검색 최적화
CREATE INDEX idx_products_search ON products(status, category, created_at DESC);

-- 주문 조회 최적화 (어드민)
CREATE INDEX idx_orders_admin_search ON orders(order_status, created_at DESC);

-- 리뷰 조회 최적화
CREATE INDEX idx_reviews_product_rating ON reviews(product_id, rating DESC, created_at DESC);
```

---

## 트리거 (Triggers)

### 1. 주문 시 재고 차감

```sql
CREATE OR REPLACE FUNCTION decrease_inventory()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE inventory
    SET quantity = quantity - NEW.quantity,
        updated_at = NOW()
    WHERE product_option_id = NEW.product_option_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_decrease_inventory
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION decrease_inventory();
```

### 2. 주문 취소 시 재고 복구

```sql
CREATE OR REPLACE FUNCTION restore_inventory()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.order_status = 'cancelled' AND OLD.order_status <> 'cancelled' THEN
        UPDATE inventory i
        SET quantity = quantity + oi.quantity,
            updated_at = NOW()
        FROM order_items oi
        WHERE oi.order_id = NEW.id
          AND i.product_option_id = oi.product_option_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_restore_inventory
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION restore_inventory();
```

### 3. 상품 상태 자동 업데이트 (품절)

```sql
CREATE OR REPLACE FUNCTION update_product_status()
RETURNS TRIGGER AS $$
BEGIN
    -- 모든 옵션의 재고가 0이면 상품 상태를 'sold_out'으로 변경
    IF (SELECT SUM(i.quantity)
        FROM inventory i
        JOIN product_options po ON i.product_option_id = po.id
        WHERE po.product_id = (
            SELECT product_id FROM product_options WHERE id = NEW.product_option_id
        )) = 0 THEN

        UPDATE products
        SET status = 'sold_out'
        WHERE id = (SELECT product_id FROM product_options WHERE id = NEW.product_option_id);

    -- 재고가 있으면 'active'로 변경
    ELSIF (SELECT SUM(i.quantity)
           FROM inventory i
           JOIN product_options po ON i.product_option_id = po.id
           WHERE po.product_id = (
               SELECT product_id FROM product_options WHERE id = NEW.product_option_id
           )) > 0 THEN

        UPDATE products
        SET status = 'active'
        WHERE id = (SELECT product_id FROM product_options WHERE id = NEW.product_option_id)
          AND status = 'sold_out';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_product_status
AFTER UPDATE ON inventory
FOR EACH ROW
EXECUTE FUNCTION update_product_status();
```

---

## 백업 및 유지보수

### 백업 전략
- **일일 전체 백업**: 매일 새벽 3시 자동 백업
- **증분 백업**: 매 6시간마다
- **보관 기간**: 30일

### 파티셔닝
대용량 데이터 처리를 위해 날짜 기반 파티셔닝을 고려합니다.

```sql
-- orders 테이블 파티셔닝 (월별)
CREATE TABLE orders_2025_01 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE orders_2025_02 PARTITION OF orders
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
```

---

## 데이터 정합성 체크

### 재고 정합성 검증 쿼리
```sql
-- 주문된 수량과 재고 차감이 일치하는지 확인
SELECT
    po.id,
    p.name,
    po.size,
    po.color,
    i.quantity AS current_stock,
    COALESCE(SUM(oi.quantity), 0) AS total_ordered
FROM product_options po
LEFT JOIN inventory i ON po.id = i.product_option_id
LEFT JOIN order_items oi ON po.id = oi.product_option_id
LEFT JOIN orders o ON oi.order_id = o.id
LEFT JOIN products p ON po.product_id = p.id
WHERE o.order_status NOT IN ('cancelled')
GROUP BY po.id, p.name, po.size, po.color, i.quantity;
```

---

이 스키마는 확장 가능하며, Phase별로 필요한 테이블을 추가할 수 있습니다.