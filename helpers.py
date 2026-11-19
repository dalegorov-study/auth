from fastapi import HTTPException, Request, status


def get_user_id_from_cookie(request: Request) -> int:
    try:
        return int(request.cookies.get('x-user-id', ''))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized',
        )
