#!/usr/bin/env python3
"""
Triple extraction functionality for RivalSearchMCP.
Handles extraction of subject-predicate-object triples from text content.
"""

import re
from typing import List, Tuple


def extract_triples(text: str) -> List[Tuple[str, str, str]]:
    """
    Extract subject-predicate-object triples from text.
    
    Args:
        text: Input text to extract triples from
        
    Returns:
        List of (subject, predicate, object) tuples
    """
    triples = []
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 2:
            subject = words[0]
            predicate = words[1]
            obj = ' '.join(words[2:])
            triples.append((subject, predicate, obj))
    return triples
