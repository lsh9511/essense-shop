# API 명세서 (API Specification)
# ESSENCE - 편집샵 API

## 기본 정보

- **Base URL**: `https://api.essence-shop.com/v1`
- **Content-Type**: `application/json`
- **인증 방식**: Bearer JWT Token

---

## 인증 (Authentication)

### 1.1. 회원가입

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123!",
  "name": "홍길동",
  "phone": "010-1234-5678",
  "birth_date": "1990-01-01",
  "gender": "male",
  "marketing_agree": true
}
```

**Response (201):**
```json
{
  "message": "회원가입이 완료되었습니다.",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "홍길동",
      "phone": "010-1234-5678"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expires_in": 3600
    }
  }
}
```

**Validation:**
- 이메일: 유효한 이메일 형식
- 비밀번호: 8자 이상, 영문 대소문자, 숫자 포함
- 전화번호: 010-XXXX-XXXX 형식

**Error (400):**
```json
{
  "error": "VALIDATION_ERROR",
  "message": "이미 사용 중인 이메일입니다."
}
```

---

### 1.2. 로그인

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

**Response (200):**
```json
{
  "message": "로그인 성공",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "홍길동",
      "role": "customer"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expires_in": 3600
    }
  }
}
```

**Error (401):**
```json
{
  "error": "UNAUTHORIZED",
  "message": "이메일 또는 비밀번호가 일치하지 않습니다."
}
```

---

### 1.3. 토큰 갱신

**Endpoint:** `POST /auth/refresh`
**Auth:** Bearer Token (Refresh Token)

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  }
}
```

---

### 1.4. 소셜 로그인

**Endpoint:** `POST /auth/social-login`

**Request Body:**
```json
{
  "provider": "kakao",
  "access_token": "kakao_access_token_here"
}
```

**Response (200):**
```json
{
  "message": "로그인 성공",
  "data": {
    "user": {
      "id": 1,
      "email": "user@kakao.com",
      "name": "홍길동",
      "provider": "kakao"
    },
    "tokens": {
      "access_token": "...",
      "refresh_token": "...",
      "expires_in": 3600
    }
  }
}
```

---

## 사용자 (Users)

### 2.1. 내 정보 조회

**Endpoint:** `GET /users/me`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "홍길동",
    "phone": "010-1234-5678",
    "birth_date": "1990-01-01",
    "gender": "male",
    "marketing_agree": true,
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

---

### 2.2. 내 정보 수정

**Endpoint:** `PATCH /users/me`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "name": "홍길동",
  "phone": "010-9999-8888",
  "birth_date": "1990-01-01",
  "gender": "male",
  "marketing_agree": false
}
```

**Response (200):**
```json
{
  "message": "정보가 수정되었습니다.",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "홍길동",
    "phone": "010-9999-8888"
  }
}
```

---

### 2.3. 배송지 목록 조회

**Endpoint:** `GET /users/me/addresses`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "recipient_name": "홍길동",
      "phone": "010-1234-5678",
      "postal_code": "12345",
      "address_line1": "서울시 강남구",
      "address_line2": "101동 101호",
      "is_default": true
    }
  ]
}
```

---

### 2.4. 배송지 추가

**Endpoint:** `POST /users/me/addresses`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "recipient_name": "홍길동",
  "phone": "010-1234-5678",
  "postal_code": "12345",
  "address_line1": "서울시 강남구",
  "address_line2": "101동 101호",
  "is_default": false
}
```

**Response (201):**
```json
{
  "message": "배송지가 추가되었습니다.",
  "data": {
    "id": 2,
    "recipient_name": "홍길동",
    "phone": "010-1234-5678",
    "postal_code": "12345",
    "address_line1": "서울시 강남구",
    "address_line2": "101동 101호",
    "is_default": false
  }
}
```

---

## 브랜드 (Brands)

### 3.1. 브랜드 목록 조회

**Endpoint:** `GET /brands`

**Query Parameters:**
- `page`: 페이지 번호 (default: 1)
- `limit`: 페이지당 항목 수 (default: 20)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "name": "미니멀웍스",
      "name_en": "Minimal Works",
      "logo_url": "https://cdn.essence-shop.com/brands/1/logo.jpg",
      "description": "본질에 집중하는 디자인"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 10,
    "total_pages": 1
  }
}
```

