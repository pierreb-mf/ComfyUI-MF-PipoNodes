# MF PipoNodes - ComfyUI Custom Nodes

**A comprehensive collection of utility and quality-of-life nodes for ComfyUI workflows**

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://github.com/pierreb-mf/ComfyUI-MF-PipoNodes)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-orange.svg)](https://github.com/comfyanonymous/ComfyUI)

---

## 📋 Overview

MF PipoNodes provides 10 specialized nodes for ComfyUI covering:
- 🎲 **Randomization** - Dice rolling for seeds and conditional logic
- 📝 **Text Processing** - Line manipulation and extraction
- 📊 **Logging** - File-based logging with timestamps
- 🔢 **Math Operations** - Modulo with cycle tracking
- 🎬 **Sequencing** - Shot helpers and story progression
- 📈 **Visualization** - Interactive graph plotting
- 🌱 **Project Management** - Seed management and step tracking

---

## 🚀 Quick Start

### Installation via ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "MF PipoNodes"
3. Click Install
4. Restart ComfyUI

### Manual Installation
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/pierreb-mf/ComfyUI-MF-PipoNodes.git
```
Then restart ComfyUI.

### Update Existing Installation
```bash
cd ComfyUI/custom_nodes/ComfyUI-MF-PipoNodes/
git pull
```
Then restart ComfyUI.

---

## 📦 Available Nodes

### 🎲 Random Category

#### **MF Dice Roller**
Simulate dice rolls for random number generation.

**Inputs:**
- `dice` (ENUM) - D4, D6, D8, D10, D12, D20, D100

**Outputs:**
- `int` (INT) - Roll result as integer
- `string` (STRING) - Roll result as string

**Use Cases:**
- Random seed generation
- Conditional branching
- Prompt variation

**Example:**
```
MF Dice Roller (D6) → Random value 1-6
↓
Use for seed or Line Select index
```

---

### 🔧 Utilities Category

#### **MF Line Counter**
Count the number of lines in multi-line text.

**Inputs:**
- `text` (STRING, multiline) - Text to count

**Outputs:**
- `line_count_int` (INT) - Line count as integer
- `line_count_str` (STRING) - Line count as string

**Features:**
- Handles all line break formats (\n, \r\n, \r)
- Counts empty lines
- Returns 0 for empty input

**Use Cases:**
- List validation before processing
- Loop control
- Workflow logic

---

#### **MF Line Select**
Extract a specific line from multi-line text by index (0-based).

**Inputs:**
- `text` (STRING, multiline) - Source text
- `line_index` (INT, 0-1000) - Line to extract (0 = first line)

**Outputs:**
- `selected_line` (STRING) - The extracted line

**Features:**
- Zero-based indexing
- Error handling for out-of-range indices
- Preserves empty lines

**Use Cases:**
- Cycling through prompts
- Processing lists sequentially
- Dynamic text selection

**Example:**
```
Prompts: "forest\nbeach\nmountain\ncity"
Line Index: 2
Output: "mountain"
```

---

### 📝 Logging Category

#### **MF Log File**
Write timestamped entries to a log file.

**Inputs:**
- `log_entry` (STRING, multiline, required) - Content to log
- `save_log_path` (STRING, optional) - Directory (defaults to output dir)
- `log_file_name` (STRING, optional) - Filename (defaults to "logfile.txt")

**Outputs:**
- `log_content` (STRING) - Full log file contents

**Features:**
- Automatic timestamps
- Creates directories if needed
- Appends to existing logs
- Display widget shows full log

**Format:**
```
[2025-10-22 14:30:15] Your log entry here

[2025-10-22 14:32:08] Another entry

