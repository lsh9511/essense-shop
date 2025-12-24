# 개발 타임라인 (Development Timeline)
# ESSENCE - 편집샵

> **참고**: 이 타임라인은 하루 3-4시간 작업 기준입니다. 수동으로 코딩하면서 각 메서드와 코드를 이해하며 진행하는 학습 중심 일정입니다.

## 전체 개요

| Phase | 기간 | 주요 목표 | 예상 시간 |
|-------|------|---------|---------|
| **MVP** | 5주 | 기본 이커머스 기능 구현 | 70-100시간 |
| **Phase 2** | 4주 | 고객 경험 개선 | 56-80시간 |
| **Phase 3** | 4주 | 마케팅 및 분석 | 56-80시간 |
| **Phase 4** | 3주 | 운영 판단 시스템 | 42-60시간 |
| **총 기간** | **16주** | **약 4개월** | **224-320시간** |

---

## MVP (Week 1-5): 핵심 이커머스 기능

### Week 1: 프로젝트 초기 설정 및 인증 시스템

#### Day 1-2: 프로젝트 초기 설정 (6-8시간)

**작업 내용**:
```bash
# 프로젝트 디렉토리 생성
mkdir essence-backend
cd essence-backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# 필수 패키지 설치
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv pydantic[email] redis
```

**디렉토리 구조**:
```
essence-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 앱 진입점
│   ├── config.py        # 환경 변수 설정
│   ├── database.py      # DB 연결 설정
│   ├── models/          # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/         # Pydantic 스키마
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/          # API 라우트
│   │   ├── __init__.py
│   │   └── auth.py
│   └── utils/           # 유틸리티 함수
│       ├── __init__.py
│       ├── auth.py      # JWT 토큰 관련
│       └── dependencies.py  # 의존성 주입
├── .env
├── requirements.txt
└── README.md
```

**학습 포인트**:
- FastAPI 프로젝트 구조 이해
- 왜 모델, 스키마, 라우트를 분리하는가?
- `__init__.py`의 역할

**체크포인트**:
- [ ] `uvicorn app.main:app --reload` 실행 성공
- [ ] http://localhost:8000/docs 에서 Swagger UI 확인
- [ ] PostgreSQL 연결 확인

---

#### Day 3-5: 사용자 인증 구현 (10-12시간)

**models/user.py 작성**:
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # 소셜 로그인 시 NULL
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**학습 포인트**:
- `Column`: 테이블 컬럼 정의. `Integer`, `String`, `Boolean` 등 타입 지정
- `primary_key=True`: 기본 키 설정
- `unique=True`: 중복 불가 제약 (이메일은 고유해야 함)
- `nullable=False`: NOT NULL 제약
- `index=True`: 검색 성능 향상을 위한 인덱스 생성
- `server_default=func.now()`: DB에서 자동으로 현재 시간 입력
- `enum.Enum`: 고정된 값만 허용 (customer, admin)

**schemas/user.py 작성**:
```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., max_length=50)
    phone: str
    marketing_agree: bool = False

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 모델을 Pydantic 모델로 변환
```

**학습 포인트**:
- `BaseModel`: Pydantic 스키마의 기본 클래스
- `EmailStr`: 이메일 형식 자동 검증
- `Field`: 추가 검증 (min_length, max_length)
- `...`: 필수 필드
- `Config.from_attributes`: ORM 객체를 dict로 변환

**utils/auth.py 작성**:
```python
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호를 bcrypt로 해싱"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """JWT Access Token 생성"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

**학습 포인트**:
- `passlib`: 비밀번호 해싱 라이브러리
- `bcrypt`: 단방향 해싱 알고리즘 (복호화 불가)
- `jwt.encode()`: JWT 토큰 생성
- `exp`: 만료 시간 (expiration)
- 왜 plain text로 저장하지 않는가? → 보안

**routes/auth.py 작성**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegister, UserResponse
from app.models.user import User
from app.utils.auth import hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """회원가입"""
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다."
        )

    # 비밀번호 해싱
    hashed_pw = hash_password(user_data.password)

    # 사용자 생성
    new_user = User(
        email=user_data.email,
        password_hash=hashed_pw,
        name=user_data.name,
        phone=user_data.phone,
        marketing_agree=user_data.marketing_agree
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
```

