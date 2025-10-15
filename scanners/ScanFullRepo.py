"""Full repository scanner with LLM-based summary generation."""

import os
import sys
from typing import Dict, List

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.clone_repo import clone_repository
from utils import color_print
from utils.file_utils import load_ignore_patterns, should_ignore_file, is_binary_file
from utils.llm_client import load_api_key, load_model
from utils.summary_generator import generate_file_summary, generate_directory_summary


def scan_repository(repo_url: str, target_dir: str = None, branch: str = None) -> bool:
    """Scan a repository and generate summaries for all files and directories.
    
    Args:
        repo_url: URL of the repository to scan.
        target_dir: Directory where repository will be cloned.
        branch: Specific branch to clone.
        
    Returns:
        True if scanning completed successfully, False otherwise.
    """
    color_print.print_bright_cyan("=" * 60)
    color_print.print_bright_cyan("Starting Full Repository Scan")
    color_print.print_bright_cyan("=" * 60)
    
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    api_key = load_api_key(config_path)
    if not api_key:
        color_print.print_red("Cannot proceed without API key. Please configure config.json")
        return False

    model = load_model(config_path)
    if not model:
        color_print.print_red("Cannot proceed without model configuration. Please configure config.json")
        return False
    
    color_print.print_cyan("\nStep 1: Cloning repository...")
    if not clone_repository(repo_url, target_dir, branch):
        color_print.print_red("Failed to clone repository")
        return False
    
    if target_dir is None:
        target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "clone_dir")
    
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    if branch:
        repo_name = f"{repo_name}-{branch}"
    
    repo_path = os.path.join(target_dir, repo_name)
    metadata_dir = os.path.join(repo_path, "scanner_metadata")
    
    ignore_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ignore.json")
    exact_names, regex_patterns = load_ignore_patterns(ignore_file_path)
    
    color_print.print_cyan(f"\nStep 2: Loading ignore patterns from {ignore_file_path}")
    color_print.print_green(f"Loaded {len(exact_names)} exact names and {len(regex_patterns)} regex patterns")
    
    color_print.print_cyan("\nStep 3: Scanning repository files...")
    
    directory_summaries: Dict[str, List[str]] = {}
    
    for root, dirs, files in os.walk(repo_path):
        dirs_to_remove = []
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if should_ignore_file(dir_path, repo_path, exact_names, regex_patterns):
                dirs_to_remove.append(dir_name)
        
        for dir_name in dirs_to_remove:
            dirs.remove(dir_name)
        
        current_dir_summaries = []
        
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            if should_ignore_file(file_path, repo_path, exact_names, regex_patterns):
                continue
            
            if is_binary_file(file_path):
                continue
            
            summary = generate_file_summary(file_path, metadata_dir, repo_path, api_key, model)
            if summary:
                current_dir_summaries.append(summary)
        
        if current_dir_summaries:
            directory_summaries[root] = current_dir_summaries
    
    color_print.print_cyan("\nStep 4: Generating directory summaries...")
    
    sorted_dirs = sorted(directory_summaries.keys(), key=lambda x: x.count(os.sep), reverse=True)
    
    for dir_path in sorted_dirs:
        file_summaries = directory_summaries[dir_path]
        
        subdirs = [d for d in sorted_dirs if d != dir_path and d.startswith(dir_path + os.sep)]
        for subdir in subdirs:
            subdir_summary_path = os.path.join(metadata_dir, os.path.relpath(subdir, repo_path), "_directory_summary.md")
            if os.path.exists(subdir_summary_path):
                try:
                    with open(subdir_summary_path, 'r') as f:
                        lines = f.readlines()
                        if len(lines) > 2:
                            file_summaries.append(''.join(lines[2:]).strip())
                except (IOError, OSError):
                    pass
        
        generate_directory_summary(dir_path, metadata_dir, repo_path, api_key, model, file_summaries)
    
    color_print.print_bright_green("\n" + "=" * 60)
    color_print.print_bright_green("Repository scan completed successfully!")
    color_print.print_bright_green("=" * 60)
    color_print.print_green(f"\nSummaries saved to: {metadata_dir}")
    
    return True


if __name__ == "__main__":
    repository_url = "https://github.com/example/repo.git"
    
    scan_repository(repository_url)
