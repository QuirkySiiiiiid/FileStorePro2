import time
from aiohttp import web
from database.database import full_userbase  # Import function to get all users from DB

routes = web.RouteTableDef()

# Store bot start time
BOT_START_TIME = time.time()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("QuirkySiiiiiid.... ✅")

@routes.get("/status", allow_head=True)
async def status_handler(request):
    # Calculate uptime
    uptime_seconds = int(time.time() - BOT_START_TIME)
    uptime = f"{uptime_seconds // 3600}h { (uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"
    
    # Fetch user data from database
    users = await full_userbase()  # This function should return a list of user dicts
    total_users = len(users)
    
    # Extract usernames (or fallback to 'No Username')
    user_list = [f"@{user['username']}" if user['username'] else "No Username" for user in users]
    
    return web.json_response({
        "status": "Server is running",
        "uptime": uptime,
        "total_users": total_users,
        "users": user_list
    })

app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=8080)  # Change port if needed
