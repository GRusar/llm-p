from app.core.errors import AppError


def error_detail(exc: AppError) -> dict[str, str]:
    return {"code": exc.code, "message": exc.message}
