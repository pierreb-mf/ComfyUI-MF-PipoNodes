"""
MF PipoNodes - Server Endpoints
API routes for Graph Plotter and Story Driver functionality
"""

from aiohttp import web
import server
import base64
import os

# Import the node classes to access their state
from .pipo_nodes_integrated import MF_GraphPlotter, MF_StoryDriver


@server.PromptServer.instance.routes.post("/api/graph_plotter/reset")
async def reset_graph_plotter(request):
    """
    API endpoint to reset a Graph Plotter node's data
    """
    try:
        data = await request.json()
        node_id = data.get("node_id")

        if not node_id:
            return web.json_response(
                {"success": False, "error": "node_id is required"}, status=400
            )

        # Call the reset method on the node class
        MF_GraphPlotter.reset_node_data(node_id)

        return web.json_response(
            {"success": True, "node_id": node_id, "message": "Graph data reset"}
        )

    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@server.PromptServer.instance.routes.post("/api/graph_plotter/save_image")
async def save_graph_image(request):
    """
    API endpoint to save graph image from base64 data to user-selected path
    """
    try:
        data = await request.json()
        image_data = data.get("image_data")
        save_path = data.get("save_path")

        if not image_data or not save_path:
            return web.json_response(
                {"success": False, "error": "image_data and save_path are required"},
                status=400,
            )

        # Remove data URL prefix if present
        if image_data.startswith("data:image"):
            image_data = image_data.split(",")[1]

        # Decode base64 and save
        image_bytes = base64.b64decode(image_data)

        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Write file (overwrites if exists)
        with open(save_path, "wb") as f:
            f.write(image_bytes)

        print(f"📊 Graph image saved to: {save_path}")

        return web.json_response({"success": True, "path": save_path})

    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


# ============================================================================
# STORY DRIVER ENDPOINTS
# ============================================================================


@server.PromptServer.instance.routes.post("/api/story_driver/reset")
async def reset_story_driver(request):
    """
    API endpoint to reset a Story Driver project
    """
    try:
        data = await request.json()
        project_name = data.get("project_name", "MyProject")
        randomize_seed = data.get("randomize_seed", True)

        # Call the reset method on the node class
        MF_StoryDriver.reset_project(project_name, randomize_seed)

        # Get updated state
        state = MF_StoryDriver._state.get(project_name, {"step": 0, "seed": 0})

        return web.json_response(
            {
                "success": True,
                "project_name": project_name,
                "step": state["step"],
                "seed": state["seed"],
            }
        )

    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
