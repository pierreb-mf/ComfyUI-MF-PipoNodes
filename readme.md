# MF PipoNodes

Utility nodes for ComfyUI workflows: randomization, text processing, logging, sequencing, and math operations.

![Version](https://img.shields.io/badge/version-1.2.0-blue)
![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-green)

## Nodes Included

### 🎲 Randomization
- **MF Dice Roller** - Simulate dice rolls (D4, D6, D8, D10, D12, D20, D100)

### 📝 Text Utilities
- **MF Line Counter** - Count lines in multi-line text
- **MF Line Select** - Extract specific lines by index

### 📋 Logging
- **MF Log File** - Write timestamped log entries
- **MF Log Reader** - Read log file contents

### 🔢 Math Operations
- **MF Modulo** - Basic modulo with visual feedback
- **MF Modulo Advanced** - Modulo with cycle tracking

### 🎬 Sequencing
- **MF Shot Helper** - Generate sequence and shot numbers based on beat points

## Installation

### ComfyUI Manager (Easiest)
1. Search for "MF PipoNodes" in ComfyUI Manager
2. Install and restart

### Manual
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/YOUR_USERNAME/ComfyUI-MF-PipoNodes.git
```
Restart ComfyUI.

## Quick Reference

### 🎲 MF Dice Roller
**Inputs:** Dice type (D4-D100)  
**Outputs:** Result as INT and STRING  
**Use for:** Random seeds, conditional branching

---

### 📝 MF Line Counter
**Inputs:** Multi-line text  
**Outputs:** Line count as INT and STRING  
**Use for:** List validation, loop control

---

### 📝 MF Line Select
**Inputs:** Text + line index (0-based)  
**Outputs:** Selected line  
**Use for:** Cycling through prompts, processing lists

---

### 📋 MF Log File
**Inputs:** 
- `log_entry` (required)
- `save_log_path` (optional, defaults to output dir)
- `log_file_name` (optional, defaults to "logfile")

**Outputs:** Full log contents  
**Use for:** Tracking generations, debugging, audit trails

---

### 📋 MF Log Reader
**Inputs:** 
- `log_file_path` (optional)
- `log_file_name` (optional)

**Outputs:** Log file contents  
**Use for:** Reading workflow history, feeding context to LLMs

---

### 🔢 MF Modulo
**Inputs:** Input number + modulo value  
**Outputs:** Result as INT and STRING  
**Use for:** List cycling, pattern generation

---

### 🔢 MF Modulo Advanced
**Inputs:** Input number + modulo value + reset option  
**Outputs:** Modulo result + cycle count (both INT and STRING)  
**Use for:** Batch rendering, tracking progress through iterations

---

### 🎬 MF Shot Helper
**Inputs:**
- `step` (INT, required) - Current frame/step number
- `beats` (STRING, required) - Beat points marking sequence boundaries

**Outputs:**
- `sequence_int` - Current sequence number
- `sequence_str` - Sequence as string
- `shot_int` - Shot number within current sequence
- `shot_str` - Shot as string
- `shot_name` - Formatted name (e.g., "seq01_shot03")

**Beat Format:** Accepts comma-separated (`3,8,15`), newline-separated, or array format (`[3,8,15]`)

**Use for:** Organizing video/animation sequences, shot naming, render organization

**How it works:** 
- Sequence 1 runs from step 0 until the first beat
- At each beat point, a new sequence begins and shot counter resets to 1
- Perfect for dividing long animations into manageable sequences

**Example:**
```
Step 0-2:  seq01_shot01, seq01_shot02, seq01_shot03
Beat at 3
Step 3-7:  seq02_shot01, seq02_shot02, seq02_shot03, seq02_shot04, seq02_shot05
Beat at 8
Step 8+:   seq03_shot01, seq03_shot02...
```

## Example Workflows

### Cycle Through Prompts During Batch Rendering
```
Counter → MF Modulo Advanced (mod 5) → MF Line Select → Your 5 prompts
                    ↓
            Cycle count tracks progress
```
Perfect for batch rendering where you want to loop through a list of prompts infinitely.

---

### Give LLMs Memory of Previous Generations
```
LLM Output → MF Log File → Stores history
MF Log Reader → Concatenate with new prompt → LLM Input
```
Your LLM maintains context across multiple generations.

---

### Random Prompt Selection
```
MF Dice Roller (D6) → MF Line Select → Pick from 6 options
```
Each execution picks a random line from your list.

---

### Track Batch Progress
```
Counter → MF Modulo Advanced → Shows position + cycles completed
       → MF Log File → Logs progress with timestamps
```

---

### Organize Animation Sequences by Beat Points
```
Frame Counter → MF Shot Helper (beats: "120,240,360")
                      ↓
            "seq01_shot01" through "seq01_shot120" (frames 0-119)
            "seq02_shot01" through "seq02_shot120" (frames 120-239)
            "seq03_shot01" through "seq03_shot120" (frames 240-359)
            "seq04_shot..." (frames 360+)
```
Automatically organize long animations into sequences based on musical beats or scene changes.

---

### Dynamic Shot Naming for Video Projects
```
Frame Number → MF Shot Helper → shot_name output
                     ↓
        Use in filename: "{shot_name}_render.png"
        Results: "seq01_shot01_render.png", "seq01_shot02_render.png"...
                 "seq02_shot01_render.png", "seq02_shot02_render.png"...
```
Perfect for organizing thousands of frames into logical shot groups.

---

### Combine Shot Helper with Prompt Switching
```
Frame Counter → MF Shot Helper → sequence_int
                      ↓
              MF Line Select (using sequence_int as index)
                      ↓
              Different prompt for each sequence!
```
Automatically switch prompts when crossing sequence boundaries.

## Key Features

**Smart Execution:** Nodes with randomization or logging re-execute every queue for fresh results.

**Universal Line Breaks:** Handles `\n`, `\r\n`, and `\r` formats automatically.

**Live Visual Feedback:** See dice rolls, calculations, log contents, and sequence/shot info directly in the node.

**Zero-Based Indexing:** Line 0 is the first line in text processing nodes.

**Flexible Beat Format:** Shot Helper accepts multiple formats for beat points (comma, newline, array).

**Professional Shot Naming:** Generates industry-standard sequence/shot naming conventions.

## Troubleshooting

**Nodes missing?** 
- Check `ComfyUI/custom_nodes/ComfyUI-MF-PipoNodes/` exists
- Verify `web/pipoNodes.js` is present
- Restart ComfyUI completely

**Display not updating?** 
- Queue the workflow to trigger execution
- Check browser console for JavaScript errors

**Log file not found?** 
- Run MF Log File first to create the file
- Verify paths match between writer and reader nodes

**Shot Helper not incrementing sequences?**
- Verify beat points are in ascending order
- Check that beats string is properly formatted
- Beat points mark the START of each new sequence

## Tips

- **Batch Rendering:** Use Modulo Advanced + Line Select to cycle through prompts
- **LLM Context:** Log outputs and read them back to maintain conversation history
- **List Safety:** Count lines before selecting to avoid index errors
- **Cycle Tracking:** Modulo Advanced shows how many complete loops you've done
- **Video Organization:** Use Shot Helper to automatically organize renders into sequences
- **Musical Timing:** Set beat points at frame numbers matching music beats for synchronized animations
- **Prompt Switching:** Combine Shot Helper's sequence output with Line Select for automatic prompt changes

## Technical Details

**Author:** Pierre Biet | Moment Factory  
**Version:** 1.2.0  
**Year:** 2025  
**License:** MIT

All nodes consolidated into single files for easy maintenance:
- `__init__.py` - All Python logic
- `web/pipoNodes.js` - All frontend extensions

## Contributing

Pull requests welcome! Fork, create a feature branch, and submit.

## Support

- Open issues on GitHub
- Check existing issues first
- Join ComfyUI Discord community

---

Made with ❤️ by Pierre Biet @ Moment Factory