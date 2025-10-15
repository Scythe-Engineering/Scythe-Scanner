"""Repository cloning utility using GitPython."""

import os
from typing import Optional
from urllib.parse import urlparse

from git import Repo

import color_print


def _extract_repo_name(repo_url: str) -> str:
    """Extract repository name from a Git URL.

    Args:
        repo_url: The Git repository URL.

    Returns:
        The repository name extracted from the URL, or a fallback name.
    """
    try:
        # Parse the URL to extract the repository name
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip('/').split('/')

        # For URLs like https://github.com/user/repo.git, we want 'repo'
        if len(path_parts) >= 2:
            repo_name = path_parts[-1]  # Get the last part
            # Remove .git extension if present
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            return repo_name

        # Fallback: use the entire path as name, replacing problematic characters
        return parsed_url.path.strip('/').replace('/', '_').replace('.git', '')

    except Exception:
        # Ultimate fallback: use a hash of the URL
        import hashlib
        return hashlib.md5(repo_url.encode()).hexdigest()[:8]


def clone_repository(
    repo_url: str,
    target_dir: Optional[str] = None,
    branch: Optional[str] = None,
    pr_number: Optional[int] = None
) -> bool:
    """Clone a Git repository into a subdirectory within the specified directory.

    Creates a folder named after the repository within the target directory
    and clones the repository into that folder. Supports cloning specific branches
    or pull requests.

    Args:
        repo_url: The URL of the Git repository to clone.
        target_dir: The base directory where the repository folder will be created.
            If None, defaults to 'clone_dir' in the project root.
        branch: The branch name to clone. If None, clones the default branch.
        pr_number: The pull request number to clone. If specified, clones the PR
            branch using GitHub's refs/pull/{number}/head. Overrides branch parameter.

    Returns:
        True if cloning was successful, False otherwise.

    Raises:
        ValueError: If repo_url is empty or invalid, or if both branch and pr_number are specified.
        OSError: If target directory cannot be created or accessed.
    """
    if not repo_url or not isinstance(repo_url, str):
        raise ValueError("Repository URL must be a non-empty string")

    if branch is not None and pr_number is not None:
        raise ValueError("Cannot specify both branch and pr_number. Choose one.")

    if target_dir is None:
        # Default to clone_dir in the project root
        target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "clone_dir")

    try:
        # Ensure base target directory exists
        os.makedirs(target_dir, exist_ok=True)

        # Extract repository name and create subdirectory path
        repo_name = _extract_repo_name(repo_url)

        # Append branch/PR info to directory name if specified
        if pr_number is not None:
            repo_name = f"{repo_name}-pr-{pr_number}"
        elif branch is not None:
            repo_name = f"{repo_name}-{branch}"

        repo_dir = os.path.join(target_dir, repo_name)

        # Ensure the repository subdirectory exists (though clone_from will create it)
        os.makedirs(repo_dir, exist_ok=True)

        # Determine what to clone (branch or PR)
        clone_target = None
        if pr_number is not None:
            # For GitHub PRs, use the pull request ref
            clone_target = f"refs/pull/{pr_number}/head"
            color_print.print_cyan(f"Cloning pull request #{pr_number}...")
        elif branch is not None:
            clone_target = branch
            color_print.print_cyan(f"Cloning branch '{branch}'...")

        # Clone the repository into the subdirectory
        if clone_target:
            Repo.clone_from(repo_url, repo_dir, branch=clone_target)
        else:
            Repo.clone_from(repo_url, repo_dir)

        color_print.print_green(f"Repository cloned to: {repo_dir}")
        if clone_target:
            color_print.print_green(f"Checked out: {clone_target}")

        # Create scanner_metadata folder in the cloned repository
        metadata_dir = os.path.join(repo_dir, "scanner_metadata")
        os.makedirs(metadata_dir, exist_ok=True)
        color_print.print_green(f"Created scanner_metadata folder: {metadata_dir}")

        return True

    except Exception as error:
        color_print.print_red(f"Failed to clone repository {repo_url}: {error}")
        return False
