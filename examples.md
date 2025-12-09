# Examples — calling the Resume Analyzer

curl example (POST JSON):

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Vardan Rastogi\nSoftware engineer with 3 years experience...",
    "job_description": "Backend Developer Intern\nWe are looking for candidates with Python and ML experience..."
  }'
```

You can also use Postman — import `main.py`'s `/analyze` route by visiting `http://127.0.0.1:8000/docs` and copying the request body.
