from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Pantry API")

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    quantity: int = 1
    notes: Optional[str] = None

# simple in-memory store
_items: List[Item] = [Item(id=1, name="Sugar", quantity=2),
    Item(id=2, name="Flour", quantity=1, notes="All-purpose"),]
_next_id = 1

@app.get("/")
def root():
    return {"message": "Pantry API is running"}

@app.get("/items", response_model=List[Item])
def list_items():
    return _items

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for it in _items:
        if it.id == item_id:
            return it
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    global _next_id
    item.id = _next_id
    _next_id += 1
    _items.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, payload: Item):
    for idx, it in enumerate(_items):
        if it.id == item_id:
            updated = it.copy(update=payload.dict(exclude_unset=True))
            updated.id = item_id
            _items[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for idx, it in enumerate(_items):
        if it.id == item_id:
            _items.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Item not found")