---

### 3.2. 브랜드 상세 조회

**Endpoint:** `GET /brands/{id}`

**Response (200):**
```json
{
  "data": {
    "id": 1,
    "name": "미니멀웍스",
    "name_en": "Minimal Works",
    "logo_url": "https://cdn.essence-shop.com/brands/1/logo.jpg",
    "description": "본질에 집중하는 디자인",
    "story": "2020년 창립된 미니멀웍스는...",
    "instagram": "https://instagram.com/minimalworks",
    "website": "https://minimalworks.com",
    "product_count": 25
  }
}
```

---

## 상품 (Products)

### 4.1. 상품 목록 조회

**Endpoint:** `GET /products`

**Query Parameters:**
- `page`: 페이지 번호 (default: 1)
- `limit`: 페이지당 항목 수 (default: 20)
- `category`: 카테고리 (tops, bottoms, outerwear, shoes, accessories)
- `brand_id`: 브랜드 ID
- `min_price`: 최소 가격
- `max_price`: 최대 가격
- `color`: 색상
- `size`: 사이즈
- `sort`: 정렬 (latest, popular, price_asc, price_desc)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "brand": {
        "id": 1,
        "name": "미니멀웍스"
      },
      "name": "오버핏 코튼 셔츠",
      "category": "tops",
      "price": 89000,
      "sale_price": 79000,
      "discount_rate": 11,
      "thumbnail_url": "https://cdn.essence-shop.com/products/1/thumb.jpg",
      "status": "active",
      "is_wishlisted": false,
      "view_count": 1234
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

---

### 4.2. 상품 상세 조회

**Endpoint:** `GET /products/{id}`

**Response (200):**
```json
{
  "data": {
    "id": 1,
    "brand": {
      "id": 1,
      "name": "미니멀웍스",
      "logo_url": "https://cdn.essence-shop.com/brands/1/logo.jpg"
    },
    "name": "오버핏 코튼 셔츠",
    "category": "tops",
    "price": 89000,
    "sale_price": 79000,
    "discount_rate": 11,
    "description": "데일리로 입기 좋은 오버핏 셔츠입니다.",
    "material": "코튼 100%",
    "country_of_origin": "대한민국",
    "care_instructions": "단독 세탁, 찬물 손세탁",
    "model_info": {
      "height": 178,
      "weight": 68,
      "size": "L"
    },
    "shipping_fee": 3000,
    "shipping_days": "2-3일",
    "images": [
      {
        "id": 1,
        "url": "https://cdn.essence-shop.com/products/1/image1.jpg",
        "is_thumbnail": true,
        "display_order": 0
      },
      {
        "id": 2,
        "url": "https://cdn.essence-shop.com/products/1/image2.jpg",
        "is_thumbnail": false,
        "display_order": 1
      }
    ],
    "options": [
      {
        "id": 1,
        "size": "M",
        "color": "블랙",
        "color_code": "#000000",
        "additional_price": 0,
        "stock": 50,
        "is_available": true
      },
      {
        "id": 2,
        "size": "M",
        "color": "화이트",
        "color_code": "#FFFFFF",
        "additional_price": 0,
        "stock": 0,
        "is_available": false
      }
    ],
    "size_guide": {
      "M": {
        "chest": 58,
        "length": 72,
        "shoulder": 50,
        "sleeve": 62
      },
      "L": {
        "chest": 60,
        "length": 74,
        "shoulder": 52,
        "sleeve": 64
      }
    },
    "review_summary": {
      "average_rating": 4.5,
      "total_reviews": 123,
      "rating_distribution": {
        "5": 80,
        "4": 30,
        "3": 10,
        "2": 2,
        "1": 1
      }
    },
    "is_wishlisted": false,
    "view_count": 1234,
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

---

### 4.3. 상품 검색

**Endpoint:** `GET /products/search`

**Query Parameters:**
- `q`: 검색어
- `page`: 페이지 번호 (default: 1)
- `limit`: 페이지당 항목 수 (default: 20)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "brand": {
        "id": 1,
        "name": "미니멀웍스"
      },
      "name": "오버핏 코튼 셔츠",
      "category": "tops",
      "price": 89000,
      "sale_price": 79000,
      "thumbnail_url": "https://cdn.essence-shop.com/products/1/thumb.jpg"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 10,
    "total_pages": 1
  }
}
```

