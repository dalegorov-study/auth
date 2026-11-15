from pydantic import BaseModel


class UserProfileCustomizationModel(BaseModel):
    theme: str
    language: str


class UserProfilePersonDetailsModel(BaseModel):
    biography: str
    interests: list[str]
    contacts: dict[str, str]


class UserProfileModel(BaseModel):
    user_id: int
    customization: UserProfileCustomizationModel
    personDetails: UserProfilePersonDetailsModel
