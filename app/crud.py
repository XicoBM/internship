from typing import List

from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate

HTTP_400_BAD_REQUEST = 400
HTTP_422_UNPROCESSABLE_ENTITY = 422

def get_items(min_price: float = 0.0) -> List[Item]:
    return [Item(**item) for item in items_db if item["price"] >= min_price]


def create_item(item: ItemCreate) -> Item:
    if any(existing_item["name"] == item.name for existing_item in items_db):
        return HTTP_422_UNPROCESSABLE_ENTITY
    if item.price <= 0:
        return HTTP_422_UNPROCESSABLE_ENTITY
    new_id = max((item["id"] for item in items_db), default=1) + 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    return Item(**new_item)


def update_item_by_id(item_id: int, update: ItemUpdate) -> Item | None:
    for item in items_db:
        if item["id"] == item_id:
            if update.name:
                if any(existing_item["name"] == update.name for existing_item in items_db if existing_item["id"] != item_id) or len(update.name) < 3:
                    return HTTP_422_UNPROCESSABLE_ENTITY
                item["name"] = update.name
            if update.price:
                item["price"] = update.price
            return Item(**item)
    return HTTP_400_BAD_REQUEST
