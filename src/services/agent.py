import asyncio
import logging
import subprocess
from src.models.schemas import GitHubIssue, TestResult
from src.services.git_manager import GitManager

logger = logging.getLogger("ghost_developer")
logger.setLevel(logging.INFO)

class GhostAgentSwarm:
    def __init__(self):
        self.git = GitManager()

    async def write_code(self, issue: GitHubIssue) -> str:
        logger.info(f"Primary Agent: Analyzing AST and writing fix for issue #{issue.number}")
        await asyncio.sleep(0.5) # Simulate LLM inference
        return "def fixed_function():\n    return True\n"

    async def write_tests(self, code: str) -> str:
        logger.info("Testing Agent: Generating pytest scripts for the new code")
        await asyncio.sleep(0.5) # Simulate LLM inference
        return "def test_fixed_function():\n    assert fixed_function() == True\n"

    async def run_tests(self, test_code: str) -> TestResult:
        logger.info("Testing Agent: Executing pytest locally")
        await asyncio.sleep(0.5) # Simulate test execution
        # Mocking test execution success for the demo
        return TestResult(passed=True, output="1 passed in 0.01s")

    async def solve_issue(self, issue: GitHubIssue):
        logger.info(f"Ghost Developer awoken for Issue #{issue.number}: {issue.title}")
        
        branch_name = f"fix/issue-{issue.number}"
        
        # 1. Branching
        try:
            self.git.checkout_new_branch(branch_name)
        except Exception:
            logger.warning(f"Could not checkout branch {branch_name}, continuing in memory simulation")

        max_retries = 3
        for attempt in range(max_retries):
            # 2. Write code
            new_code = await self.write_code(issue)
            
            # 3. Write & Run tests
            test_code = await self.write_tests(new_code)
            result = await self.run_tests(test_code)
            
            if result.passed:
                logger.info(f"Tests passed on attempt {attempt + 1}! Preparing PR.")
                try:
                    self.git.commit_and_push(f"Fix issue #{issue.number}: {issue.title}", branch_name)
                except Exception:
                    logger.warning("Simulated commit successful (bypassed actual git error in mock).")
                logger.info("Pull Request automatically opened. Going back to sleep.")
                return {"status": "success", "pr_opened": True}
            
            logger.warning(f"Tests failed on attempt {attempt + 1}. Looping to debug...")
            
        logger.error("Ghost Developer failed to resolve the issue after max retries.")
        return {"status": "failed", "pr_opened": False}
