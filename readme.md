# MF PipoNodes

Utility nodes for ComfyUI workflows: randomization, text processing, logging, and math operations.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
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

## Example Workflows

### Cycle Through Prompts During Batch Rendering
```
Counter → MF Modulo Advanced (mod 5) → MF Line Select → Your 5 prompts
                    ↓
            Cycle count tracks progress
```
Perfect for batch rendering where you want to loop through a list of prompts infinitely.

### Give LLMs Memory of Previous Generations
```
LLM Output → MF Log File → Stores history
MF Log Reader → Concatenate with new prompt → LLM Input
```
Your LLM maintains context across multiple generations.

### Random Prompt Selection
```
MF Dice Roller (D6) → MF Line Select → Pick from 6 options
```
Each execution picks a random line from your list.

### Track Batch Progress
```
Counter → MF Modulo Advanced → Shows position + cycles completed
       → MF Log File → Logs progress with timestamps
```

## Key Features

**Smart Execution:** Nodes with randomization or logging re-execute every queue for fresh results.

**Universal Line Breaks:** Handles `\n`, `\r\n`, and `\r` formats automatically.

**Live Visual Feedback:** See dice rolls, calculations, and log contents directly in the node.

**Zero-Based Indexing:** Line 0 is the first line in text processing nodes.

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

## Tips

- **Batch Rendering:** Use Modulo Advanced + Line Select to cycle through prompts
- **LLM Context:** Log outputs and read them back to maintain conversation history
- **List Safety:** Count lines before selecting to avoid index errors
- **Cycle Tracking:** Modulo Advanced shows how many complete loops you've done

## Technical Details

**Author:** Pierre Biet | Moment Factory  
**Version:** 1.0.0  
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