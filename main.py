import json
import os
from flask import Flask, request, jsonify
from schema import validate_schema
from etl import transform_data, load_to_bigquery
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/etl', methods=['POST'])
def etl_process():
    try:
        # Get JSON payload
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        # Validate schema
        is_valid, error = validate_schema(payload)
        if not is_valid:
            return jsonify({"error": f"Schema validation failed: {error}"}), 400
        
        # Transform data
        transformed_data = transform_data(payload)
        
        # Load to BigQuery
        project_id = os.getenv("euphoric-fusion-462011-r4")
        dataset_id = os.getenv("BQ_DATASET", "staging_sales")
        table_id = os.getenv("BQ_TABLE", "transactions")
        
        load_result = load_to_bigquery(transformed_data, project_id, dataset_id, table_id)
        
        return jsonify({
            "status": "success",
            "data": transformed_data,
            "bq_result": load_result
        }), 200
    
    except Exception as e:
        logging.exception("ETL processing failed")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)