---

## 장바구니 (Cart)

### 5.1. 장바구니 조회

**Endpoint:** `GET /cart`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "오버핏 코튼 셔츠",
          "thumbnail_url": "https://cdn.essence-shop.com/products/1/thumb.jpg",
          "brand_name": "미니멀웍스"
        },
        "option": {
          "id": 1,
          "size": "M",
          "color": "블랙",
          "additional_price": 0
        },
        "quantity": 2,
        "price": 79000,
        "subtotal": 158000,
        "is_available": true
      }
    ],
    "summary": {
      "total_product_price": 158000,
      "shipping_fee": 3000,
      "discount_amount": 0,
      "final_price": 161000
    }
  }
}
```

---

### 5.2. 장바구니에 상품 추가

**Endpoint:** `POST /cart/items`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "product_option_id": 1,
  "quantity": 2
}
```

**Response (201):**
```json
{
  "message": "장바구니에 추가되었습니다.",
  "data": {
    "id": 1,
    "product_option_id": 1,
    "quantity": 2
  }
}
```

**Error (400):**
```json
{
  "error": "OUT_OF_STOCK",
  "message": "재고가 부족합니다."
}
```

---

### 5.3. 장바구니 상품 수량 변경

**Endpoint:** `PATCH /cart/items/{id}`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response (200):**
```json
{
  "message": "수량이 변경되었습니다.",
  "data": {
    "id": 1,
    "quantity": 3
  }
}
```

---

### 5.4. 장바구니 상품 삭제

**Endpoint:** `DELETE /cart/items/{id}`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "message": "장바구니에서 삭제되었습니다."
}
```

---

## 주문 (Orders)

### 6.1. 주문 생성

**Endpoint:** `POST /orders`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "items": [
    {
      "product_option_id": 1,
      "quantity": 2
    }
  ],
  "recipient_name": "홍길동",
  "recipient_phone": "010-1234-5678",
  "postal_code": "12345",
  "address_line1": "서울시 강남구",
  "address_line2": "101동 101호",
  "delivery_memo": "부재시 문앞에 놓아주세요",
  "coupon_id": 1,
  "payment_method": "card"
}
```

**Response (201):**
```json
{
  "message": "주문이 생성되었습니다.",
  "data": {
    "order_id": 1,
    "order_number": "ORD-20250101-0001",
    "payment": {
      "payment_key": "toss_payment_key_here",
      "amount": 161000,
      "payment_method": "card"
    }
  }
}
```

---

### 6.2. 주문 목록 조회

**Endpoint:** `GET /orders`
**Auth:** Bearer Token

