import logging
from aiohttp import web
from .route import routes

# Configure logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the async web server setup
async def web_server():
    try:
        # Create the web application with a 30MB max client size
        web_app = web.Application(client_max_size=30000000)

        # Add routes from the routes module
        web_app.add_routes(routes)
        
        # Log successful server setup
        logger.info("Web server setup successful.")

        # Return the configured web application
        return web_app
    except Exception as e:
        # Log errors during server setup
        logger.error(f"Error in server setup: {e}")
        raise

# Run the server (this can be used if you run the script directly)
if __name__ == '__main__':
    try:
        app = web_server()
        web.run_app(app)  # Run the web server
        logger.info("Web server is running.")
    except Exception as e:
        logger.error(f"Failed to start the server: {e}")
