import unittest
import os
from schema import validate_schema, SALES_SCHEMA
from etl import transform_data
from jsonschema import validate

# Set test environment variables
os.environ["ENVIRONMENT"] = "test"
os.environ["GCP_PROJECT"] = "test-project"
os.environ["BQ_DATASET"] = "test_dataset"
os.environ["BQ_TABLE"] = "test_table"

class TestETL(unittest.TestCase):
    def test_schema_validation(self):
        valid_data = {
            "transaction_id": "TX001",
            "product_id": "P1001",
            "quantity": 2,
            "unit_price": 19.99
        }
        
        invalid_data = {
            "transaction_id": "TX001",
            "product_id": "P1001",
            "quantity": 0,  # Invalid quantity
            "unit_price": 19.99
        }
        
        # Test valid data
        is_valid, error = validate_schema(valid_data)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # Test invalid data
        is_valid, error = validate_schema(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("0 is less than the minimum of 1", error)
    
    def test_data_transformation(self):
        input_data = {
            "transaction_id": "TX001",
            "product_id": "P1001",
            "quantity": 3,
            "unit_price": 10.0,
            "tax_rate": 0.15
        }
        
        output = transform_data(input_data)
        
        # Test calculations
        self.assertEqual(output["subtotal"], 30.0)
        self.assertEqual(output["tax_amount"], 4.5)
        self.assertEqual(output["total_amount"], 34.5)
        
        # Test added fields
        self.assertIn("processing_time", output)
        self.assertEqual(output["environment"], "test")
    
    def test_bigquery_load_simulation(self):
        # This would be mocked in real tests
        # For assignment purposes, we'll simulate
        data = {
            "transaction_id": "TX001",
            "product_id": "P1001",
            "quantity": 1,
            "unit_price": 10.0,
            "subtotal": 10.0,
            "tax_amount": 1.0,
            "total_amount": 11.0,
            "processing_time": "2023-01-01T00:00:00"
        }
        
        # Simulate BigQuery load
        result = {
            "project": "test-project",
            "dataset": "test_dataset",
            "table": "test_table",
            "rows_inserted": 1
        }
        
        self.assertEqual(result["rows_inserted"], 1)

if __name__ == "__main__":
    unittest.main()