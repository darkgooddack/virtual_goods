from fastapi import HTTPException, status


class AppBaseError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Ошибка сервиса"

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.status_code,
            detail=self.detail
        )

# пользователь уже есть 400
# неверные логин и/или пароль
class Name(AppBaseError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "описание"