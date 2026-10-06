class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR", details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(AppException):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR", details=details)


class NotFoundError(AppException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(message=f"{resource} not found: {identifier}", status_code=404, error_code="NOT_FOUND")


class ModelError(AppException):
    def __init__(self, model_name: str, reason: str):
        super().__init__(message=f"Model {model_name} failed: {reason}", status_code=500, error_code="MODEL_ERROR", details={"model": model_name})
