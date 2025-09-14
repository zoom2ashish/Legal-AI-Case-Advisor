#!/usr/bin/env python3
"""
Legal AI Agents Module
Provides specialized AI agents for legal research, case analysis, document review, and precedent mining
"""

from .base_legal_agent import BaseLegalAgent
from .research_agent import LegalResearchAgent
from .case_agent import CaseAnalysisAgent
from .document_agent import DocumentReviewAgent
from .precedent_agent import PrecedentMiningAgent

__all__ = [
    'BaseLegalAgent',
    'LegalResearchAgent', 
    'CaseAnalysisAgent',
    'DocumentReviewAgent',
    'PrecedentMiningAgent'
]