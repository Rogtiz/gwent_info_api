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
    user_id: int | None
    chat_id: str
    message: str
    is_fixed: bool = False


class PropertySchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the property")
    value: str = Field(..., min_length=1, max_length=500, description="The value of the property")
    description: str | None = Field(None, max_length=500, description="Description of the property")


class PropertyCreationSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the property")
    value: str = Field(..., min_length=1, max_length=500, description="The value of the property")
    description: str | None = Field(None, max_length=500, description="Description of the property")


class GroupSchema(BaseModel):
    id: int
    name: str
    chat_id: str
    description: str | None = None
    disabled: bool = False


class GroupCreationSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the group")
    chat_id: str = Field(..., min_length=8, max_length=128, description="The chat ID of the group")
    description: str | None = Field(None, max_length=500, description="Description of the group")
    disabled: bool = False