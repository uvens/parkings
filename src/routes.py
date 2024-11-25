from fastapi import APIRouter
from src.booking.routers import router as booking_router
from src.auth.routers import router as auth_router
from src.parcking.routers import router as parking_router
from src.payment.routers import router as payment_router

router = APIRouter(prefix='/parking')
router.include_router(booking_router)
router.include_router(auth_router)
router.include_router(parking_router)
router.include_router(payment_router)
