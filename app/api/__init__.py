from .user import router as user_router
from .product import router as product_router
from .health import router as health_router

routers = [
    user_router,
    product_router,
    health_router
]
