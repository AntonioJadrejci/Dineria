from database import test_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import Restaurant
from schemas import RestaurantCreate, RestaurantResponse
from fastapi import HTTPException
from models import Category, Product
from schemas import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, RestaurantMenuResponse
app = FastAPI(
    title="Dineria API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Dineria API!"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "application": "Dineria"
    }


@app.get("/api/database-test")
def database_test():
    try:
        result = test_connection()

        return {
            "status": "connected",
            "database": "Supabase PostgreSQL",
            "result": result
        }

    except Exception as error:
        print("Database connection failed:", type(error).__name__)

        return {
            "status": "error",
            "message": "Database connection failed"
        }


@app.post("/api/restaurants", response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):
    new_restaurant = Restaurant(
        name=restaurant.name,
        slug=restaurant.slug,
        description=restaurant.description
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


@app.post("/api/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    restaurant = db.get(Restaurant, category.restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    new_category = Category(
        name=category.name,
        restaurant_id=category.restaurant_id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@app.post("/api/products", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    category = db.get(Category, product.category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get(
    "/api/restaurants/{slug}/menu",
    response_model=RestaurantMenuResponse
)
def get_restaurant_menu(
    slug: str,
    db: Session = Depends(get_db)
):
    statement = (
        select(Restaurant)
        .where(Restaurant.slug == slug)
        .options(
            selectinload(Restaurant.categories)
            .selectinload(Category.products)
        )
    )

    restaurant = db.scalar(statement)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return restaurant
