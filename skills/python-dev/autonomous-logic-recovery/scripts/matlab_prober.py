import re

class MatlabProber:
    def inject(self, code: str) -> str:
        # Regex to find 'if', 'elseif', 'for', 'while'
        # Handles both 'if cond' and 'if(cond)'
        pattern = r"(if|elseif|for|while)\s+(.*?)\n"
        replacement = r"\1 \2\nfprintf('DEBUG: \1 \2 entered\\n');\n"
        
        # Also handle one-liners or different spacing if needed, 
        # but the plan spec shows a standard block.
        return re.sub(pattern, replacement, code)
