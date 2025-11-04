# ----------------------------------------------------------------------------
# [MF PipoNodes]
# ----------------------------------------------------------------------------
# Author: Pierre Biet | Moment Factory | 2025
# 
# Description: Collection of utility nodes for ComfyUI workflows
# Version: 1.5.2 (Fixed Custom Dropdown Menu persistence - moved dropdown_options from hidden to required)
# --

import random
import os
import datetime
import json
import folder_paths
import csv
import yaml
import xml.etree.ElementTree as ET
from io import StringIO


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_log_file_path(save_log_path, log_file_name, output_dir):
    """Helper to normalize log file path and name."""
    if save_log_path is None or save_log_path.strip() == "":
        save_log_path = output_dir
    
    if log_file_name is None or log_file_name.strip() == "":
        log_file_name = "logfile"
    
    if not log_file_name.lower().endswith(".txt"):
        log_file_name += ".txt"
    
    return os.path.join(save_log_path, log_file_name)


def _normalize_text_lines(text):
    """Normalize line endings and split text into lines."""
    return text.replace('\r\n', '\n').replace('\r', '\n').split('\n')


# ============================================================================
# DICE ROLLER
# ============================================================================

class MF_DiceRoller:
    """
    A ComfyUI node that simulates dice rolling with various dice types.
    Outputs both integer and string representations of the roll result.
    """
    
    CATEGORY = "MF_PipoNodes/Random"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dice": (["D4", "D6", "D8", "D10", "D12", "D20", "D100"], {
                    "default": "D6"
                }),
            },
        }

    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("int", "string",)
    FUNCTION = "roll_dice"
    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def roll_dice(self, dice):
        """Roll the specified dice and return the result."""
        max_value = int(dice[1:])
        result = random.randint(1, max_value)
        
        print(f"🎲 Rolled {dice}: {result}")
        
        text_output = f"🎲 {result}"
        
        return {
            "ui": {
                "text": [text_output],
            },
            "result": (result, str(result),)
        }


# ============================================================================
# LINE COUNTER
# ============================================================================

class MF_LineCounter:
    """
    A ComfyUI node that counts the number of lines in a multiline string input
    and outputs both integer and string representations of the count.
    """
    
    CATEGORY = "MF_PipoNodes/Utilities"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Line 1\nLine 2\nLine 3"
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("line_count_int", "line_count_str")
    FUNCTION = "count_lines"
    
    def count_lines(self, text):
        """Count the number of lines in the input text."""
        if not text.strip():
            return (0, "0")
        
        lines = _normalize_text_lines(text)
        line_count = len(lines)
        
        return (line_count, str(line_count))


# ============================================================================
# LINE SELECT
# ============================================================================

class MF_LineSelect:
    """
    A node that selects a specific line from a text input based on the provided index.
    Every line break is counted, including empty lines.
    """
    
    CATEGORY = "MF_PipoNodes/Utilities"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "line_index": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_line",)
    FUNCTION = "select_line"
    
    def select_line(self, text, line_index):
        """Select a specific line from the input text based on index."""
        lines = _normalize_text_lines(text)
        
        if line_index < 0 or line_index >= len(lines):
            error_msg = f"⚠️ Line index {line_index} out of range (0-{len(lines)-1})"
            print(f"[MF_LineSelect] {error_msg}")
            return (error_msg,)
        
        return (lines[line_index],)


# ============================================================================
# LOG FILE WRITER
# ============================================================================

