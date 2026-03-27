---
name: pydantic
description: Use when validating and managing data structures using Python type annotations. Ideal for defining schemas, validating API responses, and ensuring structured data integrity. CRITICAL: Use `BaseModel` for complex nested schemas and `TypeAdapter` for simple types.
---
# Pydantic (V2)

## ⚠️ Mandatory Pre-flight: Resource Check

Validating massive datasets or extremely complex schemas can consume significant CPU and RAM.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Strategy**: For extremely large datasets, consider batching validation or use Polars/Pandas for bulk validation.
3. **Large Models**: Monitor memory usage when working with large nested models (e.g., LLM prompts).

## Common Pitfalls (The "Wall of Shame")

1. **Implicit Coercion**: Forgetting that Pydantic will often coerce types (e.g., "123" -> 123) by default. Use `strict=True` to prevent this.
2. **Mutable Defaults**: Using a list or dict as a default value (`friends: List[int] = []`). Pydantic handles this correctly, but it's a common footgun in general Python.
3. **Inefficient Parsing**: Using `model_validate` repeatedly on single items in a loop. Use a `TypeAdapter` for collections.

## References (Load on demand)
- `references/api-reference.md` — Formal signatures for Pydantic core classes and decorators.

## Core Concepts

### 1. Defining a Model

```python
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

# Data validation on instantiation
user = User(id=123, name="John Doe", email="john@example.com")
print(user.id)  # 123
```

### 2. Serialization (Exporting)

```python
# Convert to dict
user_dict = user.model_dump()

# Convert to JSON string
user_json = user.model_dump_json()

# Exclude specific fields
user_dict = user.model_dump(exclude={'friends'})
```

### 3. Parsing (Importing)

```python
# From dict
user = User.model_validate({'id': 123, 'name': 'John', 'email': 'j@e.com'})

# From JSON string
user = User.model_validate_json('{"id": 123, "name": "John", "email": "j@e.com"}')
```

## Advanced Features

### Field Customization

Use `Field` to add validation and metadata:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., description="The name of the item")
    price: float = Field(gt=0, description="Price must be positive")
    stock: int = Field(default=0, ge=0)
    tags: List[str] = Field(default_factory=list)
```

### Custom Validators

Use `@field_validator` for complex logic:

```python
from pydantic import BaseModel, field_validator

class Account(BaseModel):
    password: str

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
```

### Structured Output for LLMs

Pydantic is ideal for ensuring LLMs return valid JSON:

```python
from pydantic import BaseModel

class Extraction(BaseModel):
    sentiment: str
    entities: List[str]
    confidence: float

# The model's JSON schema can be passed to an LLM
schema = Extraction.model_json_schema()
```

## Common Patterns

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str

class Employee(BaseModel):
    name: str
    address: Address
```

### Root Models (for lists or dicts as top-level)

```python
from pydantic import RootModel

class UserList(RootModel):
    root: List[User]

users = UserList.model_validate([{'id': 1, ...}, {'id': 2, ...}])
```

## Performance Tips

1.  **Use `model_validate`** instead of instantiation for existing dicts.
2.  **Validation without model**: Use `TypeAdapter` for ad-hoc validation.
3.  **Strict mode**: Pass `strict=True` to prevent coerced types (e.g., "123" -> 123).

## Resources

- Official Docs: https://docs.pydantic.dev/latest/
- Pydantic V2 Migration Guide: https://docs.pydantic.dev/latest/migration/
