# CLAUDE.md - Technical Documentation for AI Assistants

> **Purpose:** This document provides technical context about ComfyUI-MF-PipoNodes architecture, conventions, and implementation patterns for AI assistants and developers working on this project.

---

## 📋 Project Overview

**ComfyUI-MF-PipoNodes** is a collection of 10+ utility nodes for ComfyUI workflows, developed by Pierre Biet at Moment Factory. The project focuses on workflow enhancement, data persistence, visualization, and sequential processing.

**Version:** 1.5.2
**License:** MIT
**Author:** Pierre Biet | Moment Factory | 2025

---

## 🏗️ Architecture

### File Structure

```
ComfyUI-MF-PipoNodes/
├── __init__.py                    # Module initialization & diagnostics
├── pipo_nodes_integrated.py       # All node class definitions
├── pipo_nodes_server.py           # API routes & endpoints
├── requirements.txt               # Python dependencies
├── web/
│   └── pipoNodes.js              # Frontend logic & widgets
├── *.md                          # Documentation files
└── [state files]                 # Auto-generated JSON state files
    ├── story_driver_state.json
    └── graph_plotter_state.json
```

### Key Components

#### 1. **Node Definitions** (`pipo_nodes_integrated.py`)

All node classes follow ComfyUI conventions:

```python
class MF_NodeName:
    CATEGORY = "MF_PipoNodes/Category"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {...},
            "optional": {...},
            "hidden": {...}
        }

    RETURN_TYPES = (...)
    RETURN_NAMES = (...)
    FUNCTION = "main_function"
    OUTPUT_NODE = True  # If node should execute on queue

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")  # Force re-execution

    def main_function(self, ...):
        return {...}
```

**Important Patterns:**
- Use `IS_CHANGED` returning `float("nan")` to force re-execution
- `OUTPUT_NODE = True` ensures execution on every queue
- State is stored in class-level variables (e.g., `cls._state`)
- Console logging uses emojis for visual identification

#### 2. **API Endpoints** (`pipo_nodes_server.py`)

API routes for frontend interactions (reset buttons, save functions):

```python
from aiohttp import web
import server

@server.PromptServer.instance.routes.post("/api/endpoint_name")
async def handler_function(request):
    try:
        data = await request.json()
        # Process request
        return web.json_response({"success": True, ...})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
```