**Query Parameters:**
- `page`: 페이지 번호 (default: 1)
- `limit`: 페이지당 항목 수 (default: 10)
- `status`: 주문 상태 (pending, paid, preparing, shipping, delivered, confirmed, cancelled)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "order_number": "ORD-20250101-0001",
      "order_status": "shipping",
      "shipping_status": "in_transit",
      "items": [
        {
          "product_name": "오버핏 코튼 셔츠",
          "brand_name": "미니멀웍스",
          "size": "M",
          "color": "블랙",
          "quantity": 2,
          "price": 79000,
          "thumbnail_url": "https://cdn.essence-shop.com/products/1/thumb.jpg"
        }
      ],
      "final_price": 161000,
      "tracking_info": {
        "courier_company": "CJ대한통운",
        "tracking_number": "123456789012"
      },
      "created_at": "2025-01-01T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 5,
    "total_pages": 1
  }
}
```

---

### 6.3. 주문 상세 조회

**Endpoint:** `GET /orders/{id}`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": {
    "id": 1,
    "order_number": "ORD-20250101-0001",
    "order_status": "shipping",
    "shipping_status": "in_transit",
    "recipient": {
      "name": "홍길동",
      "phone": "010-1234-5678",
      "postal_code": "12345",
      "address_line1": "서울시 강남구",
      "address_line2": "101동 101호",
      "delivery_memo": "부재시 문앞에 놓아주세요"
    },
    "items": [
      {
        "id": 1,
        "product_name": "오버핏 코튼 셔츠",
        "brand_name": "미니멀웍스",
        "size": "M",
        "color": "블랙",
        "quantity": 2,
        "price": 79000,
        "subtotal": 158000,
        "thumbnail_url": "https://cdn.essence-shop.com/products/1/thumb.jpg"
      }
    ],
    "payment": {
      "total_product_price": 158000,
      "shipping_fee": 3000,
      "discount_amount": 0,
      "final_price": 161000,
      "payment_method": "card",
      "paid_at": "2025-01-01T10:05:00Z"
    },
    "tracking": {
      "courier_company": "CJ대한통운",
      "tracking_number": "123456789012",
      "shipped_at": "2025-01-01T15:00:00Z"
    },
    "created_at": "2025-01-01T10:00:00Z"
  }
}
```

---

### 6.4. 주문 취소

**Endpoint:** `POST /orders/{id}/cancel`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "cancel_reason": "단순 변심"
}
```

**Response (200):**
```json
{
  "message": "주문이 취소되었습니다.",
  "data": {
    "order_id": 1,
    "order_status": "cancelled",
    "refund_amount": 161000
  }
}
```

---

### 6.5. 구매 확정

**Endpoint:** `POST /orders/{id}/confirm`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "message": "구매가 확정되었습니다.",
  "data": {
    "order_id": 1,
    "order_status": "confirmed",
    "confirmed_at": "2025-01-10T10:00:00Z"
  }
}
```

---

## 찜하기 (Wishlists)

### 7.1. 찜 목록 조회

**Endpoint:** `GET /wishlists`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "오버핏 코튼 셔츠",
        "brand_name": "미니멀웍스",
        "price": 89000,
        "sale_price": 79000,
        "thumbnail_url": "https://cdn.essence-shop.com/products/1/thumb.jpg",
        "status": "active"
      },
      "created_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

---

### 7.2. 찜하기 추가

**Endpoint:** `POST /wishlists`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "product_id": 1
}
```

**Response (201):**
```json
{
  "message": "찜 목록에 추가되었습니다.",
  "data": {
    "id": 1,
    "product_id": 1
  }
}
```

---

### 7.3. 찜하기 삭제

**Endpoint:** `DELETE /wishlists/{id}`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "message": "찜 목록에서 삭제되었습니다."
}
```

---

## 리뷰 (Reviews)

### 8.1. 리뷰 목록 조회 (상품별)

**Endpoint:** `GET /products/{product_id}/reviews`

