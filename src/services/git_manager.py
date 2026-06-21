import subprocess
import logging
from src.core.config import settings

logger = logging.getLogger("ghost_developer")

class GitManager:
    def __init__(self, repo_path: str = settings.repo_path):
        self.repo_path = repo_path

    def _run_command(self, cmd: list) -> str:
        result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Git command failed: {' '.join(cmd)}\nError: {result.stderr}")
            raise RuntimeError(f"Git command failed: {result.stderr}")
        return result.stdout.strip()

    def checkout_new_branch(self, branch_name: str):
        logger.info(f"Checking out new branch: {branch_name}")
        self._run_command(["git", "checkout", "-b", branch_name])

    def commit_and_push(self, commit_message: str, branch_name: str):
        logger.info("Committing and pushing changes")
        self._run_command(["git", "add", "."])
        self._run_command(["git", "commit", "-m", commit_message])
        # In a real scenario, this would push to remote. Mocked for safety.
        # self._run_command(["git", "push", "origin", branch_name])
        logger.info(f"Successfully simulated push for branch {branch_name}")
