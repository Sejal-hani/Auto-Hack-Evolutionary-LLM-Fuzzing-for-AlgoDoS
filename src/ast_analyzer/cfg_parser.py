"""
Abstract Syntax Tree (AST) Control Flow Analyzer.

Provides "Machine Vision" to the LLM Fuzzer.
Parses C++ source code into an AST using tree-sitter, extracting structural bottlenecks,
loop depths, and Codeforces-specific algorithmic vulnerabilities.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional

# tree-sitter is the industry standard for fast, robust AST parsing
import tree_sitter
import tree_sitter_cpp

logger = logging.getLogger(__name__)

@dataclass(frozen=True, slots=True)
class CppAstMetadata:
    """Immutable data contract for static analysis results."""
    max_loop_depth: int
    recursive_functions: tuple[str, ...]  # Tuples used for hashability/immutability
    vulnerable_stls: tuple[str, ...]
    
    def to_llm_prompt_context(self) -> str:
        """
        Translates AST metadata into highly specific, aggressive instructions 
        for the LLM Fuzzer.
        """
        context = ["--- [STATIC ANALYSIS METADATA] ---"]
        
        # Loop Complexity Hint
        if self.max_loop_depth >= 3:
            context.append(f"[!] Critical: {self.max_loop_depth}-level nested loop detected. Target O(N^{self.max_loop_depth}) polynomial exhaustion.")
        elif self.max_loop_depth == 2:
            context.append("[!] Notice: 2-level nested loop detected. Target O(N^2) quadratic traps (e.g., reverse sorted array, many identical elements).")
            
        # Recursion Hint
        if self.recursive_functions:
            funcs = ", ".join(self.recursive_functions)
            context.append(f"[!] Recursion Detected in functions: {funcs}. Exploit vector: Generate linear/star constraints to maximize Call Stack depth.")
            
        # Codeforces Specific STL Hacks
        if "unordered_map" in self.vulnerable_stls or "unordered_set" in self.vulnerable_stls:
            context.append("[!] VULNERABLE STL DETECTED: `std::unordered_map/set`. It uses a deterministic hash. Exploit vector: Generate elements separated by powers of 2 to force hash collisions and degrade O(1) to O(N).")
            
        if not context[1:]:
            context.append("[i] AST Analysis found standard linear flow. Search for hidden constant-factor bottlenecks or math traps.")
            
        context.append("----------------------------------\n")
        return "\n".join(context)


class AstAnalyzer:
    """
    Traverses the C++ AST via Depth-First Search (DFS) to extract algorithmic structure.
    """
    
    def __init__(self):
        # Initialize the C++ Grammar
        self.language = tree_sitter.Language(tree_sitter_cpp.language(), "cpp")
        self.parser = tree_sitter.Parser()
        self.parser.set_language(self.language)
        
        # Nodes that signify a loop block in C++
        self.loop_node_types = {'for_statement', 'while_statement', 'do_statement'}
        
        # Common vulnerable CP data structures
        self.target_stls = {'unordered_map', 'unordered_set'}

    def analyze_code(self, source_code: str) -> CppAstMetadata:
        """
        Main entrypoint. Parses code and returns the structural metadata.
        """
        code_bytes = source_code.encode('utf-8')
        tree = self.parser.parse(code_bytes)
        root_node = tree.root_node
        
        max_depth = self._find_max_loop_depth(root_node, current_depth=0)
        recursions = self._detect_recursive_functions(root_node, code_bytes)
        stls = self._detect_vulnerable_stls(root_node, code_bytes)
        
        return CppAstMetadata(
            max_loop_depth=max_depth,
            recursive_functions=tuple(sorted(list(recursions))),
            vulnerable_stls=tuple(sorted(list(stls)))
        )

    def _find_max_loop_depth(self, node: tree_sitter.Node, current_depth: int) -> int:
        """Recursive DFS to calculate the maximum nesting level of loops."""
        depth = current_depth
        if node.type in self.loop_node_types:
            depth += 1
            
        max_child_depth = depth
        for child in node.children:
            child_depth = self._find_max_loop_depth(child, depth)
            if child_depth > max_child_depth:
                max_child_depth = child_depth
                
        return max_child_depth

    def _detect_recursive_functions(self, root_node: tree_sitter.Node, code_bytes: bytes) -> Set[str]:
        """
        Identifies function definitions and checks if their internal block
        contains a call to their own identifier.
        """
        recursive_funcs = set()
        
        # Find all function definitions
        for child in root_node.children:
            if child.type == 'function_definition':
                # Extract the function name
                decl_node = child.child_by_field_name('declarator')
                if not decl_node:
                    continue
                    
                # Handle standard identifiers vs reference/pointer declarators
                if decl_node.type == 'identifier':
                    func_name = code_bytes[decl_node.start_byte:decl_node.end_byte].decode('utf-8')
                elif decl_node.type == 'function_declarator':
                    ident_node = decl_node.child_by_field_name('declarator')
                    if not ident_node:
                        continue
                    func_name = code_bytes[ident_node.start_byte:ident_node.end_byte].decode('utf-8')
                else:
                    continue
                    
                # Extract the function body
                body_node = child.child_by_field_name('body')
                if not body_node:
                    continue
                
                # Check if the function name is called inside its own body
                if self._contains_call_to(body_node, func_name, code_bytes):
                    recursive_funcs.add(func_name)
                    
        return recursive_funcs

    def _contains_call_to(self, node: tree_sitter.Node, target_name: str, code_bytes: bytes) -> bool:
        """Helper to scan a block of code for a specific function call."""
        if node.type == 'call_expression':
            func_node = node.child_by_field_name('function')
            if func_node and code_bytes[func_node.start_byte:func_node.end_byte].decode('utf-8') == target_name:
                return True
                
        for child in node.children:
            if self._contains_call_to(child, target_name, code_bytes):
                return True
        return False

    def _detect_vulnerable_stls(self, node: tree_sitter.Node, code_bytes: bytes) -> Set[str]:
        """Scans the AST for usage of specific hash-based C++ templates."""
        found = set()
        if node.type in {'template_type', 'type_identifier', 'identifier'}:
            text = code_bytes[node.start_byte:node.end_byte].decode('utf-8')
            if text in self.target_stls:
                found.add(text)
                
        for child in node.children:
            found.update(self._detect_vulnerable_stls(child, code_bytes))
            
        return found