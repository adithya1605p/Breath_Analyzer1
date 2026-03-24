"""
Updates DATABASE_URL in .env to use Supabase transaction pooler (port 6543)
instead of the direct DB host (port 5432) which is inaccessible externally.
"""
import re

with open('.env', 'r') as f:
    content = f.read()

# Find line with DATABASE_URL
m = re.search(r'DATABASE_URL=postgresql://([^:]+):([^@]+)@db\.([^.]+)\.supabase\.co:5432/postgres', content)
if not m:
    print("Could not find DATABASE_URL with direct host format")
    print("Trying alternative format...")
    # Maybe it's just postgres:// without the postgres. prefix
    m = re.search(r'DATABASE_URL=postgresql://postgres:([^@]+)@db\.([^.]+)\.supabase\.co:5432/postgres', content)
    if m:
        password = m.group(1)
        ref = m.group(2)
        user = 'postgres'
    else:
        print("Cannot parse URL, aborting")
        exit(1)
else:
    user = m.group(1)
    password = m.group(2)
    ref = m.group(3)

print(f"Project ref: {ref}")
print(f"User: {user}")

# Build transaction pooler URL: port 6543, pooler hostname
new_url = f"postgresql://{user}:{password}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
old_pattern = rf'DATABASE_URL=postgresql://{re.escape(user)}:{re.escape(password)}@db\.{re.escape(ref)}\.supabase\.co:5432/postgres[^\n]*'
new_content = re.sub(old_pattern, f'DATABASE_URL={new_url}', content)

if new_content == content:
    print("No change made - URL not found with exact format")
else:
    with open('.env', 'w') as f:
        f.write(new_content)
    print(f"Updated DATABASE_URL to use pooler: aws-0-ap-south-1.pooler.supabase.com:6543")
