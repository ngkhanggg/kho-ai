import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.ports import InMemoryInventoryRepository, InventoryRepositoryProtocol
from app.schema import InventoryItemResponse
from app.sessions import AccessSession, require_active_session

router = APIRouter (prefix="/api/v1/inventory", tags=["Inventory"])
_default_inventory_repo = InMemoryInventoryRepository()

def get_inventory_repo() -> InventoryRepositoryProtocol:
    return _default_inventory_repo
@router.get("", response_model=list[InventoryItemResponse])
def list_inventory(
    session: Annotated[AccessSession, Depends(require_active_session)],
    repo: Annotated[InventoryRepositoryProtocol, Depends(get_inventory_repo)]
) -> list[InventoryItemResponse]:
    items = repo.list_by_shop(session.shop_id)
    return[
        InventoryItemResponse(
            product_id=item.product_id,
            shop_id = item.shop_id,
            stock_quantity= item.stock_quantity,
            updated_at=item.updated_at
        )
        for item in items
    ]

@router.get("/{product_id}", response_model=InventoryItemResponse)
def get_product_inventory(
        product_id: uuid.UUID,
    session: Annotated[AccessSession, Depends(require_active_session)],
    repo: Annotated[InventoryRepositoryProtocol, Depends(get_inventory_repo)],
) -> InventoryItemResponse:
    item = repo.get_by_product(session.shop_id, product_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product inventory not found.",
        )
    return InventoryItemResponse(
        product_id=item.product_id,
        shop_id=item.shop_id,
        stock_quantity=item.stock_quantity,
        updated_at=item.updated_at,
    
)