class MF_LogFile:
    """
    A ComfyUI node that writes timestamped log entries to a text file.
    v1.5.1: Fixed subfolder support by copying MF_SaveData's path handling
    """
    
    CATEGORY = "MF_PipoNodes/Logging"
    
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.last_log_content = ""
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "log_entry": ("STRING", {"multiline": True}),
            },
            "optional": {
                "save_log_path": ("STRING", {"default": "output"}),
                "log_file_name": ("STRING", {"default": "logfile"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log_content",)
    FUNCTION = "write_log"
    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")
    
    def write_log(self, log_entry, save_log_path="output", log_file_name="logfile"):
        """Write a timestamped log entry to file."""
        try:
            # Normalize inputs (same as before)
            if save_log_path is None or save_log_path.strip() == "":
                save_log_path = self.output_dir
            
            if log_file_name is None or log_file_name.strip() == "":
                log_file_name = "logfile"
            
            # Create output directory if it doesn't exist (SAME AS MF_SaveData)
            os.makedirs(save_log_path, exist_ok=True)
            
            # Add .txt extension if needed
            if not log_file_name.lower().endswith(".txt"):
                log_file_name += ".txt"
            
            # Build full filepath (SAME AS MF_SaveData pattern)
            log_file_path = os.path.join(save_log_path, log_file_name)
            
            # Format entry with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_entry = f"[{timestamp}] {log_entry}\n\n"
            
            # Write new entry (append mode to preserve log history)
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(formatted_entry)
            
            # Read entire log for display
            with open(log_file_path, "r", encoding="utf-8") as f:
                self.last_log_content = f.read()
            
            print(f"📝 [MF_LogFile] Wrote entry to {log_file_path}")
            
            return {
                "ui": {
                    "log_display": [self.last_log_content],
                },
                "result": (self.last_log_content,)
            }
            
        except Exception as e:
            error_message = f"❌ Error writing log: {str(e)}"
            print(f"[MF_LogFile] {error_message}")
            return {
                "ui": {
                    "log_display": [error_message],
                },
                "result": (error_message,)
            }


# ============================================================================
# LOG FILE READER
# ============================================================================

class MF_LogReader:
    """
    A ComfyUI node that reads and displays log file content with live updates.
    """
    
    CATEGORY = "MF_PipoNodes/Logging"
    
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "log_file_path": ("STRING", {"default": folder_paths.get_output_directory()}),
                "log_file_name": ("STRING", {"default": "logfile"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log_content",)
    FUNCTION = "read_log"
    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")
    
    def read_log(self, log_file_path=None, log_file_name=None):
        """Read log file content and display it in the node."""
        full_path = _get_log_file_path(log_file_path, log_file_name, self.output_dir)
        
        try:
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                print(f"📖 [MF_LogReader] Read {len(content)} characters from {os.path.basename(full_path)}")
                
                return {
                    "ui": {
                        "log_display": [content],
                    },
                    "result": (content,)
                }
            else:
                error_msg = f"⚠️ Log file not found: {full_path}"
                print(f"[MF_LogReader] {error_msg}")
                return {
                    "ui": {
                        "log_display": [error_msg],
                    },
                    "result": (error_msg,)
                }
        except Exception as e:
            error_message = f"❌ Error reading log file: {str(e)}"
            print(f"[MF_LogReader] {error_message}")
            return {
                "ui": {
                    "log_display": [error_message],
                },
                "result": (error_message,)
            }


# ============================================================================
# MODULO
# ============================================================================

class MF_Modulo:
    """
    A ComfyUI node that applies modulo operation to an integer input
    and displays the result directly in the node.
    """
    
    CATEGORY = "MF_PipoNodes/Math"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_number": ("INT", {
                    "default": 0,
                    "min": -999999,
                    "max": 999999,
                    "step": 1
                }),
                "modulo_value": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 999999,
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("result_int", "result_string")
    FUNCTION = "apply_modulo"
    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")
    
    def apply_modulo(self, input_number, modulo_value):
        """Apply modulo operation to the input number."""
        result = input_number % modulo_value
        text_output = f"🔢 {input_number} mod {modulo_value} = {result}"
        
        print(f"[MF_Modulo] {input_number} mod {modulo_value} = {result}")
        
        return {
            "ui": {
                "text": [text_output],
            },
            "result": (result, str(result))
        }


# ============================================================================
# MODULO ADVANCED
# ============================================================================

class MF_ModuloAdvanced:
    """
    A ComfyUI node that applies modulo operation, tracks cycles,
    and displays both results directly in the node.
    """
    
    CATEGORY = "MF_PipoNodes/Math"
    
    def __init__(self):
        self.cycle_count = 0
        self.last_input = None
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_number": ("INT", {
                    "default": 0,
                    "min": -999999,
                    "max": 999999,
                    "step": 1
                }),
                "modulo_value": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 999999,
                    "step": 1
                }),
            },
            "optional": {
                "reset_cycles": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("INT", "STRING", "INT", "STRING")
    RETURN_NAMES = ("modulo_result_int", "modulo_result_string", "cycle_count_int", "cycle_count_string")
    FUNCTION = "apply_modulo_advanced"
    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")
    
    def apply_modulo_advanced(self, input_number, modulo_value, reset_cycles=False):
        """Apply modulo operation and track cycle count."""
        if reset_cycles:
            self.cycle_count = 0
            self.last_input = None
        
        if self.last_input is not None:
            # Handle large backward jumps (indicates a reset scenario)
            if input_number < self.last_input and (self.last_input - input_number) > modulo_value:
                self.cycle_count = input_number // modulo_value
            else:
                # Track cycle changes incrementally
                cycles_added = (input_number // modulo_value) - (self.last_input // modulo_value)
                self.cycle_count += cycles_added
        else:
            # First run: initialize cycle count
            self.cycle_count = input_number // modulo_value
        
        self.last_input = input_number
        modulo_result = input_number % modulo_value
        
        text_output = f"🔢 {input_number} mod {modulo_value} = {modulo_result}\n🔄 Cycle: {self.cycle_count}"
        
        print(f"[MF_ModuloAdvanced] {input_number} mod {modulo_value} = {modulo_result}, Cycle: {self.cycle_count}")
        
        return {
            "ui": {
                "text": [text_output],
            },
            "result": (
                modulo_result, 
                str(modulo_result), 
                self.cycle_count, 
                str(self.cycle_count)
            )
        }


# ============================================================================
# SHOT HELPER
# ============================================================================

class MF_ShotHelper:
    """
    A ComfyUI node that generates sequence and shot numbers based on a driving primitive
    and beat points. Sequences increment at each beat, and shot counters reset per sequence.
    """
    
    CATEGORY = "MF_PipoNodes/Sequencing"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "step": ("INT", {
                    "default": 0,
                    "forceInput": True
                }),
                "beats": ("STRING", {
                    "default": "",
                    "forceInput": True
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "STRING", "INT", "STRING", "STRING")
    RETURN_NAMES = ("sequence_int", "sequence_str", "shot_int", "shot_str", "shot_name")
    FUNCTION = "calculate_sequence_shot"
    
    def calculate_sequence_shot(self, step, beats):
        """
        Calculate sequence and shot numbers based on current step and beat points.
        
        Args:
            step: Current step number (driving primitive)
            beats: Beat points in various formats:
                   - Comma-separated: "3,8,15"
                   - Newline-separated: "3\\n8\\n15"
                   - Array format: "[3,8,15]"
        
        Returns:
            tuple: (sequence_int, sequence_str, shot_int, shot_str, shot_name)
                   shot_name format: "seq01_shot01"
        """
        # Parse beats string into sorted list of integers
        beat_list = []
        if beats.strip():
            try:
                # Remove array brackets if present
                beats_clean = beats.strip()
                if beats_clean.startswith('[') and beats_clean.endswith(']'):
                    beats_clean = beats_clean[1:-1]
                
                # Replace newlines with commas for unified parsing
                beats_clean = beats_clean.replace('\n', ',')
                
                # Split by comma and parse integers
                beat_list = sorted([int(b.strip()) for b in beats_clean.split(",") if b.strip()])
            except ValueError:
                print(f"⚠️ [MF_ShotHelper] Invalid beats format '{beats}'. Using empty beats.")
                beat_list = []
        
        # Determine which sequence we're in
        sequence_num = 1
        shot_start = 0
        
        for beat in beat_list:
            if step >= beat:
                sequence_num += 1
                shot_start = beat
            else:
                break
        
        # Calculate shot number within the current sequence
        shot_num = step - shot_start + 1
        
        # Generate formatted outputs
        sequence_str = str(sequence_num)
        shot_str = str(shot_num)
        shot_name = f"seq{sequence_num:02d}_shot{shot_num:02d}"
        
        print(f"🎬 [MF_ShotHelper] Step {step}: {shot_name}")
        
        return (sequence_num, sequence_str, shot_num, shot_str, shot_name)


# ============================================================================
# GRAPH PLOTTER
# ============================================================================

class MF_GraphPlotter:
    """
    A ComfyUI node that plots X,Y integer data points on a graph.
    Stores history across executions and displays interactive chart.
    """
    
    # Class variable to store graph data per node instance
    # Key format: "node_id" -> {"x_data": [], "y_data": []}
    _graph_data = {}
    _state_file = None
    _state_loaded = False
    
    CATEGORY = "MF_PipoNodes/Analysis"
    
    def __init__(self):
        # Initialize state file path based on this module's location
        if MF_GraphPlotter._state_file is None:
            MF_GraphPlotter._state_file = os.path.join(
                os.path.dirname(__file__), 
                "graph_plotter_state.json"
            )
        
        # Only load state once when first node is created
        if not MF_GraphPlotter._state_loaded:
            self.load_state()
            MF_GraphPlotter._state_loaded = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "X": ("INT", {
                    "default": 0,
                    "min": -999999,
                    "max": 999999,
                    "forceInput": True
                }),
                "Y": ("INT", {
                    "default": 0,
                    "min": -999999,
                    "max": 999999,
                    "forceInput": True
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            }
        }
    
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("X", "Y")
    FUNCTION = "plot_graph"
    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Always execute to update graph
        return float("nan")
    
    def load_state(self):
        """Load graph data from JSON file"""
        if os.path.exists(self._state_file):
            try:
                with open(self._state_file, 'r') as f:
                    MF_GraphPlotter._graph_data = json.load(f)
                print(f"📊 [MF_GraphPlotter] Loaded state from {os.path.basename(self._state_file)}")
            except Exception as e:
                print(f"⚠️ [MF_GraphPlotter] Could not load state: {e}")
                MF_GraphPlotter._graph_data = {}
        else:
            MF_GraphPlotter._graph_data = {}
    
    def save_state(self):
        """Save graph data to JSON file"""
        try:
            with open(self._state_file, 'w') as f:
                json.dump(MF_GraphPlotter._graph_data, f, indent=2)
        except Exception as e:
            print(f"❌ [MF_GraphPlotter] Error saving state: {e}")
    
    def get_node_data(self, node_id):
        """Get or initialize data for this node instance"""
        if node_id not in MF_GraphPlotter._graph_data:
            MF_GraphPlotter._graph_data[node_id] = {
                "x_data": [],
                "y_data": []
            }
        return MF_GraphPlotter._graph_data[node_id]
    
    def plot_graph(self, X, Y, unique_id=None):
        """
        Add data point and update graph
        """
        # Get node-specific data
        node_id = str(unique_id) if unique_id else "default"
        node_data = self.get_node_data(node_id)
        
        # Add new data point
        node_data["x_data"].append(X)
        node_data["y_data"].append(Y)
        
        # Save state
        self.save_state()
        
        # Prepare data for frontend
        graph_data = {
            "x_values": node_data["x_data"],
            "y_values": node_data["y_data"],
            "node_id": node_id,
            "point_count": len(node_data["x_data"])
        }
        
        print(f"📊 [MF_GraphPlotter] Point {len(node_data['x_data'])}: ({X}, {Y})")
        
        # Return data in UI format for JavaScript to render
        return {
            "ui": {
                "graph_data": [graph_data],
            },
            "result": (X, Y)
        }
    
    @classmethod
    def reset_node_data(cls, node_id):
        """Reset graph data for a specific node"""
        if node_id in cls._graph_data:
            cls._graph_data[node_id] = {
                "x_data": [],
                "y_data": []
            }
            
            # Save state to file
            try:
                with open(cls._state_file, 'w') as f:
                    json.dump(cls._graph_data, f, indent=2)
                print(f"🔄 [MF_GraphPlotter] Reset node {node_id}")
            except Exception as e:
                print(f"❌ [MF_GraphPlotter] Error saving state: {e}")


# ============================================================================
# STORY DRIVER
# ============================================================================

class MF_StoryDriver:
    """
    A ComfyUI node that tracks story progression steps and manages seeds.
    Increments step counter on each execution and provides seed management.
    Perfect for sequential image generation with consistent seeds per project.
    """
    
    # Class variable to store state across executions
    # Key format: "projectName" -> {"step": int, "seed": int}
    _state = {}
    _state_file = None
    _state_loaded = False
    
    CATEGORY = "MF_PipoNodes/Sequencing"
    
    def __init__(self):
        # Initialize state file path based on this module's location
        if MF_StoryDriver._state_file is None:
            MF_StoryDriver._state_file = os.path.join(
                os.path.dirname(__file__), 
                "story_driver_state.json"
            )
        
        # Only load state once when first node is created
        if not MF_StoryDriver._state_loaded:
            self.load_state()
            MF_StoryDriver._state_loaded = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "projectName": ("STRING", {
                    "default": "MyProject",
                    "multiline": False
                }),
                "randomize_seed_on_reset": ("BOOLEAN", {
                    "default": True
                }),
            },
            "optional": {},
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }
    
    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("step_int", "step_str", "projectName", "saveFolder", "storySeed")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    
    @classmethod
    def OUTPUT_COLORS(cls):
        # Blue for integers, green for strings (ComfyUI native colors)
        return {
            0: "#4E9FFF",  # step_int - Blue
            1: "#88FF88",  # step_str - Green
            2: "#88FF88",  # projectName - Green
            3: "#88FF88",  # saveFolder - Green
            4: "#4E9FFF",  # storySeed - Blue
        }
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Always execute to increment step
        return float("nan")
    
    def load_state(self):
        """Load state from JSON file"""
        if os.path.exists(self._state_file):
            try:
                with open(self._state_file, 'r') as f:
                    MF_StoryDriver._state = json.load(f)
                print(f"🎬 [MF_StoryDriver] Loaded state from {os.path.basename(self._state_file)}")
            except Exception as e:
                print(f"⚠️ [MF_StoryDriver] Could not load state: {e}")
                MF_StoryDriver._state = {}
        else:
            MF_StoryDriver._state = {}
    
    def save_state(self):
        """Save state to JSON file"""
        try:
            with open(self._state_file, 'w') as f:
                json.dump(MF_StoryDriver._state, f, indent=2)
        except Exception as e:
            print(f"❌ [MF_StoryDriver] Error saving state: {e}")
    
    def get_project_state(self, project_name):
        """Get or initialize state for a project"""
        if project_name not in MF_StoryDriver._state:
            MF_StoryDriver._state[project_name] = {
                "step": 0,
                "seed": random.randint(0, 0xffffffffffffffff)
            }
            self.save_state()
        return MF_StoryDriver._state[project_name]
    
    def execute(self, projectName, randomize_seed_on_reset, unique_id=None, extra_pnginfo=None):
        """
        Execute the node - increment step and return all outputs
        """
        # Get current project state
        project_state = self.get_project_state(projectName)
        
        # Get current values
        current_step = project_state["step"]
        current_seed = project_state["seed"]
        
        # Increment step for next execution
        project_state["step"] = current_step + 1
        self.save_state()
        
        # Prepare outputs
        step_int = current_step
        step_str = str(current_step)
        story_seed = current_seed
        
        # Replace spaces with underscores in projectName output
        project_name_output = projectName.replace(" ", "_")
        
        # Create saveFolder output (projectName_seed format)
        save_folder = f"{project_name_output}_{current_seed}"
        
        # Format status display
        status_text = f"Step: {current_step} | Seed: {current_seed}"
        
        print(f"🎬 [MF_StoryDriver] {projectName}: Step {current_step}, Seed {current_seed}")
        
        # Return in the format that works with the JavaScript extension
        return {
            "ui": {
                "status_display": [status_text],
            },
            "result": (step_int, step_str, project_name_output, save_folder, story_seed)
        }
    
    @classmethod
    def reset_project(cls, project_name, randomize_seed):
        """
        Reset a project's step counter and optionally randomize seed
        This method is called by the reset button via API
        """
        if project_name in cls._state:
            cls._state[project_name]["step"] = 0
            if randomize_seed:
                cls._state[project_name]["seed"] = random.randint(0, 0xffffffffffffffff)
        else:
            cls._state[project_name] = {
                "step": 0,
                "seed": random.randint(0, 0xffffffffffffffff)
            }
        
        # Save state to file
        try:
            with open(cls._state_file, 'w') as f:
                json.dump(cls._state, f, indent=2)
            print(f"🔄 [MF_StoryDriver] Reset project: {project_name}")
        except Exception as e:
            print(f"❌ [MF_StoryDriver] Error saving state: {e}")



# ============================================================================
# DATA NODES
# ============================================================================

class MFSaveData:
    """
    A node that saves string data to various file formats
    """
    
    @staticmethod
    def _clean_markdown_fences(data):
        """Remove markdown code fences if present"""
        if isinstance(data, str):
            data = data.strip()
            # Remove opening code fence (```json, ```xml, etc.)
            if data.startswith('```'):
                lines = data.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]  # Remove first line
                # Remove closing code fence
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]  # Remove last line
                data = '\n'.join(lines)
        return data
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("STRING", {"forceInput": True}),
                "output_path": ("STRING", {"default": "output"}),
                "filename": ("STRING", {"default": "data"}),
                "format": (["json", "xml", "csv", "yaml"],),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filepath",)
    FUNCTION = "save_data"
    CATEGORY = "MF Data"
    OUTPUT_NODE = True

    def save_data(self, data, output_path, filename, format):
        try:
            # Clean data - remove markdown code fences if present
            data = self._clean_markdown_fences(data)
            
            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            
            # Build full filepath
            filepath = os.path.join(output_path, f"{filename}.{format}")
            
            # Save based on format
            if format == "json":
                self._save_json(data, filepath)
            elif format == "xml":
                self._save_xml(data, filepath)
            elif format == "csv":
                self._save_csv(data, filepath)
            elif format == "yaml":
                self._save_yaml(data, filepath)
            
            print(f"[MF Save Data] Saved to: {filepath}")
            return (filepath,)
            
        except Exception as e:
            print(f"[MF Save Data] Error: {str(e)}")
            return (f"Error: {str(e)}",)
    
    def _save_json(self, data, filepath):
        """Save as JSON"""
        try:
            # Try to parse if it's already JSON
            parsed = json.loads(data)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            # If not valid JSON, just write the string as-is
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
    
    def _save_xml(self, data, filepath):
        """Save as XML"""
        try:
            # Try to parse if it's already XML
            root = ET.fromstring(data)
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
        except ET.ParseError:
            # If not valid XML, create a simple structure
            root = ET.Element("data")
            root.text = data
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    def _save_csv(self, data, filepath):
        """Save as CSV"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Try to parse as JSON array first
            try:
                parsed = json.loads(data)
                if isinstance(parsed, list):
                    # If it's a list of dicts, write as proper CSV
                    if parsed and isinstance(parsed[0], dict):
                        writer.writerow(parsed[0].keys())
                        for row in parsed:
                            writer.writerow(row.values())
                    else:
                        # List of values
                        for item in parsed:
                            writer.writerow([item])
                else:
                    # Single value
                    writer.writerow([data])
            except:
                # Just write as single row
                writer.writerow([data])
    
    def _save_yaml(self, data, filepath):
        """Save as YAML"""
        try:
            # Try to parse as JSON first
            parsed = json.loads(data)
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(parsed, f, default_flow_style=False, allow_unicode=True)
        except json.JSONDecodeError:
            # Save as simple string
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)


class MFReadData:
    """
    A node that reads data from various file formats and outputs as string
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "output"}),
                "filename": ("STRING", {"default": "data.json"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("data",)
    FUNCTION = "read_data"
    CATEGORY = "MF Data"

    def read_data(self, file_path, filename):
        try:
            # Build full filepath
            filepath = os.path.join(file_path, filename)
            
            if not os.path.exists(filepath):
                error_msg = f"File not found: {filepath}"
                print(f"[MF Read Data] {error_msg}")
                return (error_msg,)
            
            # Detect format from extension
            _, ext = os.path.splitext(filename)
            ext = ext.lower().lstrip('.')
            
            # Read based on format
            if ext == "json":
                data = self._read_json(filepath)
            elif ext == "xml":
                data = self._read_xml(filepath)
            elif ext == "csv":
                data = self._read_csv(filepath)
            elif ext in ["yaml", "yml"]:
                data = self._read_yaml(filepath)
            else:
                # Default: read as plain text
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = f.read()
            
            print(f"[MF Read Data] Read from: {filepath}")
            return (data,)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"[MF Read Data] {error_msg}")
            return (error_msg,)
    
    def _read_json(self, filepath):
        """Read JSON and return as formatted string"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _read_xml(self, filepath):
        """Read XML and return as string"""
        tree = ET.parse(filepath)
        root = tree.getroot()
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding='unicode')
    
    def _read_csv(self, filepath):
        """Read CSV and return as JSON string"""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            # If no headers detected, read as simple list
            if not data:
                f.seek(0)
                reader = csv.reader(f)
                data = [row for row in reader]
            return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _read_yaml(self, filepath):
        """Read YAML and return as JSON string"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)


class MFShowData:
    """
    A node that displays string data in a text box in the UI
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            }
        }
    
    INPUT_IS_LIST = False
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("data",)
    FUNCTION = "show_data"
    CATEGORY = "MF Data"
    OUTPUT_NODE = True

    @staticmethod
    def _clean_data(data):
        """Remove markdown code fences if present"""
        if isinstance(data, str):
            data = data.strip()
            # Remove opening code fence (```json, ```python, etc.)
            if data.startswith('```'):
                lines = data.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]  # Remove first line
                # Remove closing code fence
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]  # Remove last line
                data = '\n'.join(lines)
        return data
    
    def show_data(self, data, unique_id=None):
        """Display the data in a text widget and pass it through"""
        # Clean the data (remove markdown code fences if present)
        cleaned_data = self._clean_data(data)
        
        # Print to console
        print("=" * 50)
        print("[MF Show Data]")
        print("=" * 50)
        print(cleaned_data)
        print("=" * 50)
        
        # Return cleaned data with UI display
        return {
            "ui": {
                "text": (cleaned_data,)
            }, 
            "result": (cleaned_data,)
        }


# ============================================================================
# CUSTOM DROPDOWN MENU
# ============================================================================

class MFCustomDropdownMenu:
    """
    A node with a customizable dropdown menu.
    The dropdown options can be edited via an EDIT button in the UI.
    Options are stored per-node and persist in the workflow file.
    Default options: low, medium, high, ultra (like video game graphics settings)
    """
    
    CATEGORY = "MF_PipoNodes/Utilities"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Changed to STRING to accept any value
                # The dropdown is created and managed by JavaScript
                "selection": ("STRING", {"default": "medium"}),
                # CRITICAL: Must be in "required" or "optional" to serialize!
                # Using multiline=False and forceInput=False keeps it as a widget
                # JavaScript will hide it visually while keeping it serializable
                "dropdown_options": ("STRING", {
                    "default": "low\nmedium\nhigh\nultra",
                    "multiline": False,
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_value",)
    FUNCTION = "execute"
    OUTPUT_NODE = False
    
    def execute(self, selection, dropdown_options="low\nmedium\nhigh\nultra"):
        """
        Returns the selected dropdown value as a string.
        
        Args:
            selection: The currently selected option from the dropdown
            dropdown_options: Hidden field containing all options (for workflow persistence)
        
        Returns:
            Tuple containing the selected string value
        """
        return (selection,)


# ============================================================================
# NODE REGISTRATION
# ============================================================================

NODE_CLASS_MAPPINGS = {
    "MF_DiceRoller": MF_DiceRoller,
    "MF_LineCounter": MF_LineCounter,
    "MF_LineSelect": MF_LineSelect,
    "MF_LogFile": MF_LogFile,
    "MF_LogReader": MF_LogReader,
    "MF_Modulo": MF_Modulo,
    "MF_ModuloAdvanced": MF_ModuloAdvanced,
    "MF_ShotHelper": MF_ShotHelper,
    "MF_GraphPlotter": MF_GraphPlotter,
    "MF_StoryDriver": MF_StoryDriver,
    "MF_SaveData": MFSaveData,  # NEW in v1.4.0!
    "MF_ReadData": MFReadData,  # NEW in v1.4.0!
    "MF_ShowData": MFShowData,  # NEW in v1.4.0!
    "MF_CustomDropdownMenu": MFCustomDropdownMenu,  # NEW in v1.5.0!
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_DiceRoller": "MF Dice Roller",
    "MF_LineCounter": "MF Line Counter",
    "MF_LineSelect": "MF Line Select",
    "MF_LogFile": "MF Log File",
    "MF_LogReader": "MF Log Reader",
    "MF_Modulo": "MF Modulo",
    "MF_ModuloAdvanced": "MF Modulo Advanced",
    "MF_ShotHelper": "MF Shot Helper",
    "MF_GraphPlotter": "MF Graph Plotter",
    "MF_StoryDriver": "MF Story Driver",
    "MF_SaveData": "MF Save Data",  # NEW in v1.4.0!
    "MF_ReadData": "MF Read Data",  # NEW in v1.4.0!
    "MF_ShowData": "MF Show Data",  # NEW in v1.4.0!
    "MF_CustomDropdownMenu": "MF Custom Dropdown Menu",  # NEW in v1.5.0!
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

WEB_DIRECTORY = "./web"