**Query Parameters:**
- `page`: 페이지 번호 (default: 1)
- `limit`: 페이지당 항목 수 (default: 10)
- `sort`: 정렬 (latest, rating_desc, rating_asc)
- `has_photo`: 사진 리뷰만 (true/false)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "user": {
        "name": "홍*동",
        "profile_image": null
      },
      "rating": 5,
      "content": "정말 마음에 들어요! 핏도 좋고 소재도 좋습니다.",
      "images": [
        {
          "id": 1,
          "url": "https://cdn.essence-shop.com/reviews/1/image1.jpg"
        }
      ],
      "user_info": {
        "height": 178,
        "weight": 68,
        "purchased_size": "L",
        "size_satisfaction": "perfect"
      },
      "created_at": "2025-01-05T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "total_pages": 5
  }
}
```

---

### 8.2. 리뷰 작성

**Endpoint:** `POST /reviews`
**Auth:** Bearer Token

**Request Body (multipart/form-data):**
```
order_item_id: 1
rating: 5
content: "정말 마음에 들어요!"
user_height: 178
user_weight: 68
purchased_size: "L"
size_satisfaction: "perfect"
images: [File, File]
```

**Response (201):**
```json
{
  "message": "리뷰가 작성되었습니다.",
  "data": {
    "id": 1,
    "rating": 5,
    "content": "정말 마음에 들어요!"
  }
}
```

---

### 8.3. 내 리뷰 목록 조회

**Endpoint:** `GET /reviews/my`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "오버핏 코튼 셔츠",
        "thumbnail_url": "https://cdn.essence-shop.com/products/1/thumb.jpg"
      },
      "rating": 5,
      "content": "정말 마음에 들어요!",
      "images": [
        {
          "url": "https://cdn.essence-shop.com/reviews/1/image1.jpg"
        }
      ],
      "created_at": "2025-01-05T10:00:00Z"
    }
  ]
}
```

---

### 8.4. 리뷰 수정

**Endpoint:** `PATCH /reviews/{id}`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "rating": 4,
  "content": "수정된 리뷰 내용"
}
```

**Response (200):**
```json
{
  "message": "리뷰가 수정되었습니다."
}
```

---

### 8.5. 리뷰 삭제

**Endpoint:** `DELETE /reviews/{id}`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "message": "리뷰가 삭제되었습니다."
}
```

---

## 교환/반품 (Returns)

### 9.1. 교환/반품 신청

**Endpoint:** `POST /returns`
**Auth:** Bearer Token

**Request Body (multipart/form-data):**
```
order_id: 1
return_type: "return"
reason: "사이즈 불만족"
detailed_reason: "생각보다 커요"
images: [File, File]
```

**Response (201):**
```json
{
  "message": "교환/반품 신청이 완료되었습니다.",
  "data": {
    "id": 1,
    "order_id": 1,
    "return_type": "return",
    "status": "requested"
  }
}
```

---

### 9.2. 교환/반품 목록 조회

**Endpoint:** `GET /returns`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "order": {
        "id": 1,
        "order_number": "ORD-20250101-0001"
      },
      "return_type": "return",
      "reason": "사이즈 불만족",
      "status": "approved",
      "created_at": "2025-01-07T10:00:00Z"
    }
  ]
}
```

---

### 9.3. 교환/반품 상세 조회

**Endpoint:** `GET /returns/{id}`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "data": {
    "id": 1,
    "order": {
      "id": 1,
      "order_number": "ORD-20250101-0001",
      "items": [
        {
          "product_name": "오버핏 코튼 셔츠",
          "brand_name": "미니멀웍스",
          "size": "M",
          "color": "블랙"
        }
      ]
    },
    "return_type": "return",
    "reason": "사이즈 불만족",
    "detailed_reason": "생각보다 커요",
    "images": [
      {
        "url": "https://cdn.essence-shop.com/returns/1/image1.jpg"
      }
    ],
    "status": "collecting",
    "tracking": {
      "courier_company": "CJ대한통운",
      "tracking_number": "987654321098"
    },
    "refund_amount": 161000,
    "created_at": "2025-01-07T10:00:00Z",
    "approved_at": "2025-01-07T15:00:00Z"
  }
}
```

---

## 쿠폰 (Coupons)

### 10.1. 내 쿠폰 목록 조회

**Endpoint:** `GET /coupons/my`
**Auth:** Bearer Token

