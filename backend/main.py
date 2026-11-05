
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import get_db, test_connection
from models import Restaurant, Category, Product
from schemas import (
    RestaurantCreate,
    RestaurantResponse,
    CategoryCreate,
    CategoryResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    RestaurantMenuResponse
)


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


@app.post(
    "/api/restaurants",
    response_model=RestaurantResponse
)
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


@app.post(
    "/api/categories",
    response_model=CategoryResponse,
    status_code=201
)
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


@app.post(
    "/api/products",
    response_model=ProductResponse,
    status_code=201
)
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


@app.patch(
    "/api/products/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    existing_product = db.get(Product, product_id)

    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_data = product.model_dump(exclude_unset=True)

    # Provjeri novu kategoriju ako je korisnik mijenja.
    if "category_id" in update_data:
        new_category_id = update_data["category_id"]

        if new_category_id is None:
            raise HTTPException(
                status_code=422,
                detail="Category ID cannot be null"
            )

        new_category = db.get(Category, new_category_id)

        if new_category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        current_category = db.get(
            Category,
            existing_product.category_id
        )

        if new_category.restaurant_id != current_category.restaurant_id:
            raise HTTPException(
                status_code=400,
                detail="Category belongs to another restaurant"
            )

    # Ažuriraj samo polja koja su poslana.
    for field, value in update_data.items():
        setattr(existing_product, field, value)

    db.commit()
    db.refresh(existing_product)

    return existing_product


@app.delete(
    "/api/products/{product_id}",
    status_code=204
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    existing_product = db.get(Product, product_id)

    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(existing_product)
    db.commit()
