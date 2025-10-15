# ----------------------------------------------------------------------------
# [MF PipoNodes]
# ----------------------------------------------------------------------------
# Author: Pierre Biet | Moment Factory | 2025
# 
# Description: Collection of utility nodes for ComfyUI workflows
# Version: 1.2.0
# --

import random
import os
import datetime
import folder_paths


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
                "save_log_path": ("STRING", {"default": folder_paths.get_output_directory()}),
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
    
    def write_log(self, log_entry, save_log_path=None, log_file_name=None):
        """Write a timestamped log entry to file."""
        log_file_path = _get_log_file_path(save_log_path, log_file_name, self.output_dir)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_entry = f"[{timestamp}] {log_entry}\n\n"
        
        try:
            # Write new entry
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(formatted_entry)
            
            # Read entire log for display
            with open(log_file_path, "r", encoding="utf-8") as f:
                self.last_log_content = f.read()
            
            print(f"📝 [MF_LogFile] Wrote entry to {os.path.basename(log_file_path)}")
            
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
    "MF_ShotHelper": MF_ShotHelper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_DiceRoller": "MF Dice Roller",
    "MF_LineCounter": "MF Line Counter",
    "MF_LineSelect": "MF Line Select",
    "MF_LogFile": "MF Log File",
    "MF_LogReader": "MF Log Reader",
    "MF_Modulo": "MF Modulo",
    "MF_ModuloAdvanced": "MF Modulo Advanced",
    "MF_ShotHelper": "MF Shot Helper"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

WEB_DIRECTORY = "./web"