**Query Parameters:**
- `status`: 쿠폰 상태 (available, used, expired)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "coupon": {
        "id": 1,
        "code": "WELCOME10",
        "name": "신규 회원 10% 할인",
        "discount_type": "percent",
        "discount_value": 10,
        "min_order_amount": 100000,
        "max_discount_amount": 50000
      },
      "is_used": false,
      "issued_at": "2025-01-01T00:00:00Z",
      "expires_at": "2025-12-31T23:59:59Z"
    }
  ]
}
```

---

### 10.2. 쿠폰 코드로 발급받기

**Endpoint:** `POST /coupons/apply`
**Auth:** Bearer Token

**Request Body:**
```json
{
  "coupon_code": "WELCOME10"
}
```

**Response (201):**
```json
{
  "message": "쿠폰이 발급되었습니다.",
  "data": {
    "id": 1,
    "coupon": {
      "name": "신규 회원 10% 할인",
      "discount_type": "percent",
      "discount_value": 10
    }
  }
}
```

---

## 알림 (Notifications)

### 11.1. 알림 목록 조회

**Endpoint:** `GET /notifications`
**Auth:** Bearer Token

**Query Parameters:**
- `page`: 페이지 번호 (default: 1)
- `limit`: 페이지당 항목 수 (default: 20)
- `is_read`: 읽음 여부 (true/false)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "type": "shipping",
      "title": "배송이 시작되었습니다",
      "content": "주문번호 ORD-20250101-0001 상품이 배송 시작되었습니다.",
      "link_url": "/orders/1",
      "is_read": false,
      "created_at": "2025-01-02T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 10,
    "total_pages": 1
  }
}
```

---

### 11.2. 알림 읽음 처리

**Endpoint:** `POST /notifications/{id}/read`
**Auth:** Bearer Token

**Response (200):**
```json
{
  "message": "알림을 읽었습니다."
}
```

---

## 어드민 API (Admin)

모든 어드민 API는 `role=admin` 사용자만 접근 가능합니다.

### 12.1. 대시보드

**Endpoint:** `GET /admin/dashboard`
**Auth:** Bearer Token (Admin)

**Response (200):**
```json
{
  "data": {
    "today": {
      "orders": 15,
      "revenue": 2350000
    },
    "this_month": {
      "orders": 450,
      "revenue": 67500000,
      "profit": 27000000
    },
    "pending_orders": 5,
    "low_stock_products": 8,
    "pending_returns": 3
  }
}
```

---

### 12.2. 상품 등록

**Endpoint:** `POST /admin/products`
**Auth:** Bearer Token (Admin)

**Request Body (multipart/form-data):**
```
brand_id: 1
name: "오버핏 코튼 셔츠"
category: "tops"
price: 89000
sale_price: 79000
description: "데일리로 입기 좋은 셔츠"
material: "코튼 100%"
country_of_origin: "대한민국"
care_instructions: "단독 세탁, 찬물 손세탁"
model_height: 178
model_weight: 68
model_size: "L"
shipping_fee: 3000
shipping_days: "2-3일"
images: [File, File, File]
options: [{"size": "M", "color": "블랙", "color_code": "#000000", "stock": 50}]
```

**Response (201):**
```json
{
  "message": "상품이 등록되었습니다.",
  "data": {
    "id": 1,
    "name": "오버핏 코튼 셔츠"
  }
}
```

---

### 12.3. 주문 목록 조회 (어드민)

**Endpoint:** `GET /admin/orders`
**Auth:** Bearer Token (Admin)

