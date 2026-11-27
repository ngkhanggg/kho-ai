import uuid
from datetime import datetime, timezone
from typing import Protocol
from pydantic import BaseModel
from typing import Literal
class UserRecord(BaseModel):
    user_id: uuid.UUID
    shop_id: uuid.UUID
    full_name: str
    email: str
    password_hash: str
    created_at: datetime
    last_login_at: datetime | None = None

class UserRepositoryProtocol(Protocol):
    def get_by_email(self, email: str) -> UserRecord | None: ...
    def create_user_with_shop(
        self, full_name: str, shop_name: str, email: str, password_hash: str
    ) -> UserRecord: ...

class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users_by_email: dict[str, UserRecord] = {}

    def get_by_email(self, email: str) -> UserRecord | None:
        return self._users_by_email.get(email.strip().lower())

    def create_user_with_shop(
        self, full_name: str, shop_name: str, email: str, password_hash: str
    ) -> UserRecord:
        normalized = email.strip().lower()
        if normalized in self._users_by_email:
            raise ValueError("Duplicate email")
        record = UserRecord(
            user_id=uuid.uuid4(),
            shop_id=uuid.uuid4(),
            full_name=full_name.strip(),
            email=normalized,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc),
            last_login_at=None,
        )
        self._users_by_email[normalized] = record
        return record
class InventoryRecord(BaseModel):
        product_id: uuid.UUID
        shop_id: uuid.UUID
        stock_quantity: int
        updated_at: datetime
    
class InventoryAdjustmentRecord(BaseModel):
    adjustment_id:uuid.UUID
    product_id: uuid.UUID
    shop_id: uuid.UUID
    user_id: uuid.UUID
    adjustment_type: Literal["increase", "decrease", "set"]
    previous_quantity: int
    quantity_change: int
    new_quantity: int
    reason: str
    created_at: datetime

class InventoryRepositoryProtocol(Protocol):
    def list_by_shop(self, shop_id: uuid.UUID) -> list[InventoryRecord]: ...
    def get_by_product(self,shop_id:uuid.UUID,  product_id: uuid.UUID) -> InventoryRecord | None: ...
    def adjust_stock(
            self,
            shop_id: uuid.UUID,
            product_id: uuid.UUID,
            user_id: uuid.UUID,
            adjustment_type: Literal["increase", "decrease","set"],
            quantity: int,
            reason: str
    ) -> InventoryAdjustmentRecord: ...
    def list_adjustments(
        self, shop_id: uuid.UUID, product_id: uuid.UUID
    ) -> list[InventoryAdjustmentRecord] | None: ...

class InMemoryInventoryRepository:
    def __init__(self) -> None:
        self._items: dict[tuple[uuid.UUID, uuid.UUID],InventoryRecord] = {}
        self._adjustments: dict[tuple[uuid.UUID, uuid.UUID], list[InventoryAdjustmentRecord]] = {}

    def seed_product(self, shop_id: uuid.UUID, product_id: uuid.UUID, stock_quantity: int=0) -> InventoryRecord:
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        now = datetime.now(timezone.utc)
        record = InventoryRecord(
            product_id=product_id,
            shop_id=shop_id,
            stock_quantity=stock_quantity,
            updated_at=now
        )
        self._items[(shop_id, product_id)] = record
        self._adjustments.setdefault((shop_id,product_id), [])
        return record
    def list_by_shop(self,shop_id: uuid.UUID) -> list[InventoryRecord]:
        return[
            item for (item_shop_id, _), item in self._items.items()
            if item_shop_id == shop_id
        ]
    def get_by_product(self,shop_id:uuid.UUID, product_id:uuid.UUID) -> InventoryRecord | None:
        return self._items.get((shop_id, product_id))
