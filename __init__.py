"""
MF PipoNodes - ComfyUI Custom Nodes
Collection of utility nodes and workflow management tools
Author: Pierre Biet | Moment Factory | 2025
Version: 1.5.1
"""

print("\n" + "=" * 70)
print("[MF_PipoNodes] Initialization starting...")
print("=" * 70)

# Test 1: Check if pipo_nodes_integrated exists
import os
module_dir = os.path.dirname(__file__)
print(f"[MF_PipoNodes] Module directory: {module_dir}")

integrated_file = os.path.join(module_dir, "pipo_nodes_integrated.py")
if os.path.exists(integrated_file):
    size = os.path.getsize(integrated_file)
    print(f"[MF_PipoNodes] ✅ Found pipo_nodes_integrated.py ({size:,} bytes)")
else:
    print(f"[MF_PipoNodes] ❌ ERROR: pipo_nodes_integrated.py NOT FOUND!")
    print(f"[MF_PipoNodes] Expected at: {integrated_file}")

server_file = os.path.join(module_dir, "pipo_nodes_server.py")
if os.path.exists(server_file):
    size = os.path.getsize(server_file)
    print(f"[MF_PipoNodes] ✅ Found pipo_nodes_server.py ({size:,} bytes)")
else:
    print(f"[MF_PipoNodes] ❌ ERROR: pipo_nodes_server.py NOT FOUND!")

web_dir = os.path.join(module_dir, "web")
if os.path.exists(web_dir):
    print(f"[MF_PipoNodes] ✅ Found web/ directory")
    js_files = [f for f in os.listdir(web_dir) if f.endswith('.js')]
    for js_file in js_files:
        print(f"[MF_PipoNodes]   - {js_file}")
else:
    print(f"[MF_PipoNodes] ⚠️  Warning: web/ directory not found")

print("-" * 70)

# Test 2: Try importing node classes
try:
    print("[MF_PipoNodes] Attempting to import node classes...")
    from .pipo_nodes_integrated import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    print(f"[MF_PipoNodes] ✅ SUCCESS! Loaded {len(NODE_CLASS_MAPPINGS)} nodes:")
    for i, node_name in enumerate(NODE_CLASS_MAPPINGS.keys(), 1):
        display_name = NODE_DISPLAY_NAME_MAPPINGS.get(node_name, node_name)
        print(f"[MF_PipoNodes]   {i:2d}. {node_name:20s} → {display_name}")
except ImportError as e:
    print(f"[MF_PipoNodes] ❌ ImportError: {e}")
    print("[MF_PipoNodes] This usually means:")
    print("[MF_PipoNodes]   - pipo_nodes_integrated.py has a syntax error")
    print("[MF_PipoNodes]   - Or it's trying to import something that doesn't exist")
    import traceback
    traceback.print_exc()
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
except Exception as e:
    print(f"[MF_PipoNodes] ❌ Unexpected error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}

print("-" * 70)

# Test 3: Try importing server endpoints
try:
    print("[MF_PipoNodes] Attempting to import server endpoints...")
    from . import pipo_nodes_server
    print("[MF_PipoNodes] ✅ Server endpoints loaded")
except ImportError as e:
    print(f"[MF_PipoNodes] ⚠️  Warning: Could not load server: {e}")
    print("[MF_PipoNodes] Reset buttons may not work, but nodes will function")
except Exception as e:
    print(f"[MF_PipoNodes] ⚠️  Warning: Server error: {type(e).__name__}: {e}")

print("=" * 70)
print(f"[MF_PipoNodes] Initialization {'COMPLETE' if len(NODE_CLASS_MAPPINGS) > 0 else 'FAILED'}")
print(f"[MF_PipoNodes] Nodes available: {len(NODE_CLASS_MAPPINGS)}")
print("=" * 70 + "\n")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Web directory for JavaScript extensions
WEB_DIRECTORY = "./web"