**Critical Convention:**
- **ALL routes MUST use `/api/` prefix** (ComfyUI's `api.fetchApi()` adds this automatically)
- Example: `/api/story_driver/reset`, `/api/graph_plotter/save_image`

**Current Endpoints:**
- `POST /api/story_driver/reset` - Reset project step and seed
- `POST /api/graph_plotter/reset` - Clear graph data for specific node
- `POST /api/graph_plotter/save_image` - Save graph as PNG

#### 3. **Frontend Extensions** (`web/pipoNodes.js`)

Extends ComfyUI nodes with custom UI elements:

```javascript
import { app } from "../../scripts/app.js"
import { api } from "../../scripts/api.js"

app.registerExtension({
  name: "MF.PipoNodes",

  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "MF_NodeName") {
      // Add custom widgets, buttons, or displays
      const onNodeCreated = nodeType.prototype.onNodeCreated
      nodeType.prototype.onNodeCreated = function() {
        onNodeCreated?.apply(this, arguments)
        // Custom initialization
      }
    }
  }
})
```

**UI Components:**
- **Reset Buttons:** Call API endpoints to clear state
- **Status Displays:** Read-only text showing state info
- **Interactive Canvas:** Chart.js graphs for visualization
- **Save Buttons:** Trigger file dialogs and save operations

#### 4. **Module Initialization** (`__init__.py`)

Comprehensive initialization with diagnostics:

```python
# 1. File existence checks
# 2. Import node classes from pipo_nodes_integrated
# 3. Import server endpoints (CRITICAL!)
from . import pipo_nodes_server  # Must be imported to register routes

# 4. Export mappings
NODE_CLASS_MAPPINGS = {...}
NODE_DISPLAY_NAME_MAPPINGS = {...}
WEB_DIRECTORY = "./web"
```

**Common Issue:** Forgetting to import `pipo_nodes_server` prevents API routes from registering.

---

## 🔄 State Management

### Persistent State Pattern

Several nodes maintain persistent state across ComfyUI sessions using JSON files:

#### MF Story Driver (`story_driver_state.json`)

```json
{
  "MyProject": {
    "step": 5,
    "seed": 12345678901234567890
  },
  "AnotherProject": {
    "step": 0,
    "seed": 98765432109876543210
  }
}
```

**State Management:**
```python
class MF_StoryDriver:
    _state_file = "story_driver_state.json"
    _state = {}

    @classmethod
    def _load_state(cls):
        if os.path.exists(cls._state_file):
            with open(cls._state_file, "r") as f:
                cls._state = json.load(f)

    @classmethod
    def _save_state(cls):
        with open(cls._state_file, "w") as f:
            json.dump(cls._state, f, indent=2)
```

#### MF Graph Plotter (`graph_plotter_state.json`)

```json
{
  "node_123": {
    "x_data": [0, 1, 2, 3],
    "y_data": [10, 15, 8, 20]
  }
}
```

**Key stored per node ID** to support multiple independent graph plotters.

### State Best Practices

1. **Load state at class level** (not in `__init__`)
2. **Save after every mutation** to prevent data loss
3. **Use unique identifiers** (project names, node IDs) as keys
4. **Graceful fallback** if state file doesn't exist
5. **Pretty print JSON** with `indent=2` for readability

---

## 🎨 Frontend-Backend Communication

### Pattern: Reset Functionality

**Frontend (pipoNodes.js):**
```javascript
nodeType.prototype.resetStory = async function() {
  const projectName = this.widgets.find(w => w.name === 'projectName')?.value

  try {
    const response = await api.fetchApi('/story_driver/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_name: projectName,
        randomize_seed: true
      })
    })

    if (response.ok) {
      const data = await response.json()
      // Update UI with response data
    }
  } catch (error) {
    console.error('Error:', error)
  }
}
```

**Backend (pipo_nodes_server.py):**
```python
@server.PromptServer.instance.routes.post("/api/story_driver/reset")
async def reset_story_driver(request):
    data = await request.json()
    project_name = data.get("project_name", "MyProject")

    MF_StoryDriver.reset_project(project_name, data.get("randomize_seed", True))
    state = MF_StoryDriver._state.get(project_name, {"step": 0, "seed": 0})

    return web.json_response({
        "success": True,
        "step": state["step"],
        "seed": state["seed"]
    })
```

### Pattern: Data Visualization

**Chart.js Integration:**

1. **Load Chart.js** via CDN in pipoNodes.js
2. **Create canvas element** as custom widget
3. **Update graph on execution** via `onExecuted` hook
4. **Save as PNG** using canvas.toDataURL()

```javascript
// Create canvas widget
this.addCustomWidget({
  name: "graph_canvas",
  type: "canvas",
  draw: function(ctx, node, width, y) {
    // Chart.js rendering
  }
})
```

---

## 🛠️ Development Guidelines

### Adding a New Node

**Step 1: Define Node Class** (pipo_nodes_integrated.py)

```python
class MF_NewNode:
    CATEGORY = "MF_PipoNodes/YourCategory"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_name": ("TYPE", {"default": value}),
            }
        }

    RETURN_TYPES = ("OUTPUT_TYPE",)
    RETURN_NAMES = ("output_name",)
    FUNCTION = "process"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def process(self, input_name):
        result = # ... your logic
        print(f"🔧 [MF_NewNode] {result}")
        return (result,)
```

**Step 2: Register Node** (__init__.py)

```python
NODE_CLASS_MAPPINGS = {
    "MF_NewNode": MF_NewNode,
    # ... other nodes
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_NewNode": "🔧 MF New Node",
    # ... other display names
}
```

**Step 3: Add Frontend Logic** (web/pipoNodes.js) *(if needed)*

```javascript
if (nodeData.name === "MF_NewNode") {
  const onNodeCreated = nodeType.prototype.onNodeCreated
  nodeType.prototype.onNodeCreated = function() {
    onNodeCreated?.apply(this, arguments)

    // Add custom widgets, buttons, or displays
  }
}
```

**Step 4: Add API Endpoints** (pipo_nodes_server.py) *(if needed)*

```python
@server.PromptServer.instance.routes.post("/api/new_node/action")
async def new_node_action(request):
    # Handle request
    return web.json_response({"success": True})
```

**Step 5: Update Documentation**
- Add node to README.md
- Update CHANGELOG.md with version bump
- Add usage examples

### Code Conventions

#### Python Style
- **PEP 8** compliance
- **Type hints** where appropriate
- **Docstrings** for all public methods
- **Console logging** with emoji prefixes: `print(f"✨ [NodeName] Message")`

#### JavaScript Style
- **JavaScript Standard Style**
- **Async/await** for API calls
- **Error handling** with try/catch
- **Console logging** for debugging

#### Naming Conventions
- **Classes:** `MF_PascalCase`
- **Functions:** `snake_case`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private methods:** `_leading_underscore`
- **Node display names:** Emoji prefix (e.g., "🎲 MF Dice Roller")

### Testing Checklist

Before submitting changes:

- [ ] Node appears in ComfyUI node menu
- [ ] All inputs/outputs work as expected
- [ ] State persists across restarts (if applicable)
- [ ] API endpoints respond correctly (if applicable)
- [ ] Console shows expected log messages
- [ ] No JavaScript errors in browser console (F12)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

---

## 🐛 Common Issues & Solutions

### Issue: Routes Return 405 Method Not Allowed

**Cause:** Missing `/api/` prefix in route decorator

**Solution:**
```python
# ❌ Wrong
@server.PromptServer.instance.routes.post("/story_driver/reset")

# ✅ Correct
@server.PromptServer.instance.routes.post("/api/story_driver/reset")
```

### Issue: Routes Never Register

**Cause:** `pipo_nodes_server.py` not imported in `__init__.py`

**Solution:**
```python
# In __init__.py
try:
    from . import pipo_nodes_server  # Must import to register routes
    print("[MF_PipoNodes] ✅ Server endpoints loaded")
except Exception as e:
    print(f"[MF_PipoNodes] ⚠️ Could not load server: {e}")
```

### Issue: Node Doesn't Re-execute

**Cause:** Missing `IS_CHANGED` method or `OUTPUT_NODE` flag

**Solution:**
```python
OUTPUT_NODE = True

@classmethod
def IS_CHANGED(cls, **kwargs):
    return float("nan")  # Forces re-execution every time
```

### Issue: State Not Persisting

**Cause:** Not saving state after mutations

**Solution:**
```python
# After modifying state
cls._state[key] = value
cls._save_state()  # Don't forget this!
```

### Issue: Widget Not Updating

**Cause:** Not using `onExecuted` hook to update UI

**Solution:**
```javascript
nodeType.prototype.onExecuted = function(message) {
  onExecuted?.apply(this, arguments)

  const widget = this.widgets?.find(w => w.name === 'status_display')
  if (widget && message.status_display?.[0]) {
    widget.value = message.status_display[0]
  }
}
```

---

## 📊 Node Categories & Purpose

| Category | Nodes | Purpose |
|----------|-------|---------|
| **Random** | MF Dice Roller | Random number generation with dice simulation |
| **Utilities** | MF Line Counter, MF Line Select | Text processing and list manipulation |
| **Logging** | MF Log File, MF Log Reader | File-based logging with timestamps |
| **Math** | MF Modulo, MF Modulo Advanced | Mathematical operations with cycle tracking |
| **Sequencing** | MF Shot Helper, MF Story Driver | Sequential processing and project management |
| **Visualization** | MF Graph Plotter | Interactive data visualization with Chart.js |
| **Data** | MF Save Data, MF Read Data, MF Show Data | Multi-format data I/O and display |

---

## 🔗 Dependencies

### Python (requirements.txt)
```
PyYAML>=6.0.1  # For YAML file support
```

### JavaScript (CDN)
- **Chart.js 3.9.1** - Loaded dynamically from CDN for graph visualization

### ComfyUI Integration
- Uses ComfyUI's folder_paths module
- Integrates with ComfyUI's PromptServer
- Extends app via extension system

---

## 🚀 Workflow Integration Patterns

### Pattern 1: Sequential Processing
```
MF Story Driver → step_int → Processing Logic
              ↓
         storySeed → KSampler (consistent results)
```

### Pattern 2: Cyclic Operations
```
Counter → MF Modulo Advanced → MF Line Select
                            ↓
                    Infinite prompt cycling
```

### Pattern 3: Data Visualization
```
Parameter Sweep → X/Y Values → MF Graph Plotter
                                      ↓
                            Visual analysis + PNG export
```

### Pattern 4: Persistent Logging
```
LLM Output → MF Log File → Timestamped history
                 ↓
         MF Log Reader → Context for next LLM call
```

---

## 📝 Version History

- **v1.5.2** - Fixed custom dropdown persistence
- **v1.4.0** - Added data I/O nodes (Save/Read/Show Data)
- **v1.3.0** - Added Graph Plotter and Story Driver
- **v1.2.0** - Added Shot Helper, improved modulo
- **v1.1.0** - Added advanced modulo with cycle tracking
- **v1.0.0** - Initial release with 8 core nodes

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

**Quick Guidelines:**
- Follow existing code patterns
- Add comprehensive docstrings
- Update documentation
- Test thoroughly
- One feature per PR

---

## 📚 Additional Resources

- **Main Documentation:** [README.md](readme.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Contributing Guide:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **License:** [LICENSE.md](LICENSE.md)
- **Authors:** [AUTHORS.md](AUTHORS.md)

---

## 💡 AI Assistant Notes

When working on this project:

1. **Always check** if routes have `/api/` prefix
2. **Always import** `pipo_nodes_server` in `__init__.py`
3. **Always save state** after mutations
4. **Always add** `IS_CHANGED` returning `float("nan")` for dynamic nodes
5. **Always test** in a real ComfyUI environment
6. **Always update** documentation when adding features
7. **Use emojis** in console logs for visual identification
8. **Follow patterns** established in existing nodes

---

**Made with ❤️ for the ComfyUI Community**
