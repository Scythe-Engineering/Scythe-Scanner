"""Summary generation and storage utilities."""

import os
from typing import Optional, List

import color_print
from llm_client import generate_summary, load_model


def check_summary_exists(summary_path: str) -> bool:
    """Check if a summary file already exists.
    
    Args:
        summary_path: Path to the summary markdown file.
        
    Returns:
        True if summary exists, False otherwise.
    """
    return os.path.exists(summary_path)


def save_summary_markdown(summary_path: str, summary_content: str, original_path: str) -> bool:
    """Save summary to a markdown file.
    
    Args:
        summary_path: Path where the summary should be saved.
        summary_content: The summary text to save.
        original_path: Original file/directory path being summarized.
        
    Returns:
        True if saved successfully, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        
        with open(summary_path, 'w') as file:
            file.write(f"# Summary: {original_path}\n\n")
            file.write(summary_content)
            file.write("\n")
        
        return True
        
    except (IOError, OSError) as error:
        color_print.print_red(f"Failed to save summary to {summary_path}: {error}")
        return False


def generate_file_summary(file_path: str, metadata_dir: str, repo_base_path: str, api_key: str, model: str) -> Optional[str]:
    """Generate summary for a single file.

    Args:
        file_path: Path to the file to summarize.
        metadata_dir: Base directory for scanner_metadata.
        repo_base_path: Base path of the repository.
        api_key: OpenRouter API key.
        model: Model name to use for generation.

    Returns:
        Summary string if successful, None otherwise.
    """
    relative_path = os.path.relpath(file_path, repo_base_path)
    summary_filename = f"{os.path.basename(file_path)}.summary.md"
    summary_dir = os.path.join(metadata_dir, os.path.dirname(relative_path))
    summary_path = os.path.join(summary_dir, summary_filename)
    
    if check_summary_exists(summary_path):
        color_print.print_yellow(f"Summary already exists: {relative_path}")
        with open(summary_path, 'r') as file:
            lines = file.readlines()
            if len(lines) > 2:
                return ''.join(lines[2:]).strip()
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        if not content.strip():
            color_print.print_yellow(f"Skipping empty file: {relative_path}")
            return None
        
        color_print.print_cyan(f"Generating summary for: {relative_path}")
        summary = generate_summary(content, f"file: {relative_path}", api_key, model)
        
        if summary:
            if save_summary_markdown(summary_path, summary, relative_path):
                color_print.print_green(f"Summary saved: {relative_path}")
                return summary
        
        return None
        
    except (IOError, OSError) as error:
        color_print.print_red(f"Failed to read file {file_path}: {error}")
        return None


def generate_directory_summary(directory_path: str, metadata_dir: str, repo_base_path: str, api_key: str, model: str, file_summaries: List[str]) -> Optional[str]:
    """Generate rollup summary for a directory.

    Args:
        directory_path: Path to the directory to summarize.
        metadata_dir: Base directory for scanner_metadata.
        repo_base_path: Base path of the repository.
        api_key: OpenRouter API key.
        model: Model name to use for generation.
        file_summaries: List of summaries from files in this directory.

    Returns:
        Summary string if successful, None otherwise.
    """
    relative_path = os.path.relpath(directory_path, repo_base_path)
    if relative_path == '.':
        relative_path = 'repository root'
        summary_path = os.path.join(metadata_dir, "_repository_summary.md")
    else:
        summary_dir = os.path.join(metadata_dir, relative_path)
        summary_path = os.path.join(summary_dir, "_directory_summary.md")
    
    if check_summary_exists(summary_path):
        color_print.print_yellow(f"Directory summary already exists: {relative_path}")
        return None
    
    if not file_summaries:
        color_print.print_yellow(f"No file summaries to aggregate for: {relative_path}")
        return None
    
    aggregated_content = "\n\n".join(file_summaries)
    
    color_print.print_cyan(f"Generating directory summary for: {relative_path}")
    summary = generate_summary(aggregated_content, f"directory: {relative_path}", api_key, model)
    
    if summary:
        if save_summary_markdown(summary_path, summary, relative_path):
            color_print.print_green(f"Directory summary saved: {relative_path}")
            return summary
    
    return None
