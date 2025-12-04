# Alias Management System

## Overview
Secure alias-based payment routing system that replaces sensitive account numbers with memorable aliases while maintaining full auditability and regulatory compliance.

## Core Use Cases

### 1. Alias Registration & Management
- **Registration**: Create new aliases with bank account mapping
- **Validation**: Enforce alias format (4-30 chars, alphanumeric)
- **Normalization**: Automatic case-insensitive handling
- **Uniqueness**: Prevent duplicate active aliases per tenant
- **Status Management**: ACTIVE/INACTIVE lifecycle

### 2. Alias Resolution & Privacy
- **Limited Exposure**: Only reveal bank, account type, last 4 digits
- **Tenant Isolation**: Aliases are scoped to specific banks/tenants
- **Privacy by Design**: No PII exposure in resolution responses

### 3. Audit & Compliance Features
- **Hash Chain**: Cryptographically linked event history
- **WORM Compliance**: Write-Once-Read-Many evidence generation
- **Integrity Verification**: Tamper-detection for audit trails
- **Regulatory Access**: Controlled endpoints for auditors

### 4. Interoperability
- **Global Registry**: Cross-tenant alias validation
- **Secure Routing**: Bank routing code resolution (SWIFT/BIC)
- **Audit Trail**: Log all cross-tenant queries
- **Privacy-Preserving**: Hash-based validation without data exposure

## Security Architecture

### Hash Chain Implementation
CUB Hash (Pseudonymization):
SHA256(tenant_id + bank + account_type + last_4 + alias_normalized + pepper)

Event Hash Chain (Audit Integrity):
SHA256(tenant_id + alias + event_type + timestamp + previous_hash)

### Privacy Safeguards
- **No PII Storage**: Only hashed references to sensitive data
- **Limited Resolution**: Expose only necessary information for payments
- **Tenant Boundaries**: Strict data isolation between institutions
- **Audit-Only Access**: Regulators see hashes, not raw data

## API Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/aliases/` | Register new alias | JWT |
| GET | `/aliases/{alias}` | Resolve alias to account hint | JWT |
| DELETE | `/aliases/{alias}` | Deactivate alias | JWT |
| GET | `/aliases/{alias}/history` | Get full event history | JWT |
| GET | `/aliases/{alias}/verify-chain` | Verify hash chain integrity | JWT |
| GET | `/aliases/{alias}/validate` | Global interoperability check | JWT |
| GET | `/regulatory/worm-evidence/{date}` | WORM compliance data | Admin JWT |

## Data Models

### AliasRegistryEntity
- Core alias mapping with validation rules
- Status lifecycle management
- CUB hash for pseudonymized linking

### AliasEventEntity  
- Immutable audit trail entries
- Hash chain for integrity verification
- Correlation ID for request tracing

### GlobalAliasEntity
- Cross-tenant alias registry
- Routing code mapping (SWIFT/BIC)
- Active/inactive status for interoperability