**학습 포인트**:
- `APIRouter`: 라우트 그룹화
- `Depends(get_db)`: 의존성 주입으로 DB 세션 가져오기
- `db.query(User).filter()`: SQL의 SELECT * FROM users WHERE ...
- `.first()`: 첫 번째 결과 반환 (없으면 None)
- `db.add()`: INSERT 준비
- `db.commit()`: 실제 DB에 저장
- `db.refresh()`: DB에서 생성된 ID 등을 다시 가져옴
- `HTTPException`: HTTP 에러 응답

**체크포인트**:
- [ ] 회원가입 API 호출 성공
- [ ] 이메일 중복 시 에러 반환
- [ ] 비밀번호가 bcrypt로 해싱되어 저장되는지 확인

---

#### Day 6-7: 로그인 및 토큰 검증 (6-8시간)

**로그인 API 추가**:
```python
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """로그인"""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 일치하지 않습니다."
        )

    # Access Token 생성
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }
```

**의존성 주입 (utils/dependencies.py)**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.config import settings

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """토큰에서 현재 사용자 가져오기"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
```

**학습 포인트**:
- `HTTPBearer`: Authorization: Bearer <token> 헤더 파싱
- `jwt.decode()`: 토큰 검증 및 payload 추출
- `payload.get("sub")`: subject (사용자 ID)
- 왜 의존성 주입을 사용하는가? → 코드 재사용, 테스트 용이

**체크포인트**:
- [ ] 로그인 성공 시 토큰 발급
- [ ] 잘못된 비밀번호로 로그인 시 401 에러
- [ ] 토큰을 헤더에 포함해서 `/users/me` API 호출 성공

---

### Week 2: 브랜드 및 상품 관리

#### Day 1-2: 브랜드 CRUD (6-8시간)

**models/brand.py 작성**:
```python
from sqlalchemy import Column, Integer, String, Text, Decimal, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    name_en = Column(String(100))
    logo_url = Column(String(500))
    description = Column(Text)
    story = Column(Text)
    instagram = Column(String(255))
    website = Column(String(255))
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**브랜드 CRUD API 구현**:
- 브랜드 목록 조회: `GET /brands`
- 브랜드 상세 조회: `GET /brands/{id}`
- 브랜드 등록 (어드민): `POST /admin/brands`

**학습 포인트**:
- 페이지네이션 구현 (`skip`, `limit`)
- 관계형 데이터 (Brand ↔ Product)

---

#### Day 3-7: 상품 관리 (14-16시간)

**models/product.py 작성**:
```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class ProductCategory(str, enum.Enum):
    TOPS = "tops"
    BOTTOMS = "bottoms"
    OUTERWEAR = "outerwear"
    SHOES = "shoes"
    ACCESSORIES = "accessories"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    price = Column(Integer, nullable=False)
    sale_price = Column(Integer)
    description = Column(Text)
    status = Column(String(20), nullable=False, default="active")

    # 관계 정의
    brand = relationship("Brand", backref="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    options = relationship("ProductOption", back_populates="product", cascade="all, delete-orphan")
```

**학습 포인트**:
- `ForeignKey`: 외래 키 (Brand와 연결)
- `relationship`: ORM 레벨에서 관계 정의
- `backref`: 역참조 (brand.products로 접근 가능)
- `cascade`: 상품 삭제 시 이미지도 함께 삭제

**상품 옵션 (models/product_option.py)**:
```python
class ProductOption(Base):
    __tablename__ = "product_options"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    size = Column(String(20), nullable=False)
    color = Column(String(50), nullable=False)
    color_code = Column(String(7))
    additional_price = Column(Integer, nullable=False, default=0)

    product = relationship("Product", back_populates="options")
    inventory = relationship("Inventory", uselist=False, back_populates="product_option")
```

**상품 등록 API 구현**:
```python
@router.post("/admin/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)  # 어드민만 접근
):
    """상품 등록 (어드민)"""
    new_product = Product(
        brand_id=product_data.brand_id,
        name=product_data.name,
        category=product_data.category,
        price=product_data.price,
        sale_price=product_data.sale_price,
        description=product_data.description
    )

    db.add(new_product)
    db.flush()  # ID 생성 (아직 커밋 전)

    # 옵션 추가
    for option_data in product_data.options:
        option = ProductOption(
            product_id=new_product.id,
            size=option_data.size,
            color=option_data.color,
            color_code=option_data.color_code
        )
        db.add(option)

        # 재고 초기화
        inventory = Inventory(
            product_option_id=option.id,
            quantity=option_data.stock
        )
        db.add(inventory)

    db.commit()
    db.refresh(new_product)

    return new_product
```

**학습 포인트**:
- `db.flush()`: 커밋 없이 ID만 생성 (트랜잭션 내에서 ID 필요할 때)
- 중첩된 데이터 생성 (Product → Options → Inventory)
- 트랜잭션의 원자성 (하나라도 실패하면 전체 롤백)

**체크포인트**:
- [ ] 브랜드 등록 및 조회
- [ ] 상품 등록 (옵션 포함)
- [ ] 상품 목록 조회 (필터링, 정렬)
- [ ] 상품 상세 조회 (옵션, 이미지 포함)

---

### Week 3: 장바구니 및 주문 시스템

#### Day 1-3: 장바구니 구현 (10-12시간)

**models/cart.py**:
```python
class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", backref="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_option_id = Column(Integer, ForeignKey("product_options.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
    product_option = relationship("ProductOption")
```

**장바구니 추가 API**:
```python
@router.post("/cart/items")
def add_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """장바구니에 상품 추가"""
    # 장바구니가 없으면 생성
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.flush()

    # 재고 확인
    inventory = db.query(Inventory).filter(
        Inventory.product_option_id == item_data.product_option_id
    ).first()

    if inventory.quantity < item_data.quantity:
        raise HTTPException(status_code=400, detail="재고가 부족합니다.")

    # 이미 담긴 상품이면 수량 증가
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_option_id == item_data.product_option_id
    ).first()

    if existing_item:
        existing_item.quantity += item_data.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_option_id=item_data.product_option_id,
            quantity=item_data.quantity
        )
        db.add(new_item)

    db.commit()

    return {"message": "장바구니에 추가되었습니다."}
```

**학습 포인트**:
- 중복 체크 후 수량 증가 vs 새로 추가
- 재고 확인의 중요성
- 트랜잭션 안전성

---

#### Day 4-7: 주문 시스템 (14-16시간)

**models/order.py**:
```python
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_name = Column(String(50), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    postal_code = Column(String(10), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    total_product_price = Column(Integer, nullable=False)
    shipping_fee = Column(Integer, nullable=False, default=3000)
    discount_amount = Column(Integer, nullable=False, default=0)
    final_price = Column(Integer, nullable=False)
    order_status = Column(String(20), nullable=False, default="pending")

    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", uselist=False, back_populates="order")
```

**주문 생성 API**:
```python
@router.post("/orders")
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """주문 생성"""
    # 주문 번호 생성
    from datetime import datetime
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{generate_seq():04d}"

    # 총 금액 계산
    total_price = 0
    order_items = []

    for item_data in order_data.items:
        option = db.query(ProductOption).filter(
            ProductOption.id == item_data.product_option_id
        ).first()

        if not option:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

        product = option.product

        # 재고 확인
        inventory = db.query(Inventory).filter(
            Inventory.product_option_id == option.id
        ).first()

        if inventory.quantity < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"{product.name} 재고가 부족합니다.")

        # 가격 계산
        price = product.sale_price if product.sale_price else product.price
        subtotal = price * item_data.quantity
        total_price += subtotal

        order_items.append({
            "product_option_id": option.id,
            "product_name": product.name,
            "brand_name": product.brand.name,
            "size": option.size,
            "color": option.color,
            "price": price,
            "quantity": item_data.quantity,
            "subtotal": subtotal
        })

    # 주문 생성
    new_order = Order(
        order_number=order_number,
        user_id=current_user.id,
        recipient_name=order_data.recipient_name,
        recipient_phone=order_data.recipient_phone,
        postal_code=order_data.postal_code,
        address_line1=order_data.address_line1,
        address_line2=order_data.address_line2,
        delivery_memo=order_data.delivery_memo,
        total_product_price=total_price,
        shipping_fee=3000,
        final_price=total_price + 3000
    )

    db.add(new_order)
    db.flush()

    # 주문 상품 추가
    for item in order_items:
        order_item = OrderItem(
            order_id=new_order.id,
            **item
        )
        db.add(order_item)

        # 재고 차감 (트리거 대신 직접 처리)
        inventory = db.query(Inventory).filter(
            Inventory.product_option_id == item["product_option_id"]
        ).first()
        inventory.quantity -= item["quantity"]

    db.commit()
    db.refresh(new_order)

    return new_order
```

**학습 포인트**:
- 주문 생성의 복잡성 (재고 확인, 가격 계산, 재고 차감)
- 트랜잭션의 중요성 (하나라도 실패하면 롤백)
- 스냅샷 저장 (주문 시점의 상품명, 가격 저장)

**체크포인트**:
- [ ] 장바구니 담기, 수정, 삭제
- [ ] 주문 생성 (재고 차감 확인)
- [ ] 재고 부족 시 주문 실패
- [ ] 주문 목록 조회

---

### Week 4: 결제 연동 및 주문 관리

#### Day 1-3: Toss Payments 연동 (10-12시간)

**결제 API 연동**:
```bash
pip install requests
```

**utils/payment.py**:
```python
import requests
from app.config import settings

def confirm_payment(payment_key: str, order_id: str, amount: int):
    """Toss Payments 결제 승인"""
    url = "https://api.tosspayments.com/v1/payments/confirm"

    headers = {
        "Authorization": f"Basic {settings.TOSS_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "paymentKey": payment_key,
        "orderId": order_id,
        "amount": amount
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise Exception("결제 승인 실패")

    return response.json()
```

**결제 승인 API**:
```python
@router.post("/payments/confirm")
def confirm_payment_endpoint(
    payment_data: PaymentConfirm,
    db: Session = Depends(get_db)
):
    """결제 승인"""
    # 주문 조회
    order = db.query(Order).filter(Order.id == payment_data.order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")

    # Toss Payments 결제 승인 요청
    try:
        result = confirm_payment(
            payment_key=payment_data.payment_key,
            order_id=order.order_number,
            amount=order.final_price
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 결제 정보 저장
    payment = Payment(
        order_id=order.id,
        payment_key=payment_data.payment_key,
        payment_method=result.get("method"),
        amount=result.get("totalAmount"),
        status="completed",
        paid_at=datetime.now()
    )
    db.add(payment)

    # 주문 상태 변경
    order.order_status = "paid"

    db.commit()

    return {"message": "결제가 완료되었습니다."}
```

**학습 포인트**:
- 외부 API 호출 (`requests.post`)
- 결제 승인의 2단계 프로세스 (결제 → 승인)
- 에러 처리의 중요성

---

#### Day 4-7: 어드민 주문 관리 (14-16시간)

**주문 목록 조회 (어드민)**:
```python
@router.get("/admin/orders")
def get_orders_admin(
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """주문 목록 조회 (어드민)"""
    query = db.query(Order)

    # 필터링
    if status:
        query = query.filter(Order.order_status == status)

    if search:
        query = query.filter(
            or_(
                Order.order_number.contains(search),
                Order.recipient_name.contains(search),
                Order.recipient_phone.contains(search)
            )
        )

    # 정렬
    query = query.order_by(Order.created_at.desc())

    # 페이지네이션
    skip = (page - 1) * limit
    total = query.count()
    orders = query.offset(skip).limit(limit).all()

    return {
        "data": orders,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    }
```

**송장번호 입력 API**:
```python
@router.post("/admin/orders/{order_id}/shipping")
def add_tracking_number(
    order_id: int,
    tracking_data: TrackingNumberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """송장번호 입력"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")

    order.courier_company = tracking_data.courier_company
    order.tracking_number = tracking_data.tracking_number
    order.order_status = "shipping"
    order.shipping_status = "shipped"
    order.shipped_at = datetime.now()

    db.commit()

    # 고객에게 배송 시작 알림 발송 (TODO: 이메일/SMS)

    return {"message": "송장번호가 입력되었습니다."}
