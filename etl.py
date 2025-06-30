import datetime
import os
from google.cloud import bigquery

def transform_data(data):
    """Transform sales data with calculations and enrichment"""
    # Calculate derived fields
    subtotal = data['quantity'] * data['unit_price']
    tax_rate = data.get('tax_rate', 0.1)  # Default to 10% tax
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount
    
    # Add timestamps
    current_time = datetime.datetime.utcnow().isoformat()
    
    # Return enriched data
    return {
        **data,
        "subtotal": subtotal,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "processing_time": current_time,
        "environment": os.getenv("ENVIRONMENT", "dev")
    }

def load_to_bigquery(data, project_id, dataset_id, table_id):
    """Load transformed data to BigQuery"""
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    errors = client.insert_rows_json(
        table_ref,
        [data],
        row_ids=[data['transaction_id']]
    )
    
    if errors:
        raise RuntimeError(f"BigQuery insert errors: {errors}")
    
    return {
        "project": project_id,
        "dataset": dataset_id,
        "table": table_id,
        "rows_inserted": 1
    }