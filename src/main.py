# src/main.py
from pydantic import BaseModel, Field
from mcp.server.fastmcp import Context, FastMCP
from smithery.decorators import smithery

from services.token_manager import get_token_manager

# 1. Define a configuration schema for the MCP session
class ConfigSchema(BaseModel):
    app_id: str = Field(..., description="The App ID of your Feishu application.")
    app_secret: str = Field(..., description="The App Secret of your Feishu application.")
    refresh_token: str = Field(..., description="The initial refresh_token to start the session.")

# 2. Create the server factory function and apply the smithery decorator
@smithery.server(config_schema=ConfigSchema)
def create_server():
    """Create and configure the Feishu Token MCP server."""
    
    # 3. Instantiate the FastMCP server
    server = FastMCP(
        "Feishu Token Manager",
        description="A server to manage and refresh Feishu user access tokens.",
        version="1.0.0"
    )

    # 4. Define the tool to get the token
    @server.tool()
    def get_feishu_token(ctx: Context) -> dict:
        """
        Provides a valid Feishu access token. 
        If the existing token is expired or invalid, it will be refreshed automatically.
        The necessary app_id, app_secret, and refresh_token are retrieved from the session configuration.
        Returns a dictionary containing the access_token, new refresh_token, and expiration timestamp.
        """
        session_config = ctx.session_config
        
        # Get the token manager instance for the current session
        manager = get_token_manager(
            app_id=session_config.app_id,
            app_secret=session_config.app_secret,
            refresh_token=session_config.refresh_token
        )
        
        token_info, error = manager.get_token_info()
        
        if error:
            # In MCP, it's better to raise an exception or return a structured error
            raise Exception(f"Failed to refresh token: {error}")
            
        if not token_info:
            raise Exception("Failed to retrieve token information.")

        # Update the session's refresh_token for the next call
        session_config.refresh_token = token_info["refresh_token"]

        return token_info

    return server
