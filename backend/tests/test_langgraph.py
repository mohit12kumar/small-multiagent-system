import sys
import os

# Add root project directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.graph.workflow import interview_graph

def test_langgraph_compilation():
    print("==================================================")
    print("       LangGraph State Graph Check               ")
    print("==================================================")
    
    print(f"Graph Object: {interview_graph}")
    print("\nState Graph Nodes:")
    for node in interview_graph.nodes:
        print(f"  - Node: {node}")
        
    print("\nState Graph Verification: SUCCESS!")
    print("==================================================")

if __name__ == "__main__":
    test_langgraph_compilation()
