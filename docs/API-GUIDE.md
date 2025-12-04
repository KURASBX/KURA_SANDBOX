# API Integration Guide

## Quick Start

### 1. Tenant Registration
```bash
curl -X POST https://api.aliassystem.com/tenants/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Bank",
    "code": "exbank",
    "type": "BANK", 
    "contact_email": "admin@exbank.com",
    "roles": ["OPERATOR"]
  }'
```

### 2. Alias Management Examples
# Register alias
response = await client.post("/aliases/", json={
    "alias": "john.doe2024",
    "bank": "Banco Santander", 
    "account_type": "CTA_CORRIENTE",
    "last_4": "1234"
})

# Resolve alias
response = await client.get("/aliases/john.doe2024")
# Returns: {"exists": true, "account_hint": {"bank": "Santander", "type": "CTA_CORRIENTE", "last_4": "1234"}}

# Error Handling
## Common HTTP Status Codes
 - 400 - Validation errors (invalid alias format, etc.)
 - 401 - Authentication required/invalid
 - 403 - Insufficient permissions
 - 404 - Alias or tenant not found
 - 409 - Alias already exists
 - 429 - Rate limit exceeded

## Error Response Format
{
  "detail": "EV008",
  "message": "Alias already exists for this tenant"
}

# Best Practices
## Security
 - Store API keys securely using environment variables
 - Implement JWT token rotation
 - Use correlation IDs for troubleshooting
 - Enable audit logging for compliance

# Performance
 - Cache alias resolutions when appropriate
 - Implement exponential backoff for retries
 - Batch operations for bulk alias management
 - Monitor hash chain verification costs