"""
Reasoning and AI processing tools for FastMCP server.
"""

import json
from typing import Optional
from mcp.server import FastMCP
from src.reasoning.processor import ReasoningProcessor
from src.schemas.schemas import ReasoningResult, ReasoningStep


def register_reasoning_tools(mcp: FastMCP):
    """Register all reasoning and AI processing tools."""
    
    # Initialize reasoning processor (singleton)
    reason_processor = ReasoningProcessor()
    
    @mcp.tool()
    def adaptive_reason(
        step_content: str,
        step_num: int,
        estimated_steps: int,
        continue_reasoning: bool,
        is_revision: bool = False,
        revises_step: Optional[int] = None,
        branch_from_step: Optional[int] = None,
        branch_id: Optional[str] = None,
        needs_more_steps: bool = False
    ) -> ReasoningResult:
        """Dynamic step-by-step reasoning for problems. Allows revisions, branching, extension of steps."""
        
        # Preserve exact original logic by calling the processor
        arguments = {
            'step_content': step_content,
            'step_num': step_num,
            'estimated_steps': estimated_steps,
            'continue_reasoning': continue_reasoning,
            'is_revision': is_revision,
            'revises_step': revises_step,
            'branch_from_step': branch_from_step,
            'branch_id': branch_id,
            'needs_more_steps': needs_more_steps
        }
        
        result = reason_processor.process_step(arguments)
        response_data = json.loads(result['content'][0]['text'])
        
        return ReasoningResult(
            current_step=ReasoningStep(
                step_num=response_data['step_num'],
                content=step_content,
                estimated_steps=response_data['estimated_steps'],
                continue_reasoning=response_data['continue_reasoning'],
                is_revision=is_revision,
                revises_step=revises_step,
                branch_from_step=branch_from_step,
                branch_id=branch_id,
                needs_more_steps=needs_more_steps
            ),
            paths=response_data['paths'],
            steps_count=response_data['steps_count']
        )