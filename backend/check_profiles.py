import asyncio, asyncpg

async def main():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    raw_url = os.environ.get("DATABASE_URL", "")
    # asyncpg uses postgresql:// not postgresql+asyncpg
    url = raw_url.replace("postgresql+asyncpg://", "postgresql://")
    url = url.split("?")[0]  # strip query params
    try:
        conn = await asyncpg.connect(url)
        rows = await conn.fetch("SELECT id, username, role FROM profiles LIMIT 10")
        print(f"Found {len(rows)} profiles:")
        for r in rows:
            print(f"  id={str(r['id'])} username={r['username']} role={r['role']}")
        await conn.close()
    except Exception as e:
        print(f"DB ERROR: {e}")

asyncio.run(main())
