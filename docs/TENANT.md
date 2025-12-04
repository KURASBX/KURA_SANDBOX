# Tenant Management System

## Overview
Multi-tenant architecture supporting banks, administrators, and partners with role-based access control and secure authentication.

## Tenant Types & Roles

### Tenant Types
- **BANK**: Financial institutions that manage aliases and accounts
- **ADMIN**: System administrators with oversight capabilities  
- **PARTNER**: Third-party service providers with limited access

### Role-Based Access Control
- **ADMIN**: Full system access, tenant management, regulatory endpoints
- **OPERATOR**: Daily alias operations (register/resolve/deactivate)
- **VIEWER**: Read-only access for monitoring and reporting

## Lifecycle Management

### Tenant Registration
#### Creation Flow
1. Validate unique code, email, tax_id
2. Set initial status: PENDING
3. Generate secure API key
4. Assign default OPERATOR role

#### Activation & Status
 - **PENDING**: Newly created, requires activation
 - **ACTIVE**: Fully operational tenant
 - **INACTIVE**: Temporarily disabled
 - **SUSPENDED**: Administrative suspension

### Authentication Flow
1. Tenant provides code + API key
2. System validates credentials and active status
3. JWT token issued with tenant context
4. Token used for subsequent API calls

### Security Model
#### API Key Security
 - **Format**: tk_{tenant_code}_{cryptographically_random_24_chars}

 - One-time exposure during tenant creation

 - No storage in database (tenant must secure it)

# JWT Token Claims
{
  "tenant_id": "uuid",
  "tenant_code": "string", 
  "tenant_type": "BANK|ADMIN|PARTNER",
  "roles": ["admin", "operator", "viewer"],
  "aud": "alias-api",
  "iss": "https://idp.local"
}

API Endpoints
Method	Endpoint	Purpose	Auth
POST	/tenants/	Create new tenant	Public*
GET	/tenants/	List all tenants	Admin
GET	/tenants/{id}	Get tenant details	Admin
POST	/tenants/auth/token	Authenticate tenant	Public
POST	/tenants/{code}/activate	Activate pending tenant	Admin
*Public endpoints with rate limiting and fraud detection

Use Cases
Bank Onboarding
Bank administrator submits tenant creation request

System admin reviews and activates tenant

Bank receives API key for integration

Bank begins alias management operations

Partner Integration
Payment processor registers as PARTNER tenant

Limited to alias resolution only

Can validate aliases across multiple banks

No alias creation or modification rights

Administrative Oversight
ADMIN tenants can manage all tenant lifecycles

Access regulatory and reporting endpoints

Monitor system health and usage metrics

