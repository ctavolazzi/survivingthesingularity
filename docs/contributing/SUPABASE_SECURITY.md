# Supabase Security Guidelines

## Handling SQL Files Securely

The SQL files in the `supabase/` directory contain database schema definitions and migrations. These files should be handled with care for the following security reasons:

1. **Database Structure Exposure**: SQL files reveal your database structure, which could be exploited by attackers.
2. **Potential Credentials**: Ensure no credentials or sensitive information are stored in these files.
3. **Attack Surface**: Knowledge of your database schema increases the attack surface for potential SQL injection attacks.

## Security Recommendations

### Before Deployment

1. **Run the SQL scripts** to set up your database tables and functions.
2. **Verify** that everything is working correctly.
3. **Delete the SQL files** from your local machine once they've been applied to your Supabase instance.
4. **Do not commit** these files to version control (they are already in `.gitignore`).

### For the `sts_newsletter_subscribers` Table

The table contains potentially sensitive user data:
- Email addresses
- IP addresses
- User agents
- Referrer information

Ensure that:
1. **Row-Level Security (RLS)** is enabled on this table in Supabase.
2. **API access** is properly restricted to authorized users only.
3. **Regular audits** are performed to check who has accessed this data.

## After Running SQL Scripts

After you've successfully run the SQL scripts and verified that the newsletter subscription functionality works:

1. Use our cleanup script to safely remove sensitive files:
```bash
# Run the cleanup script
./scripts/database/cleanup-supabase-files.sh
```

This script will:
- Back up the README file
- Remove all SQL files
- Remove the migrations and sql directories
- Remove the supabase directory if it's empty

## Supabase Dashboard Security

1. **Enable 2FA** on your Supabase account.
2. **Regularly rotate** service role keys and JWT secrets.
3. **Monitor database access logs** for unusual activity.
4. **Implement proper RLS policies** for all tables containing user data.

Remember: The best security practice is to minimize the exposure of your database structure and to follow the principle of least privilege for all database operations.