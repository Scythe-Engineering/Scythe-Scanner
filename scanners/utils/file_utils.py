"""File utility functions for repository scanning."""

import os
import json
from pathlib import Path
from fnmatch import fnmatch
from typing import List, Set, Tuple


COMMON_BINARY_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar',
    '.exe', '.dll', '.so', '.dylib', '.a', '.lib',
    '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.pyc', '.pyo', '.class', '.jar', '.war',
    '.db', '.sqlite', '.sqlite3',
    '.bin', '.dat', '.o', '.obj'
}


def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary by looking for null bytes.
    
    Args:
        file_path: Path to the file to check.
        
    Returns:
        True if the file appears to be binary, False otherwise.
    """
    file_extension = Path(file_path).suffix.lower()
    if file_extension in COMMON_BINARY_EXTENSIONS:
        return True
    
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(8192)
            return b'\x00' in chunk
    except (IOError, OSError):
        return True


def load_ignore_patterns(ignore_file_path: str) -> Tuple[List[str], List[str]]:
    """Load ignore patterns from ignore.json file.
    
    Args:
        ignore_file_path: Path to the ignore.json file.
        
    Returns:
        Tuple of (exact_names, regex_patterns) lists.
    """
    try:
        with open(ignore_file_path, 'r') as file:
            ignore_data = json.load(file)
            exact_names = ignore_data.get('names', [])
            regex_patterns = ignore_data.get('regexes', [])
            return exact_names, regex_patterns
    except (IOError, OSError, json.JSONDecodeError):
        return [], []


def should_ignore_file(file_path: str, base_path: str, exact_names: List[str], regex_patterns: List[str]) -> bool:
    """Check if a file should be ignored based on patterns.
    
    Args:
        file_path: Full path to the file.
        base_path: Base directory path for relative path calculation.
        exact_names: List of exact names to ignore.
        regex_patterns: List of glob patterns to match.
        
    Returns:
        True if the file should be ignored, False otherwise.
    """
    relative_path = os.path.relpath(file_path, base_path)
    path_parts = relative_path.split(os.sep)
    
    for part in path_parts:
        if part in exact_names:
            return True
    
    for pattern in regex_patterns:
        if fnmatch(relative_path, pattern) or any(fnmatch(part, pattern) for part in path_parts):
            return True
    
    return False


def get_text_files_in_directory(directory_path: str, exact_names: List[str], regex_patterns: List[str]) -> List[str]:
    """Recursively get all non-binary, non-ignored files in a directory.
    
    Args:
        directory_path: Path to the directory to scan.
        exact_names: List of exact names to ignore.
        regex_patterns: List of glob patterns to match for ignoring.
        
    Returns:
        List of file paths that should be processed.
    """
    text_files = []
    
    for root, dirs, files in os.walk(directory_path):
        dirs_to_remove = []
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if should_ignore_file(dir_path, directory_path, exact_names, regex_patterns):
                dirs_to_remove.append(dir_name)
        
        for dir_name in dirs_to_remove:
            dirs.remove(dir_name)
        
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            if should_ignore_file(file_path, directory_path, exact_names, regex_patterns):
                continue
            
            if is_binary_file(file_path):
                continue
            
            text_files.append(file_path)
    
    return text_files
