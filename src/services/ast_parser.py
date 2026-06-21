import ast
import logging
from typing import List
from src.models.schemas import ParsedASTNode

logger = logging.getLogger("ghost_developer")

class CodeContextExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> List[ParsedASTNode]:
        """Surgically extracts classes and functions to bypass LLM context limits."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                source = f.read()
            
            tree = ast.parse(source)
            lines = source.splitlines()
            extracted_nodes = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    # Get the code snippet for this specific AST node
                    start = node.lineno - 1
                    end = node.end_lineno
                    code_snippet = "\n".join(lines[start:end])
                    
                    extracted_nodes.append(
                        ParsedASTNode(
                            name=node.name,
                            type=type(node).__name__,
                            code_snippet=code_snippet,
                            start_line=node.lineno,
                            end_line=node.end_lineno
                        )
                    )
            logger.info(f"Extracted {len(extracted_nodes)} nodes from {self.file_path}")
            return extracted_nodes
        except Exception as e:
            logger.error(f"Failed to parse AST for {self.file_path}: {str(e)}")
            return []
