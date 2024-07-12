from pydantic import BaseModel, Field


class OperationValidator(BaseModel):
    """Validate if a user wants to post a transaction or wants to get
    information from data already entered before into the database.
    Returned only the type of transaction: POST or GET."""
    type: str = Field(..., description="Type of operation if POST or GET")


class PostOperation(BaseModel):
    """Extract information about the transaction of the user
    if it is preforming an income or expense operation, get total amount,
    concept, and bank or card name"""

    amount: int = Field(..., description="Total amount of transaction")
    description: str = Field(..., description="Description or concept of transaction")
    card_name: str = Field(..., description="Name of the bank account or card")
    type: str = Field(..., description="Type of operation if income or expense")
