<div align="center">
  <h1>👻 Ghost Developer</h1>
  <p><b>An autonomous AI developer that lives in your repository, fixes bugs, and submits PRs while you sleep.</b></p>

  <img src="https://img.shields.io/badge/STATUS-PRODUCTION_READY-brightgreen" />
  <img src="https://img.shields.io/badge/FASTAPI-ORCHESTRATOR-blue" />
  <img src="https://img.shields.io/badge/AST-PARSING-orange" />
</div>

## The Problem
You are losing 15+ hours a week reviewing minor Pull Requests and fixing syntax bugs instead of actually building your startup. You are burning out.

## The Solution
I built **Ghost Developer**—an autonomous AI agent swarm that listens to your GitHub webhooks. When an issue is tagged "bug", it wakes up, clones the repo, fixes the bug, runs tests locally, and submits a PR. 

No SaaS subscriptions. No granting read/write access to third-party corporate APIs. 

## How it Works (Under the Hood)
1. **GitHub Webhooks & FastAPI:** A localized server listens for new GitHub issues.
2. **AST Parsing:** To bypass LLM context limits, the system doesn't feed your 50,000-line codebase to the LLM. Instead, it uses an Abstract Syntax Tree (AST) parser to surgically extract only the relevant classes and functions.
3. **Multi-Agent Swarm (`asyncio`):** 
   - A *Primary Agent* writes the bug fix.
   - A *Testing Agent* writes `pytest` scripts and executes them locally.
   - If tests fail, the swarm loops and self-debugs.
4. **Git Automation:** Uses subprocesses to automatically checkout a branch, commit the fix, and push the Pull Request.

## Architecture

```mermaid
sequenceDiagram
    participant GitHub
    participant FastAPI_Webhook
    participant AST_Parser
    participant Ghost_Swarm
    participant Git_CLI
    
    GitHub->>FastAPI_Webhook: POST /webhook/github (Issue #42)
    FastAPI_Webhook->>AST_Parser: Extract relevant code context
    AST_Parser-->>Ghost_Swarm: Parsed AST Nodes
    loop Debugging Cycle
        Ghost_Swarm->>Ghost_Swarm: Write Fix
        Ghost_Swarm->>Ghost_Swarm: Write & Run Pytest
    end
    Ghost_Swarm->>Git_CLI: Commit & Push Branch
    Git_CLI-->>GitHub: Open Pull Request
```

## Setup & Run
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```
Then, point your GitHub repository Webhook to your local server (e.g., using `ngrok`).

---
*Built to completely eradicate the technical bottlenecks of early-stage startups.*