```

**Use Cases:**
- Generation tracking
- Debugging workflows
- Audit trails
- LLM conversation history

---

#### **MF Log Reader**
Read the contents of a log file.

**Inputs:**
- `log_file_path` (STRING, optional) - Directory
- `log_file_name` (STRING, optional) - Filename

**Outputs:**
- `log_content` (STRING) - File contents

**Use Cases:**
- Reading workflow history
- Feeding context to LLMs
- Reviewing generation logs

---

### 🔢 Math Category

#### **MF Modulo**
Basic modulo operation with visual feedback.

**Inputs:**
- `input_number` (INT) - Number to process
- `modulo_value` (INT, min 1) - Divisor

**Outputs:**
- `result_int` (INT) - Modulo result
- `result_str` (STRING) - Result as string

**Example:**
```
Input: 7, Modulo: 3 → Output: 1
Input: 9, Modulo: 3 → Output: 0
```

**Use Cases:**
- List cycling
- Pattern generation
- Periodic triggers

---

#### **MF Modulo Advanced**
Enhanced modulo with cycle tracking.

**Inputs:**
- `input_number` (INT) - Number to process
- `modulo_value` (INT, min 1) - Divisor
- `reset_cycle` (BOOLEAN) - Reset cycle counter

**Outputs:**
- `result_int` (INT) - Modulo result
- `result_str` (STRING) - Result as string
- `cycle_int` (INT) - Complete cycles
- `cycle_str` (STRING) - Cycles as string

**Example:**
```
Steps 0-4, Mod 5: Cycle 0, Results 0-4
Steps 5-9, Mod 5: Cycle 1, Results 0-4
Steps 10-14, Mod 5: Cycle 2, Results 0-4
```

**Use Cases:**
- Batch rendering with progress tracking
- Multi-pass workflows
- Iteration counting

---

### 🎬 Sequencing Category

#### **MF Shot Helper**
Organize frames/steps into sequences and shots based on beat points.

**Inputs:**
- `step` (INT, required) - Current frame/step number
- `beats` (STRING, required) - Beat points marking sequence boundaries

**Outputs:**
- `sequence_int` (INT) - Current sequence number
- `sequence_str` (STRING) - Sequence as string
- `shot_int` (INT) - Shot number within sequence
- `shot_str` (STRING) - Shot as string
- `shot_name` (STRING) - Formatted name (e.g., "seq01_shot03")

**Beat Formats Supported:**
```
Comma-separated: "3,8,15,25"
Newline-separated: "3\n8\n15\n25"
Array format: "[3,8,15,25]"
```

**How It Works:**
- Sequence 1: Steps 0 until first beat
- At each beat: New sequence starts, shot resets to 1
- Perfect for dividing long animations into logical segments

**Example:**
```
Beats: "120,240,360"