**Query Parameters:**
- `page`: 페이지 번호
- `limit`: 페이지당 항목 수
- `status`: 주문 상태
- `start_date`: 시작 날짜 (YYYY-MM-DD)
- `end_date`: 종료 날짜 (YYYY-MM-DD)
- `search`: 검색어 (주문번호, 주문자명, 전화번호)

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "order_number": "ORD-20250101-0001",
      "user": {
        "name": "홍길동",
        "phone": "010-1234-5678"
      },
      "items_summary": "오버핏 코튼 셔츠 외 1건",
      "final_price": 161000,
      "order_status": "paid",
      "created_at": "2025-01-01T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 450,
    "total_pages": 23
  }
}
```

---

### 12.4. 주문 상태 변경

**Endpoint:** `PATCH /admin/orders/{id}/status`
**Auth:** Bearer Token (Admin)

**Request Body:**
```json
{
  "order_status": "preparing"
}
```

**Response (200):**
```json
{
  "message": "주문 상태가 변경되었습니다."
}
```

---

### 12.5. 송장번호 입력

**Endpoint:** `POST /admin/orders/{id}/shipping`
**Auth:** Bearer Token (Admin)

**Request Body:**
```json
{
  "courier_company": "CJ대한통운",
  "tracking_number": "123456789012"
}
```

**Response (200):**
```json
{
  "message": "송장번호가 입력되었습니다.",
  "data": {
    "order_status": "shipping",
    "shipped_at": "2025-01-02T15:00:00Z"
  }
}
```

---

### 12.6. 재고 조정

**Endpoint:** `PATCH /admin/inventory/{id}`
**Auth:** Bearer Token (Admin)

**Request Body:**
```json
{
  "quantity": 100,
  "memo": "재입고"
}
```

**Response (200):**
```json
{
  "message": "재고가 조정되었습니다.",
  "data": {
    "id": 1,
    "product_option_id": 1,
    "quantity": 100
  }
}
```

---

### 12.7. 매출 통계

**Endpoint:** `GET /admin/stats/revenue`
**Auth:** Bearer Token (Admin)

**Query Parameters:**
- `start_date`: 시작 날짜 (YYYY-MM-DD)
- `end_date`: 종료 날짜 (YYYY-MM-DD)
- `group_by`: 그룹 기준 (day, week, month)

**Response (200):**
```json
{
  "data": {
    "total_revenue": 67500000,
    "total_orders": 450,
    "average_order_value": 150000,
    "chart_data": [
      {
        "date": "2025-01-01",
        "revenue": 2350000,
        "orders": 15
      },
      {
        "date": "2025-01-02",
        "revenue": 1800000,
        "orders": 12
      }
    ]
  }
}
```

---

### 12.8. 인기 상품 통계

**Endpoint:** `GET /admin/stats/popular-products`
**Auth:** Bearer Token (Admin)

**Query Parameters:**
- `start_date`: 시작 날짜
- `end_date`: 종료 날짜
- `limit`: Top N개 (default: 10)

**Response (200):**
```json
{
  "data": [
    {
      "product_id": 1,
      "product_name": "오버핏 코튼 셔츠",
      "brand_name": "미니멀웍스",
      "total_orders": 120,
      "total_quantity": 180,
      "total_revenue": 14220000
    }
  ]
}
```

---

## 에러 코드

| 코드 | HTTP Status | 설명 |
|------|-------------|------|
| VALIDATION_ERROR | 400 | 요청 데이터 검증 실패 |
| UNAUTHORIZED | 401 | 인증 실패 (토큰 없음 또는 만료) |
| FORBIDDEN | 403 | 권한 없음 |
| NOT_FOUND | 404 | 리소스를 찾을 수 없음 |
| ALREADY_EXISTS | 409 | 이미 존재함 (중복) |
| OUT_OF_STOCK | 400 | 재고 부족 |
| PAYMENT_FAILED | 400 | 결제 실패 |
| ORDER_CANNOT_CANCEL | 400 | 취소할 수 없는 주문 |
| INTERNAL_ERROR | 500 | 서버 내부 오류 |

**에러 응답 형식:**
```json
{
  "error": "ERROR_CODE",
  "message": "사용자에게 보여줄 에러 메시지",
  "details": {
    "field": "email",
    "reason": "이미 사용 중인 이메일입니다."
  }
}
```

---

## Rate Limiting

- **일반 API**: 분당 60회
- **어드민 API**: 분당 120회
- 초과 시 HTTP 429 (Too Many Requests) 응답

---

## Pagination

모든 목록 API는 다음과 같은 pagination 형식을 사용합니다:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

---

이 API 명세서는 개발 진행에 따라 업데이트될 수 있습니다.