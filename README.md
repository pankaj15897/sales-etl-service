# 🚀 Sales ETL Microservice – Cloud Run + BigQuery + CI/CD

A production-ready HTTP-triggered ETL microservice built with Python, deployed on Cloud Run, integrated with BigQuery, and powered by Cloud Build CI/CD.

---

## 🔧 Implementation Steps

### ✅ Set Up GCP Environment

1. **Create a new GCP project**
2. **Enable APIs**:

   * Cloud Run
   * Cloud Build
   * BigQuery
3. **Create BigQuery datasets**:

   * `staging_sales`
   * `production_sales`

---

### 🗃️ Create Repository

```bash
git init sales-etl-service
cd sales-etl-service
# Add project files
git add .
git commit -m "Initial commit"
```

---

### ⚙️ Configure Cloud Build

1. Connect your GitHub repo to **Cloud Build**
2. Grant the following roles to the Cloud Build service account:

   * `Cloud Run Admin`
   * `Service Account User`
   * `Cloud Build Service Account`

---

### 🌍 Set Environment Variables

In Cloud Run → Service → Environment Variables tab:

| Variable      | Value                                 |
| ------------- | ------------------------------------- |
| `GCP_PROJECT` | Your GCP project ID                   |
| `BQ_DATASET`  | `staging_sales` or `production_sales` |
| `BQ_TABLE`    | `transactions`                        |

---

### 🗄️ Create BigQuery Table

```sql
CREATE TABLE `your-project.staging_sales.transactions` (
  transaction_id STRING,
  product_id STRING,
  quantity FLOAT64,
  unit_price FLOAT64,
  customer_id STRING,
  location STRING,
  tax_rate FLOAT64,
  subtotal FLOAT64,
  tax_amount FLOAT64,
  total_amount FLOAT64,
  processing_time TIMESTAMP,
  environment STRING
);
```

---

### 🧪 Test Locally

```bash
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

#### 🔁 Sample cURL Test

```bash
curl -X POST http://localhost:8080/etl \
  -H "Content-Type: application/json" \
  -d '{
        "transaction_id": "TX1001",
        "product_id": "P2001",
        "quantity": 2,
        "unit_price": 15.99
      }'
```

---

### 🚢 Deploy via CI/CD

Push changes to the main branch to trigger the build and deployment:

```bash
git push origin main
```

Monitor progress in **Cloud Build > History**.

---

## ✨ Key Features

### 🛡️ Schema Validation

* Uses JSON Schema
* Returns detailed validation errors

### 🔄 Data Transformation

* Calculates `subtotal`, `tax`, `total_amount`
* Adds `processing_time` and `environment` flags

### 📊 BigQuery Integration

* Uses official BigQuery client
* Supports streaming inserts
* Graceful error handling

### 🔁 CI/CD Pipeline

* Runs unit tests before deploy
* Deploys to **staging** and **prod**
* Supports **blue-green traffic splitting**
* Tracks revisions with Git commit SHA

---

## 🧠 Best Practices Followed

* Stateless microservice design
* Environment-specific configs
* Centralized error handling
* Structured logging (for observability)
* Health check compatibility with Cloud Run

---

## 🔧 Customization Points

### 🧬 Schema

Modify `SALES_SCHEMA` in `schema.py` to update or add fields.

### 🛠️ Transform Logic

Enhance `transform_data()` in `etl.py` to:

* Add currency conversion
* Lookup customer details
* Enrich geo-data

### 🚦 Deployment Strategy

* Customize traffic splits
* Add manual approval steps for production
* Enable canary/gradual rollouts

### 🔐 Security

* Add Firebase Auth / OAuth2
* Use API keys
* Integrate with Secret Manager

### 📈 Monitoring

* Connect to Cloud Logging & Monitoring
* Add Stackdriver alerting
* Track failed inserts

---

## ✅ Final Words

This architecture is designed for scale, clarity, and real-world reliability. Extend it to fit your business logic and confidently deploy new ETL features in minutes.
