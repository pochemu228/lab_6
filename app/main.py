from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from dependencies import verify_token_query  # используем вариант с query


app = FastAPI(title="Laba #6", description="Token authentication demo")


router = APIRouter(
    prefix="/api",
    tags=["items"],
    dependencies=[Depends(verify_token_query)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid or missing API token",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid or missing API token"}
                }
            }
        }
    }
)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemResponse(Item):
    id: int



items_db = {}
counter = 1



@router.get("/items/{item_id}")
async def get_item(item_id: int):

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.get("/items")
async def get_all_items():

    return list(items_db.values())


# Небезопасные методы (POST, PUT, PATCH, DELETE) - требуют токен
@router.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):

    global counter
    item_data = item.dict()
    item_data["id"] = counter
    items_db[counter] = item_data
    counter += 1
    return item_data


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = item.dict()
    item_data["id"] = item_id
    items_db[item_id] = item_data
    return item_data


@router.patch("/items/{item_id}")
async def patch_item(item_id: int, item: Item):

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")


    current_item = items_db[item_id]
    update_data = item.dict(exclude_unset=True)
    current_item.update(update_data)
    return current_item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int):

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = items_db.pop(item_id)
    return {"message": "Item deleted", "item": deleted_item}


app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Labа #6 - Token Authentication",
        "usage": {
            "query_string": "Add ?api_token=YOUR_TOKEN to unsafe methods (POST, PUT, PATCH, DELETE)",
            "note": "GET requests don't require authentication"
        }
    }

