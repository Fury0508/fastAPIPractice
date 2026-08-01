from fastapi import FastAPI, Query, HTTPException
from data import menu_item
from models import MenuResponse, MenuItem

app = FastAPI(
    title = "Chai Point menu API",
    description="Read only menu API for Kiosk displays and movile app"
)

@app.get("/")
def root():
    return {"message": "Welcome to chai point Menu API"}



@app.get("/menu", response_model=MenuResponse) # dependency engine
def get_menu(category:str | None = Query(None, description="Filter by chai,snacks or combo")):
    if category:
        filtered = [item for item in menu_item if item['category'] == category.lower()]
        if not filtered:
            raise HTTPException(status_code= 404, detail=f"No item found in category: {category}")
        return MenuResponse(count=len(filtered), items = filtered)
    return MenuResponse(count=len(menu_item), items=menu_item)

@app.get("/menu/{item_id}", response_model=MenuItem)
def get_item(item_id: int ):
    for item in menu_item:
        if item['id'] == item_id:
            return item
    raise HTTPException(status_code= 404, detail=f"Menu item with id {item_id} not found")


