from datetime import datetime, timedelta, timezone
import uuid

import pytest
from fastapi.testclient import TestClient

from app.inventory_router import get_inventory_repo
from app.main import app
from app.ports import InMemoryInventoryRepository
from app.sessions import AccessSession, require_active_session


@pytest.fixture
def inventory_ctx():
    repo = InMemoryInventoryRepository()
    shop_id = uuid.uuid4()
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()
    repo.seed_product(shop_id=shop_id, product_id=product_id, stock_quantity=10)

    session = AccessSession(
        sub=user_id,
        shop_id=shop_id,
        email="owner@khoai.vn",
        jti=uuid.uuid4(),
        exp=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    app.dependency_overrides[get_inventory_repo] = lambda: repo
    app.dependency_overrides[require_active_session] = lambda: session

    with TestClient(app) as client:
        yield client, repo, shop_id, product_id

    app.dependency_overrides.clear()


def test_list_inventory_returns_only_current_shop_items(inventory_ctx):
    client, repo, _, product_id = inventory_ctx
    repo.seed_product(shop_id=uuid.uuid4(), product_id=uuid.uuid4(), stock_quantity=50)

    res = client.get("/api/v1/inventory")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["product_id"] == str(product_id)
    assert items[0]["stock_quantity"] == 10


def test_get_product_inventory_returns_item_or_404(inventory_ctx):
    client, repo, _, product_id = inventory_ctx
    other_shop_product = uuid.uuid4()
    repo.seed_product(shop_id=uuid.uuid4(), product_id=other_shop_product, stock_quantity=25)

    ok_res = client.get(f"/api/v1/inventory/{product_id}")
    assert ok_res.status_code == 200
    assert ok_res.json()["stock_quantity"] == 10

    not_found_res = client.get(f"/api/v1/inventory/{other_shop_product}")
    assert not_found_res.status_code == 404


def test_seed_rejects_negative_stock():
    repo = InMemoryInventoryRepository()
    with pytest.raises(ValueError, match="negative"):
        repo.seed_product(shop_id=uuid.uuid4(), product_id=uuid.uuid4(), stock_quantity=-1)