Frames 0-119:   seq01_shot001 through seq01_shot120
Frames 120-239: seq02_shot001 through seq02_shot120
Frames 240-359: seq03_shot001 through seq03_shot120
Frames 360+:    seq04_shot001 through seq04_shot...
```

**Use Cases:**
- Video/animation organization
- Musical synchronization
- Scene-based rendering
- Automatic file naming

---

#### **MF Story Driver** ⭐ *NEW in v1.3.0*
Project-based step sequencing with persistent seed management.

**Inputs:**
- `projectName` (STRING) - Project identifier
- `randomize_seed_on_reset` (BOOLEAN) - Whether to change seed on reset

**Outputs:**
- `step_int` (INT) - Current step number (auto-increments)
- `step_str` (STRING) - Step as string
- `projectName` (STRING) - Sanitized name (spaces → underscores)
- `saveFolder` (STRING) - Formatted folder name (`projectName_seed`)
- `storySeed` (INT) - Project's persistent seed

**Features:**
- ✨ **Persistent State:** State saved per project across sessions
- 🔢 **Auto-Increment:** Steps advance automatically on each execution
- 🌱 **Seed Management:** Consistent seeds per project
- 🔄 **Reset Button:** Reset step counter and optionally randomize seed
- 📁 **Folder Naming:** Generates organized output paths

**UI Elements:**
- Status display: `Step: X | Seed: Y`
- 🔄 Reset Story button

**Example Workflow:**
```
MF Story Driver (projectName: "MyStory")
├─ Step 0, Seed: 12345678901234567890
├─ Outputs:
│  ├─ step_int: 0
│  ├─ projectName: "MyStory"
│  ├─ saveFolder: "MyStory_12345678901234567890"
│  └─ storySeed: 12345678901234567890
│
Next execution:
├─ Step 1, Same seed
│
After reset (randomize ON):
└─ Step 0, New seed: 98765432109876543210
```

**Use Cases:**
1. **Sequential Image Generation**
   ```
   Story Driver → storySeed → KSampler
   ↓
   Consistent seed across all story steps
   ```

2. **Batch Rendering with Tracking**
   ```
   Story Driver → step_int → Filename
   ↓
   Automatic numbering: "MyStory_001.png", "MyStory_002.png"...
   ```

3. **Multi-Shot Story Development**
   ```
   Story Driver → step_int → Line Select → Different prompts per step
   ↓
   Each story beat uses different prompt
   ```

4. **Organized Output Structure**
   ```
   Story Driver → saveFolder → Save Image path
   ↓
   All renders go to "MyStory_12345/image_001.png"
   ```

**State Persistence:**
- State saved in `story_driver_state.json` (automatically created)
- Each project tracked independently
- Survives ComfyUI restarts

---

### 📈 Visualization Category

#### **MF Graph Plotter** ⭐ *NEW in v1.3.0*
Interactive X/Y data plotter with Chart.js visualization.

**Inputs:**
- `X` (INT) - X coordinate
- `Y` (INT) - Y coordinate

**Outputs:**
- `X` (INT) - Pass-through X value
- `Y` (INT) - Pass-through Y value

**Features:**
- 📊 **Live Visualization:** Real-time Chart.js graph
- 💾 **Save to PNG:** Export graph image
- 🔄 **Reset Per Node:** Clear data for each node independently
- 📈 **Smooth Curves:** Interpolated line rendering
- 🎯 **Interactive Tooltips:** Hover to see exact X/Y values
- 💾 **Persistent State:** Data preserved across sessions

**UI Elements:**
- Interactive canvas (400x300px)
- 🔄 Reset Graph button
- 💾 Save Graph button
- Tooltip on hover showing coordinates

**Graph Styling:**
- Yellow (#FFEC00) line with subtle fill
- Minimal axis labels (Y label only)
- Black axis borders
- Grid lines for reference
- Smooth curve interpolation

**Example Workflow:**
```
Loop Counter (0-10)
├─ X coordinate
├─ Some Calculation → Y coordinate
└─ MF Graph Plotter → Visual plot
```

**Use Cases:**
1. **Parameter Relationship Visualization**
   ```
   CFG Scale → X
   Quality Score → Y
   Plot to find optimal CFG value
   ```

2. **Workflow Progression Tracking**
   ```
   Step Number → X
   Loss Value → Y
   Monitor training progress
   ```

3. **Data Analysis**
   ```
   Prompt Variation Index → X
   Image Similarity Score → Y
   Visualize prompt effectiveness
   ```

4. **Real-time Monitoring**
   ```
   Time Step → X
   Memory Usage → Y
   Track resource consumption
   ```

**State Management:**
- Data stored per node ID in `graph_plotter_state.json`
- Each Graph Plotter node maintains independent data
- State survives ComfyUI restarts
- Reset button clears data for that specific node only

**Saving Graphs:**
1. Click 💾 Save Graph button
2. Choose save location via file dialog
3. Graph exported as PNG image

---

## 🎯 Common Workflow Patterns

### Pattern 1: Infinite Prompt Cycling
```
Counter → MF Modulo Advanced (mod 5) → MF Line Select
                ↓                              ↓
         Tracks cycles              Cycles through 5 prompts
                ↓
         Your prompt list (5 items)
```
Perfect for batch rendering that loops through prompts indefinitely.

---

### Pattern 2: LLM Context Accumulation
```
LLM Output → MF Log File → Stores conversation history
                ↓
     MF Log Reader → Concatenate with new prompt
                ↓
         LLM Input (with full context)
```
Maintains conversation history across multiple LLM generations.

---

### Pattern 3: Random Selection
```
MF Dice Roller (D6) → MF Line Select → Picks random line
                              ↓
                 Your list of 6 options
```
Each execution randomly selects from your list.

---

### Pattern 4: Progress Tracking with Logging
```
Counter → MF Modulo Advanced → Position + Cycles
            ↓
    MF Log File → Logs progress with timestamps
```
Track exactly where you are in long batch processes.

---

### Pattern 5: Video Sequence Organization
```
Frame Counter → MF Shot Helper (beats: "120,240,360")
                       ↓
    Automatic sequence/shot naming:
    - Frames 0-119: seq01_shot001-120
    - Frames 120-239: seq02_shot001-120
    - Frames 240-359: seq03_shot001-120
                       ↓
    Use shot_name in filename → Organized output
