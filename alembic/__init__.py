from fastapi import APIRouter

from alembic.controllers.alembic_controller import router as alembic_router

# __all__ = ['alembic_crud']

router = APIRouter()
router.include_router(router=alembic_router, prefix="/alembic", tags=["alembic"])
