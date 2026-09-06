"""
Prompt and Output Validators
Pillar 1: Prompt & Output Validation
"""

from typing import Dict, List, Any, Optional


class PromptValidator:
    """Validates prompts for quality and completeness."""
    
    @staticmethod
    def validate_not_empty(prompt: str) -> bool:
        """Check if prompt is not empty."""
        return isinstance(prompt, str) and len(prompt.strip()) > 0
    
    @staticmethod
    def validate_min_length(prompt: str, min_length: int = 10) -> bool:
        """Check if prompt meets minimum length requirement."""
        return len(prompt.strip()) >= min_length
    
    @staticmethod
    def validate_max_length(prompt: str, max_length: int = 5000) -> bool:
        """Check if prompt is within maximum length."""
        return len(prompt.strip()) <= max_length
    
    @staticmethod
    def validate_contains_keywords(prompt: str, keywords: List[str]) -> bool:
        """Check if prompt contains required keywords."""
        prompt_lower = prompt.lower()
        return all(keyword.lower() in prompt_lower for keyword in keywords)
    
    @classmethod
    def validate_prompt(cls, prompt: str, **kwargs) -> Dict[str, Any]:
        """Comprehensive prompt validation."""
        results = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Basic validation
        if not cls.validate_not_empty(prompt):
            results["is_valid"] = False
            results["errors"].append("Prompt is empty")
            return results
        
        # Length validation
        min_len = kwargs.get("min_length", 10)
        max_len = kwargs.get("max_length", 5000)
        
        if not cls.validate_min_length(prompt, min_len):
            results["is_valid"] = False
            results["errors"].append(f"Prompt is shorter than minimum length ({min_len})")
        
        if not cls.validate_max_length(prompt, max_len):
            results["is_valid"] = False
            results["errors"].append(f"Prompt exceeds maximum length ({max_len})")
        
        # Keywords validation
        required_keywords = kwargs.get("required_keywords", [])
        if required_keywords and not cls.validate_contains_keywords(prompt, required_keywords):
            missing = [kw for kw in required_keywords 
                      if kw.lower() not in prompt.lower()]
            results["warnings"].append(f"Missing keywords: {missing}")
        
        return results


class OutputValidator:
    """Validates LLM outputs for quality and compliance."""
    
    @staticmethod
    def validate_not_empty(output: str) -> bool:
        """Check if output is not empty."""
        return isinstance(output, str) and len(output.strip()) > 0
    
    @staticmethod
    def validate_min_length(output: str, min_length: int = 10) -> bool:
        """Check if output meets minimum length."""
        return len(output.strip()) >= min_length
    
    @staticmethod
    def validate_max_length(output: str, max_length: int = 5000) -> bool:
        """Check if output is within maximum length."""
        return len(output.strip()) <= max_length
    
    @staticmethod
    def validate_contains_text(output: str, required_text: List[str]) -> bool:
        """Check if output contains required text patterns."""
        output_lower = output.lower()
        return all(text.lower() in output_lower for text in required_text)
    
    @staticmethod
    def validate_format(output: str, expected_format: Optional[str] = None) -> bool:
        """Validate output format (json, markdown, plain text, etc.)."""
        if expected_format is None:
            return True
        
        if expected_format.lower() == "json":
            import json
            try:
                json.loads(output)
                return True
            except:
                return False
        
        return True
    
    @classmethod
    def validate_output(cls, output: str, **kwargs) -> Dict[str, Any]:
        """Comprehensive output validation."""
        results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "metrics": {
                "length": len(output.strip()),
                "word_count": len(output.strip().split())
            }
        }
        
        # Basic validation
        if not cls.validate_not_empty(output):
            results["is_valid"] = False
            results["errors"].append("Output is empty")
            return results
        
        # Length validation
        min_len = kwargs.get("min_length", 10)
        max_len = kwargs.get("max_length", 5000)
        
        if not cls.validate_min_length(output, min_len):
            results["is_valid"] = False
            results["errors"].append(f"Output is shorter than minimum ({min_len})")
        
        if not cls.validate_max_length(output, max_len):
            results["is_valid"] = False
            results["errors"].append(f"Output exceeds maximum ({max_len})")
        
        # Content validation
        required_content = kwargs.get("required_content", [])
        if required_content and not cls.validate_contains_text(output, required_content):
            missing = [t for t in required_content if t.lower() not in output.lower()]
            results["warnings"].append(f"Missing content: {missing}")
        
        # Format validation
        expected_format = kwargs.get("format")
        if expected_format and not cls.validate_format(output, expected_format):
            results["errors"].append(f"Output format mismatch. Expected: {expected_format}")
            results["is_valid"] = False
        
        return results
