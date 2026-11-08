
from io import BytesIO
from uuid import uuid4

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image, UnidentifiedImageError

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import get_db, test_connection
from models import Restaurant, Category, Product
from schemas import (
    RestaurantCreate,
    RestaurantResponse,
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    RestaurantMenuResponse,
)
from storage import supabase, BUCKET_NAME

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


MAX_IMAGE_SIZE = 5 * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "JPEG": ("image/jpeg", "jpg"),
    "PNG": ("image/png", "png"),
    "WEBP": ("image/webp", "webp"),
}


@app.post(
    "/api/products/{product_id}/image",
    response_model=ProductResponse
)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Čitamo najviše 5 MB + 1 bajt.
    image_bytes = await file.read(MAX_IMAGE_SIZE + 1)

    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image must be smaller than 5 MB"
        )

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image_format = image.format
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )

    if image_format not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG and WEBP are allowed"
        )

    content_type, extension = ALLOWED_IMAGE_TYPES[image_format]

    file_path = (
        f"restaurants/{product.category.restaurant_id}/"
        f"products/{product.id}/{uuid4().hex}.{extension}"
    )

    
    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            path=file_path,
            file=image_bytes,
            file_options={
                "content-type": content_type,
                "upsert": "false"
            }
        )

        image_url = supabase.storage.from_(
            BUCKET_NAME
        ).get_public_url(file_path)

    except Exception as error:
        print(f"SUPABASE STORAGE ERROR: {error}")

        raise HTTPException(
            status_code=502,
            detail="Image upload failed"
        ) from error

    product.image_url = image_url
    db.commit()
    db.refresh(product)

    return product


@app.patch(
    "/api/categories/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = category_data.name.strip()

    if not category.name:
        raise HTTPException(
            status_code=422,
            detail="Category name cannot be empty"
        )

    db.commit()
    db.refresh(category)

    return category


@app.delete("/api/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if category.products:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a category that contains products"
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully"
    }


