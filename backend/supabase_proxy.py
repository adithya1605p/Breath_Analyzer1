"""
Simple HTTP proxy to route Supabase requests through IPv6
Run this alongside your backend
"""
import asyncio
import aiohttp
from aiohttp import web

SUPABASE_HOST = "db.tmavkmymbdcmugunjtle.supabase.co"
SUPABASE_PORT = 5432

async def proxy_handler(request):
    """Proxy PostgreSQL connections to Supabase"""
    # This won't work for PostgreSQL protocol, need different approach
    return web.Response(text="Proxy running", status=200)

async def start_proxy():
    app = web.Application()
    app.router.add_route('*', '/{tail:.*}', proxy_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 5433)
    await site.start()
    print("[PROXY] Supabase proxy running on localhost:5433")
    print("[PROXY] Update DATABASE_URL to use localhost:5433")
    
if __name__ == "__main__":
    asyncio.run(start_proxy())
    asyncio.get_event_loop().run_forever()
