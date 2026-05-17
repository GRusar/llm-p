class AppError(Exception):
    default_message = "Application error"
    code = "APP_ERROR"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        self.code = type(self).code
        super().__init__(self.message)


class ConflictError(AppError):
    default_message = "Resource already exists"
    code = "CONFLICT"


class UnauthorizedError(AppError):
    default_message = "Unauthorized"
    code = "UNAUTHORIZED"


class ForbiddenError(AppError):
    default_message = "Forbidden"
    code = "FORBIDDEN"


class NotFoundError(AppError):
    default_message = "Resource not found"
    code = "NOT_FOUND"


class ExternalServiceError(AppError):
    default_message = "External service error"
    code = "EXTERNAL_SERVICE_ERROR"