```
Perfect for long animations divided into sequences.

---

### Pattern 6: Sequence-Based Prompt Switching
```
Frame Counter → MF Shot Helper → sequence_int
                       ↓
              MF Line Select (using sequence_int)
                       ↓
         Different prompt for each sequence
```
Automatically switch prompts when crossing sequence boundaries.

---

### Pattern 7: Story-Driven Generation ⭐ *NEW*
```
MF Story Driver (projectName: "MyStory")
├─ step_int → Image naming/numbering
├─ storySeed → KSampler seed (consistent across story)
├─ saveFolder → Output directory organization
└─ projectName → Metadata/tagging
```
Perfect for sequential storytelling with consistent style.

---

### Pattern 8: Parameter Sweep with Visualization ⭐ *NEW*
```
Loop: CFG Scale 1-10
├─ CFG Value → X coordinate
├─ Image Quality Metric → Y coordinate
└─ MF Graph Plotter → Visual results
```
Visualize how parameters affect output quality.

---

### Pattern 9: Multi-Project Workflow ⭐ *NEW*
```
Project Selector → MF Story Driver (projectName input)
                         ↓
         Multiple projects tracked independently
         - "Character_Study": Step 25, Seed: 123...
         - "Environment_Test": Step 10, Seed: 456...
         - "Style_Exploration": Step 5, Seed: 789...
