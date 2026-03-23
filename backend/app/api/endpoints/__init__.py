from fastapi import APIRouter
from . import dashboard, gee, users, admin_complaints, admin_tasks, admin_alerts

api_router = APIRouter()
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(gee.router, prefix="/gee", tags=["earth-engine"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# Citizen-scoped routes: /user/complaints (no admin required)
api_router.include_router(users.router, prefix="/user", tags=["citizen"])
api_router.include_router(admin_complaints.router, prefix="/admin/complaints", tags=["admin-complaints"])
api_router.include_router(admin_tasks.router, prefix="/admin/tasks", tags=["admin-tasks"])
api_router.include_router(admin_alerts.router, prefix="/admin/alerts", tags=["admin-alerts"])
