class UserNotFoundError(Exception):
    ...


class UserEmailAlreadyExistsError(Exception):
    ...


class UserProfileNotFoundError(Exception):
    ...


class UserInactiveError(Exception):
    ...


class FileAlreadyExistsError(Exception):
    ...


class InvalidFileDataError(Exception):
    ...
