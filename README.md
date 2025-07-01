# calculate_reorder_quantity
IBM Cloud의 code engine을 통해 바로 배포하여 서비스 함.

https://calculate-reorder-app.1wrbgjmhze46.us-south.codeengine.appdomain.cloud
https://calculate-reorder-app.1wrbgjmhze46.us-south.codeengine.appdomain.cloud


```curl
curl -X POST "https://calculate-reorder-app.1wrbgjmhze46.us-south.codeengine.appdomain.cloud/calculate-reorder-quantity" \
  -H "Content-Type: application/json" \
  -u "test:test" \
  -d '{
    "current_inventory": 100,
    "historic_data": 120,
    "forecast": 150
  }'
```

```bash
  pip install fastapi uvicorn
```
```bash
uvicorn calculate_reorder_quantity:app --host 0.0.0.0 --port 8080 --reload

```

curl -X POST "http://127.0.0.1:8080/calculate-reorder-quantity" \
  -H "Content-Type: application/json" \
  -u "test:test" \
  -d '{
    "current_inventory": 100,
    "historic_data": 120,
    "forecast": 150
  }'
