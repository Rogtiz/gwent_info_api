from pydantic import BaseModel, Field

class UserCreationSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user")
    chat_id: str = Field(..., min_length=8, max_length=128, description="The chat ID of the user")

class UserSchema(BaseModel):
    id: int
    username: str
    chat_id: str
    full_name: str | None = None
    description: str | None = None
    disabled: bool = False
    admin_level: int = 0
    is_banned: bool = False


class FeedbackCreationSchema(BaseModel):
    chat_id: str
    message: str = Field(..., min_length=1, max_length=500, description="Feedback message from the user")
    is_fixed: bool = False


class FeedbackSchema(BaseModel):
    id: int
    user_id: int
    chat_id: str
    message: str
    is_fixed: bool = False