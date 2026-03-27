import re

class CSharpProber:
    def inject(self, code: str) -> str:
        # Minimal regex-based injection for 'if' statements
        pattern = r"if\s*\((.*?)\)\s*\{"
        replacement = r'if (\1) { Console.WriteLine("DEBUG: if (\1) entered");'
        return re.sub(pattern, replacement, code)
