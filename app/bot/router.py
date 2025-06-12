from fastapi import APIRouter, HTTPException
from app.bot.dao import UsersDAO, PropertiesDAO, FeedbacksDAO
from app.bot.schemas import UserSchema, UserCreationSchema, FeedbackSchema, FeedbackCreationSchema

router = APIRouter()

@router.get("user/{chat_id}")
async def get_user(chat_id: str) -> UserSchema:
    """
    Get user by chat_id.
    """
    user = await UsersDAO.find_one_or_none(chat_id=chat_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/user")
async def create_user(user_data: UserCreationSchema) -> UserSchema:
    """
    Create a new user.
    """
    user = await UsersDAO.add(user_data.dict())
    if user:
        return user
    raise HTTPException(status_code=400, detail="User not created")


@router.get("/feedback")
async def get_all_feedback() -> list[FeedbackSchema]:
    """
    Get all feedback.
    """
    feedback = await FeedbacksDAO.find_all()
    if feedback:
        return feedback
    raise HTTPException(status_code=404, detail="No feedback found")


@router.post("/feedback")
async def create_feedback(feedback_data: FeedbackCreationSchema) -> FeedbackSchema:
    """
    Create a new feedback.
    """
    feedback = await FeedbacksDAO.add(feedback_data)
    if feedback:
        return feedback
    raise HTTPException(status_code=400, detail="Feedback not created")


@router.get("/property/{key}")
async def get_property(key: str) -> str:
    """
    Get a property by key.
    """
    property_value = await PropertiesDAO.find_one_or_none(name=key)
    if property_value:
        return property_value.value
    raise HTTPException(status_code=404, detail="Property not found")


@router.post("/property")
async def create_property(key: str, value: str) -> str:
    """
    Create a new property.
    """
    property_value = await PropertiesDAO.add(name=key, value=value)
    if property_value:
        return property_value.value
    raise HTTPException(status_code=400, detail="Property not created")


@router.delete("/property/{key}")
async def delete_property(key: str) -> str:
    """
    Delete a property by key.
    """
    deleted = await PropertiesDAO.delete(name=key)
    if deleted:
        return f"Property '{key}' deleted successfully"
    raise HTTPException(status_code=404, detail="Property not found")


@router.put("/property/{key}")
async def update_property(key: str, value: str) -> str:
    """
    Update a property by key.
    """
    updated_property = await PropertiesDAO.update(name=key, value=value)
    if updated_property:
        return updated_property.value
    raise HTTPException(status_code=404, detail="Property not found")