"""
MF Data Nodes for ComfyUI
Save, Read, and Show data in various formats (JSON, XML, CSV, YAML)
"""

import os
from .mf_data_nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Get the directory where this __init__.py is located
WEB_DIRECTORY = "./web"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