```

**체크포인트**:
- [ ] Toss Payments 결제 테스트 (테스트 키 사용)
- [ ] 결제 승인 성공
- [ ] 어드민에서 주문 목록 조회
- [ ] 송장번호 입력 및 상태 변경

---

### Week 5: 재고 관리 및 MVP 마무리

#### Day 1-3: 재고 관리 (10-12시간)

**재고 현황 조회**:
```python
@router.get("/admin/inventory")
def get_inventory_list(
    page: int = 1,
    limit: int = 50,
    low_stock: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """재고 현황 조회"""
    query = db.query(Inventory).join(ProductOption).join(Product)

    if low_stock:
        query = query.filter(Inventory.quantity <= Inventory.safe_stock)

    skip = (page - 1) * limit
    total = query.count()
    inventory_list = query.offset(skip).limit(limit).all()

    return {
        "data": [
            {
                "id": inv.id,
                "product_name": inv.product_option.product.name,
                "brand_name": inv.product_option.product.brand.name,
                "size": inv.product_option.size,
                "color": inv.product_option.color,
                "quantity": inv.quantity,
                "safe_stock": inv.safe_stock,
                "status": "부족" if inv.quantity <= inv.safe_stock else "정상"
            }
            for inv in inventory_list
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    }
```

**재고 조정 API**:
```python
@router.patch("/admin/inventory/{inventory_id}")
def adjust_inventory(
    inventory_id: int,
    adjust_data: InventoryAdjust,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """재고 조정"""
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="재고를 찾을 수 없습니다.")

    inventory.quantity = adjust_data.quantity
    inventory.updated_at = datetime.now()

    db.commit()

    return {"message": "재고가 조정되었습니다."}
```

---

#### Day 4-7: 테스트 및 버그 수정 (14-16시간)

**테스트 시나리오**:
1. 회원가입 → 로그인
2. 브랜드 및 상품 등록 (어드민)
3. 상품 목록 조회
4. 장바구니 담기
5. 주문 생성
6. 결제 (Toss Payments 테스트 키)
7. 어드민에서 주문 확인 및 송장 입력
8. 재고 확인

**체크포인트**:
- [ ] 모든 MVP 기능 동작 확인
- [ ] 에러 처리 완료
- [ ] 로그 추가 (디버깅용)

---

## Phase 2 (Week 6-9): 고객 경험 개선

### Week 6: 찜하기, 리뷰 시스템

**찜하기 구현** (Day 1-2):
- models/wishlist.py 작성
- 찜하기 CRUD API

**리뷰 시스템** (Day 3-7):
- models/review.py 작성
- 이미지 업로드 (S3 or 로컬)
- 리뷰 작성/수정/삭제 API
- 상품 상세에서 리뷰 목록 조회

---

### Week 7: 브랜드 페이지, 검색/필터

**브랜드 페이지** (Day 1-3):
- 브랜드 상세 페이지 API
- 브랜드별 상품 목록

**검색/필터** (Day 4-7):
- 전체 검색 (상품명, 브랜드명)
- 필터링 (카테고리, 가격대, 색상, 사이즈)
- 정렬 (최신순, 인기순, 가격순)

---

### Week 8: 배송지 관리, 알림

**배송지 관리** (Day 1-3):
- models/address.py
- 배송지 CRUD API
- 기본 배송지 설정

**알림 시스템** (Day 4-7):
- models/notification.py
- 주문/배송 알림 생성
- 알림 목록 조회 API

---

### Week 9: 프론트엔드 연동

**React 프로젝트 초기화** (Day 1-2):
```bash
npm create vite@latest essence-frontend -- --template react-ts
cd essence-frontend
npm install
npm install axios react-router-dom @tanstack/react-query tailwindcss
```

**기본 페이지 구현** (Day 3-7):
- 로그인/회원가입 페이지
- 상품 목록 페이지
- 상품 상세 페이지
- 장바구니 페이지
- 주문하기 페이지

---

## Phase 3 (Week 10-13): 마케팅 및 분석

### Week 10: 쿠폰 시스템

**쿠폰 구현** (Day 1-5):
- models/coupon.py, user_coupons.py
- 쿠폰 생성/발급 API (어드민)
- 쿠폰 적용 로직
- 주문 시 쿠폰 할인

---

### Week 11: 교환/반품 관리

**교환/반품 구현** (Day 1-7):
- models/return.py
- 교환/반품 신청 API
- 어드민에서 승인/거부
- 환불 처리 (Toss Payments 환불 API)

---

### Week 12: 통계 대시보드

**통계 API 구현** (Day 1-7):
- 매출 통계 (일/주/월별)
- 인기 상품 Top 10
- 고객 구매 패턴 분석
- 차트 데이터 생성

---

### Week 13: 최종 테스트 및 배포

**통합 테스트** (Day 1-3):
- 전체 시나리오 테스트
- 부하 테스트 (locust)

**배포** (Day 4-7):
- Docker 컨테이너화
- AWS/GCP 배포
- 도메인 연결
- HTTPS 설정

---

## Phase 4 (Week 14-16): 운영 판단 시스템

> 상세 문서: `docs/OPERATIONS_SYSTEM.md` 참고

### Week 14: 데이터 모델 및 상품 입력 자동화

#### Day 1-2: 데이터 모델 설계 (6-8시간)

**소싱 판단 테이블 생성**:
```python
# models/sourcing_decision.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from app.db.base import Base

class SourcingDecision(Base):
    __tablename__ = "sourcing_decisions"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    decision_type = Column(String(20))  # 직매입/위탁
    purchase_score = Column(Integer)  # 0-100
    estimated_monthly_sales = Column(Integer)
    margin_rate = Column(Numeric(5, 2))
    inventory_turnover_days = Column(Integer)
    return_rate = Column(Numeric(5, 2))
    decision_date = Column(DateTime, server_default=func.now())
    notes = Column(Text)
```

**Alembic 마이그레이션**:
```bash
alembic revision --autogenerate -m "Add sourcing_decisions table"
alembic upgrade head
```

---

#### Day 3-5: 상품 일괄 등록 기능 (10-12시간)

**CSV 파서 구현**:
```python
# utils/csv_parser.py
import pandas as pd

def parse_product_csv(file_path: str) -> list[dict]:
    """CSV 파일을 파싱하여 상품 데이터 리스트 반환"""
    df = pd.read_csv(file_path)

    # 필수 컬럼 검증
    required_cols = ['브랜드명', '상품명', '원가', '판매가', 'SKU']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"필수 컬럼 누락: {col}")

    # dict 리스트로 변환
    products = df.to_dict('records')
    return products
```

**일괄 등록 API**:
```python
# api/v1/endpoints/admin/products.py
@router.post("/bulk-import")
async def bulk_import_products(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """상품 일괄 등록"""
    # CSV 파일 저장
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 파싱 및 등록
    products = parse_product_csv(file_path)
    success = 0
    errors = []

    for idx, product_data in enumerate(products):
        try:
            # 중복 체크
            existing = db.query(Product).filter(
                Product.sku == product_data['SKU']
            ).first()

            if existing:
                errors.append({"row": idx+1, "reason": "중복 SKU"})
                continue

            # 상품 생성
            product = Product(**product_data)
            db.add(product)
            success += 1

        except Exception as e:
            errors.append({"row": idx+1, "reason": str(e)})

    db.commit()

    return {
        "total": len(products),
        "imported": success,
        "failed": len(errors),
        "errors": errors
    }
```

---

#### Day 6-7: 테스트 및 UI (6-8시간)

**테스트**:
- 100개 상품 테스트 데이터 업로드
- 에러 핸들링 개선

**어드민 UI**:
- 파일 업로드 폼
- 진행 상태 표시
- 결과 리포트 표시

---

### Week 15: 소싱 판단 알고리즘

#### Day 1-3: 판단 알고리즘 구현 (10-12시간)

**점수 계산 서비스**:
```python
# services/sourcing_service.py
class SourcingService:
    def calculate_purchase_score(self, product_data: dict) -> int:
        """직매입 점수 계산 (0-100)"""
        score = 0

        # 예상 판매량 (30점)
        if product_data['estimated_monthly_sales'] >= 10:
            score += 30
        elif product_data['estimated_monthly_sales'] >= 5:
            score += 15

        # 마진율 (25점)
        margin_rate = product_data['margin_rate']
        if margin_rate >= 0.45:
            score += 25
        elif margin_rate >= 0.35:
            score += 15

        # 재고 회전율 (20점)
        if product_data['inventory_turnover_days'] <= 30:
            score += 20
        elif product_data['inventory_turnover_days'] <= 60:
            score += 10

        # 반품률 (15점)
        if product_data['return_rate'] <= 0.05:
            score += 15
        elif product_data['return_rate'] <= 0.10:
            score += 7

        # 브랜드 신뢰도 (10점)
        if product_data.get('brand_verified'):
            score += 10

        return score

    def get_recommendation(self, score: int) -> dict:
        """추천 결과 생성"""
        if score >= 70:
            return {
                "decision": "직매입 추천",
                "level": "high",
                "color": "green"
            }
        elif score >= 30:
            return {
                "decision": "신중 검토",
                "level": "medium",
                "color": "yellow"
            }
        else:
            return {
                "decision": "위탁 추천",
                "level": "low",
                "color": "red"
            }
```

---

#### Day 4-7: API 및 UI (10-12시간)

**소싱 분석 API**:
```python
@router.post("/sourcing/analyze")
def analyze_sourcing(
    request: SourcingAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """소싱 방식 판단"""
    service = SourcingService()

    score = service.calculate_purchase_score(request.dict())
    recommendation = service.get_recommendation(score)

    # 판단 기록 저장
    decision = SourcingDecision(
        product_id=request.product_id,
        decision_type=recommendation['decision'],
        purchase_score=score,
        **request.dict()
    )
    db.add(decision)
    db.commit()

    return {
        "purchase_score": score,
        "recommendation": recommendation['decision'],
        "reasons": service.get_reasons(request.dict(), score),
        "estimated_profit": service.calculate_profit(request.dict())
    }
```

---

### Week 16: 운영 리포트

#### Day 1-3: 리포트 생성 엔진 (10-12시간)

**수익성 분석 리포트**:
```python
# services/report_service.py
class ReportService:
    def generate_profitability_report(
        self,
        start_date: date,
        end_date: date,
        db: Session
    ) -> dict:
        """수익성 분석 리포트"""

        # 기간 내 판매 데이터
        orders = db.query(Order).filter(
            Order.created_at >= start_date,
            Order.created_at <= end_date
        ).all()

        # 상품별 집계
        product_stats = {}
        for order in orders:
            for item in order.order_items:
                if item.product_id not in product_stats:
                    product_stats[item.product_id] = {
                        'sales': 0,
                        'revenue': 0,
                        'profit': 0,
                        'quantity': 0
                    }

                stats = product_stats[item.product_id]
                stats['quantity'] += item.quantity
                stats['revenue'] += item.price * item.quantity
                stats['profit'] += (item.price - item.product.cost) * item.quantity

        return {
            'period': {'start': start_date, 'end': end_date},
            'total_revenue': sum(s['revenue'] for s in product_stats.values()),
            'total_profit': sum(s['profit'] for s in product_stats.values()),
            'products': product_stats
        }
```

---

#### Day 4-7: PDF/Excel 출력 및 대시보드 (10-12시간)

**PDF 생성**:
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_to_pdf(report_data: dict, output_path: str):
    """리포트를 PDF로 출력"""
    c = canvas.Canvas(output_path, pagesize=A4)
    c.drawString(100, 800, f"수익성 분석 리포트")
    c.drawString(100, 780, f"기간: {report_data['period']['start']} ~ {report_data['period']['end']}")
    # ... 리포트 내용 작성
    c.save()
```

**대시보드 통합**:
- 리포트 목록 조회
- 자동 리포트 스케줄링 (Celery)
- 다운로드 링크 생성

---

## 주요 학습 포인트 요약

### Backend 핵심 개념
1. **SQLAlchemy ORM**: 테이블 정의, 관계 설정, 쿼리
2. **Pydantic**: 데이터 검증 및 직렬화
3. **JWT 인증**: 토큰 생성, 검증, 의존성 주입
4. **트랜잭션**: commit, rollback, flush
5. **외부 API 연동**: Toss Payments, S3

### 개발 패턴
1. **레이어 분리**: Models, Schemas, Routes
2. **의존성 주입**: Depends()
3. **에러 처리**: HTTPException
4. **페이지네이션**: skip, limit
5. **필터링 및 정렬**: filter(), order_by()

---

## 다음 단계

Week 1 Day 1-2의 "프로젝트 초기 설정"부터 시작하세요!
질문이 있을 때마다 물어보시면, 각 메서드와 코드의 의미를 자세히 설명드리겠습니다.