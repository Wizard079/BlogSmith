#!/usr/bin/env python
import sys
import warnings
from blogsmith.cli import parse_args
from blogsmith.env import DEBUG
from blogsmith.crew import Blogsmith
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    args = parse_args()
    if DEBUG:
        print(f"Running in DEBUG mode with args: {args}")
    inputs = {
        'topic': args.topic,
        'tone' : args.tone,
    }
    
    try:
        Blogsmith().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