```
Manage multiple concurrent projects with independent progression.

---

## 🎨 Node Categories in ComfyUI

All nodes are organized under `MF_PipoNodes/`:
- **Random** - Dice Roller
- **Utilities** - Line Counter, Line Select
- **Logging** - Log File, Log Reader
- **Math** - Modulo, Modulo Advanced
- **Sequencing** - Shot Helper, Story Driver
- **Visualization** - Graph Plotter

---

## 💡 Key Features

### Smart Execution
Nodes with randomization (Dice Roller, Story Driver) or logging automatically re-execute on every queue for fresh results.

### Universal Line Break Handling
All text-processing nodes automatically handle `\n`, `\r\n`, and `\r` line break formats.

### Live Visual Feedback
- Dice rolls appear directly in node
- Logs display in real-time
- Calculations show immediately
- Graphs update live
- Status displays for story progression

### Zero-Based Indexing
Line 0 is the first line in all text processing nodes.

### Flexible Input Formats
- Shot Helper accepts multiple beat formats
- Text inputs handle various line endings
- State management uses human-readable JSON

### Professional Naming
- Shot Helper generates industry-standard sequence/shot names
- Story Driver creates organized folder structures
- Consistent formatting across all outputs

### State Persistence
- Graph Plotter data survives restarts
- Story Driver projects tracked across sessions
- Automatic state file management

---

## 🔧 Technical Details

### File Structure
```
ComfyUI-MF-PipoNodes/
├── __init__.py                      # Node registration and diagnostics
├── pipo_nodes_integrated.py         # All node implementations
├── pipo_nodes_server.py             # API endpoints
├── graph_plotter_state.json         # Graph data (auto-generated)
├── story_driver_state.json          # Story state (auto-generated)
├── web/
│   └── pipoNodes.js                 # Frontend extensions
└── README.md
```

### Dependencies
- **Core:** ComfyUI (no additional Python packages)
- **Frontend:** Chart.js 4.4.0 (loaded from CDN)
- **Compatible:** All ComfyUI versions

### State Files
State files are automatically created in the node directory:
- `graph_plotter_state.json` - Per-node graph data
- `story_driver_state.json` - Per-project story state

These files are **not tracked in git** (see .gitignore).

### API Endpoints
The extension provides REST API endpoints for interactive features:
- `POST /graph_plotter/reset` - Reset graph data
- `POST /graph_plotter/save_image` - Save graph as PNG
- `POST /story_driver/reset` - Reset story project

---

## 🐛 Troubleshooting

### Nodes Not Appearing
1. Check that `ComfyUI/custom_nodes/ComfyUI-MF-PipoNodes/` exists
2. Verify `web/pipoNodes.js` is present
3. Restart ComfyUI completely
4. Check console for errors during startup

### Display Not Updating
1. Queue the workflow to trigger execution
2. Check browser console (F12) for JavaScript errors
3. Verify Chart.js loaded (check console for "📊 Chart.js loaded")

### Log File Not Found
1. Run MF Log File node first to create the file
2. Verify file paths match between writer and reader
3. Check that output directory is writable

### Graph Not Resetting
1. Ensure you clicked the 🔄 Reset Graph button
2. Check browser console for API errors
3. Verify node ID is correctly identified

### Story Not Incrementing
1. Verify projectName is unique per project
2. Check that state file is writable
3. Ensure node is actually executing (not cached)

### Shot Helper Not Incrementing Sequences
1. Verify beat points are in ascending order
2. Check beat string formatting
3. Remember: beats mark the START of each new sequence

---

## 📚 Best Practices

### For Batch Rendering
- Use **Modulo Advanced** + **Line Select** to cycle through prompts
- Enable cycle tracking to know your progress
- Combine with **Log File** to record each generation

### For LLM Workflows
- Store **all** LLM interactions in Log File
- Use **Log Reader** to feed context back
- Timestamp tracking helps debugging

### For List Processing
- Always **count lines** before selecting
- Use modulo to safely cycle through lists
- Handle edge cases with error checking

### For Animation Workflows
- Use **Shot Helper** for frame organization
- Set beats at musically significant points
- Leverage automatic shot naming for rendering

### For Story Generation
- Use **Story Driver** for consistent seeds per project
- Reset between stories, not between steps
- Leverage saveFolder for automatic organization
- Track multiple projects simultaneously

### For Data Analysis
- Use **Graph Plotter** for visual parameter sweeps
- Save graphs before resetting for record-keeping
- Plot relationships between generation parameters

---

## 🎓 Learning Resources

### Example Workflows
Check the [examples](examples/) directory for:
- Prompt cycling templates
- LLM context management
- Animation sequence setups
- Story-driven generation patterns
- Parameter visualization workflows

### Video Tutorials
- Coming soon!

### Community Projects
Share your workflows using MF PipoNodes:
- Tag us in discussions
- Submit pull requests with examples
- Join our Discord community

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. Create a **feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

### Development Guidelines
- Follow existing code style
- Add comments for complex logic
- Update README for new features
- Test thoroughly in ComfyUI

---

## 📝 Changelog

### v1.3.0 (2025-10-22)
**New Features:**
- ⭐ **MF Graph Plotter** - Interactive data visualization with Chart.js
- ⭐ **MF Story Driver** - Project-based step sequencing with seed management

**Technical:**
- Refactored codebase into modular files
- Added API endpoints for reset/save functionality
- Implemented JSON state persistence
- Enhanced initialization with diagnostics
- Improved error handling and logging

**Files:**
- Added `pipo_nodes_integrated.py` for all node logic
- Added `pipo_nodes_server.py` for API routes
- Enhanced `__init__.py` with better diagnostics
- Updated `web/pipoNodes.js` with new node support

### v1.2.0 (2025-01-15)
- Added MF Shot Helper
- Improved modulo operations
- Enhanced logging features

### v1.1.0 (2024-12-01)
- Added advanced modulo with cycle tracking
- Improved text processing
- Bug fixes and optimizations

### v1.0.0 (2024-11-01)
- Initial release
- 8 core nodes

---

## 📞 Support

### Report Issues
- **GitHub Issues:** https://github.com/pierreb-mf/ComfyUI-MF-PipoNodes/issues
- Check existing issues before creating new ones
- Provide ComfyUI version and error logs

### Discussions
- **GitHub Discussions:** https://github.com/pierreb-mf/ComfyUI-MF-PipoNodes/discussions
- Feature requests welcome
- Share workflow ideas

### Community
- **ComfyUI Discord:** Join the official server
- **Tag:** @pierreb-mf for MF PipoNodes questions

---

## 📜 License

**MIT License**

Copyright (c) 2025 Pierre Biet | Moment Factory

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👤 Author

**Pierre Biet**  
Moment Factory  
2025

---

## 🙏 Acknowledgments

- ComfyUI community for feedback and inspiration
- Chart.js team for the excellent visualization library
- All contributors and users of MF PipoNodes

---

## 🔗 Links

- **GitHub Repository:** https://github.com/pierreb-mf/ComfyUI-MF-PipoNodes
- **ComfyUI:** https://github.com/comfyanonymous/ComfyUI
- **Moment Factory:** https://momentfactory.com

---

**Made with ❤️ for the ComfyUI Community**
