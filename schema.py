from jsonschema import validate, ValidationError

# Define JSON schema for sales transactions
SALES_SCHEMA = {
    "type": "object",
    "properties": {
        "transaction_id": {"type": "string"},
        "product_id": {"type": "string"},
        "quantity": {"type": "number", "minimum": 1},
        "unit_price": {"type": "number", "minimum": 0},
        "customer_id": {"type": "string"},
        "location": {"type": "string"},
        "tax_rate": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["transaction_id", "product_id", "quantity", "unit_price"]
}

def validate_schema(data):
    try:
        validate(instance=data, schema=SALES_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, e.message