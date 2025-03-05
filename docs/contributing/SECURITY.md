# Security Guidelines

This document outlines security best practices for the Surviving the Singularity project. Following these guidelines is essential to maintain the security and integrity of the application.

## Sensitive Information

### What to Never Commit to Version Control

- **Environment Variables**: Never commit `.env` files containing actual credentials
- **API Keys**: Never hardcode API keys in the codebase
- **Database Credentials**: Never include database connection strings or credentials
- **SQL Files**: Never commit SQL files that reveal database structure
- **Private Scripts**: Utility scripts that could modify site content should be kept private
- **User Data**: Never commit files containing user information

### Excluded Directories and Files

The following directories and files are excluded from version control for security reasons:

- `/supabase/` - Contains database structure and migrations
- `*.sql` - SQL files that could reveal database structure
- `/scripts/` - Utility scripts that could be used to modify the site
- `/cursor/` - Development logs that might contain sensitive information
- `.env` files - Environment variables containing credentials

## Authentication and Authorization

### User Authentication

- Always use HTTPS for all communications
- Implement proper session management
- Use secure password storage (bcrypt or similar)
- Implement rate limiting for login attempts

### Authorization Controls

- Implement proper role-based access control (RBAC)
- Use Row Level Security (RLS) in Supabase for data access control
- Validate user permissions server-side for all protected operations
- Never rely solely on client-side permission checks

## API Security

- Validate and sanitize all user inputs
- Implement proper CORS policies
- Use CSRF tokens for form submissions
- Rate limit API endpoints to prevent abuse
- Implement proper error handling that doesn't leak sensitive information

## Database Security

- Follow the [Supabase Security Guidelines](./SUPABASE_SECURITY.md) for all database operations
- Use parameterized queries to prevent SQL injection
- Implement Row Level Security (RLS) for all tables
- Regularly audit database access logs
- Use the principle of least privilege for database access

## Frontend Security

- Sanitize user-generated content before rendering
- Implement Content Security Policy (CSP) headers
- Use SvelteKit's built-in XSS protections
- Avoid using `innerHTML` or similar DOM manipulation methods with user input

## Deployment Security

- Use environment variables for all sensitive configuration
- Regularly update dependencies to patch security vulnerabilities
- Implement proper logging for security events
- Configure proper HTTP security headers
- Use a web application firewall (WAF) if possible

## Security Incident Response

If you discover a security vulnerability:

1. **Do not** disclose it publicly in issues or discussions
2. Contact the project maintainers directly via email
3. Provide detailed information about the vulnerability
4. Allow time for the vulnerability to be addressed before disclosure

## Regular Security Practices

- Regularly run security audits on the codebase
- Keep all dependencies updated
- Review access controls periodically
- Monitor for unusual activity
- Rotate API keys and credentials regularly

By following these guidelines, we can maintain a secure application that protects both user data and system integrity.