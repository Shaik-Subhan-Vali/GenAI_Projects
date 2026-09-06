"""
Unit Tests for Prompt Validation
Pillar 1: Prompt & Output Validation
"""

import pytest
from src.validators import PromptValidator


class TestPromptValidator:
    """Test suite for PromptValidator."""
    
    def test_validate_not_empty_with_valid_prompt(self):
        """Test that a valid non-empty prompt passes validation."""
        prompt = "What is the capital of France?"
        assert PromptValidator.validate_not_empty(prompt) is True
    
    def test_validate_not_empty_with_empty_string(self):
        """Test that an empty prompt fails validation."""
        prompt = ""
        assert PromptValidator.validate_not_empty(prompt) is False
    
    def test_validate_not_empty_with_whitespace_only(self):
        """Test that whitespace-only prompt fails validation."""
        prompt = "   "
        assert PromptValidator.validate_not_empty(prompt) is False
    
    def test_validate_min_length_passes(self):
        """Test that a prompt meeting minimum length passes."""
        prompt = "This is a valid prompt"
        assert PromptValidator.validate_min_length(prompt, min_length=10) is True
    
    def test_validate_min_length_fails(self):
        """Test that a prompt below minimum length fails."""
        prompt = "Short"
        assert PromptValidator.validate_min_length(prompt, min_length=10) is False
    
    def test_validate_max_length_passes(self):
        """Test that a prompt within max length passes."""
        prompt = "This is a test prompt"
        assert PromptValidator.validate_max_length(prompt, max_length=100) is True
    
    def test_validate_max_length_fails(self):
        """Test that a prompt exceeding max length fails."""
        prompt = "a" * 1000
        assert PromptValidator.validate_max_length(prompt, max_length=100) is False
    
    def test_validate_contains_keywords_success(self):
        """Test keyword validation with all keywords present."""
        prompt = "Please summarize the document about artificial intelligence"
        keywords = ["summarize", "document"]
        assert PromptValidator.validate_contains_keywords(prompt, keywords) is True
    
    def test_validate_contains_keywords_failure(self):
        """Test keyword validation with missing keywords."""
        prompt = "Please summarize the document"
        keywords = ["summarize", "classification"]
        assert PromptValidator.validate_contains_keywords(prompt, keywords) is False
    
    @pytest.mark.validation
    def test_comprehensive_prompt_validation_success(self):
        """Test comprehensive validation with all checks passing."""
        prompt = "Please provide a detailed analysis of machine learning models"
        result = PromptValidator.validate_prompt(
            prompt,
            min_length=10,
            max_length=1000,
            required_keywords=["analysis", "models"]
        )
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    @pytest.mark.validation
    def test_comprehensive_prompt_validation_failure(self):
        """Test comprehensive validation with errors."""
        prompt = "Short"
        result = PromptValidator.validate_prompt(
            prompt,
            min_length=20,
            max_length=1000,
            required_keywords=["analysis"]
        )
        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
    
    @pytest.mark.validation
    def test_comprehensive_prompt_validation_with_warnings(self):
        """Test comprehensive validation with warnings (missing keywords)."""
        prompt = "Please provide a detailed summary"
        result = PromptValidator.validate_prompt(
            prompt,
            min_length=10,
            max_length=1000,
            required_keywords=["analysis", "summary"]
        )
        # Should be valid but with a warning for missing 'analysis' keyword
        assert len(result["warnings"]) > 0


class TestPromptValidatorIntegration:
    """Integration tests for prompt validation."""
    
    @pytest.mark.integration
    def test_batch_prompt_validation(self):
        """Test validation of multiple prompts."""
        prompts = [
            "What is Python programming?",
            "Explain machine learning concepts",
            ""  # Empty prompt
        ]
        
        results = []
        for prompt in prompts:
            result = PromptValidator.validate_prompt(prompt, min_length=10)
            results.append(result["is_valid"])
        
        assert results == [True, True, False]
    
    @pytest.mark.integration
    def test_prompt_validation_case_insensitive_keywords(self):
        """Test that keyword matching is case-insensitive."""
        prompt = "Please SUMMARIZE this DOCUMENT about AI"
        keywords = ["summarize", "document"]  # lowercase keywords
        assert PromptValidator.validate_contains_keywords(prompt, keywords) is True
