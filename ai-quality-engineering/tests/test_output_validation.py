"""
Unit Tests for Output Validation
Pillar 1: Prompt & Output Validation
"""

import pytest
from src.validators import OutputValidator


class TestOutputValidator:
    """Test suite for OutputValidator."""
    
    def test_validate_not_empty_with_valid_output(self):
        """Test that a valid non-empty output passes validation."""
        output = "This is a valid LLM output."
        assert OutputValidator.validate_not_empty(output) is True
    
    def test_validate_not_empty_with_empty_string(self):
        """Test that an empty output fails validation."""
        output = ""
        assert OutputValidator.validate_not_empty(output) is False
    
    def test_validate_min_length_passes(self):
        """Test that output meeting minimum length passes."""
        output = "This is a comprehensive response to your question"
        assert OutputValidator.validate_min_length(output, min_length=20) is True
    
    def test_validate_min_length_fails(self):
        """Test that output below minimum length fails."""
        output = "Short"
        assert OutputValidator.validate_min_length(output, min_length=20) is False
    
    def test_validate_max_length_passes(self):
        """Test that output within max length passes."""
        output = "This is a response"
        assert OutputValidator.validate_max_length(output, max_length=100) is True
    
    def test_validate_max_length_fails(self):
        """Test that output exceeding max length fails."""
        output = "a" * 6000
        assert OutputValidator.validate_max_length(output, max_length=5000) is False
    
    def test_validate_contains_text_success(self):
        """Test content validation when all required text is present."""
        output = "Machine learning is a subset of artificial intelligence"
        required_text = ["machine learning", "artificial intelligence"]
        assert OutputValidator.validate_contains_text(output, required_text) is True
    
    def test_validate_contains_text_failure(self):
        """Test content validation when required text is missing."""
        output = "Machine learning is important"
        required_text = ["machine learning", "deep learning"]
        assert OutputValidator.validate_contains_text(output, required_text) is False
    
    def test_validate_format_json_valid(self):
        """Test JSON format validation with valid JSON."""
        output = '{"status": "success", "value": 42}'
        assert OutputValidator.validate_format(output, expected_format="json") is True
    
    def test_validate_format_json_invalid(self):
        """Test JSON format validation with invalid JSON."""
        output = '{"status": "success", value: 42}'  # Missing quotes around key
        assert OutputValidator.validate_format(output, expected_format="json") is False
    
    def test_validate_format_none(self):
        """Test that None format always passes."""
        output = "any text here"
        assert OutputValidator.validate_format(output, expected_format=None) is True
    
    @pytest.mark.validation
    def test_comprehensive_output_validation_success(self):
        """Test comprehensive validation with all checks passing."""
        output = "Python is a powerful programming language used in AI and data science"
        result = OutputValidator.validate_output(
            output,
            min_length=20,
            max_length=5000,
            required_content=["Python", "AI"]
        )
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert result["metrics"]["length"] > 0
        assert result["metrics"]["word_count"] > 0
    
    @pytest.mark.validation
    def test_comprehensive_output_validation_failure(self):
        """Test comprehensive validation with errors."""
        output = "Short output"
        result = OutputValidator.validate_output(
            output,
            min_length=50,
            max_length=5000,
            required_content=["detailed", "comprehensive"]
        )
        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
    
    @pytest.mark.validation
    def test_comprehensive_output_validation_with_format(self):
        """Test output validation with format checking."""
        output = '{"answer": "The capital of France is Paris"}'
        result = OutputValidator.validate_output(
            output,
            min_length=10,
            format="json"
        )
        assert result["is_valid"] is True
    
    @pytest.mark.validation
    def test_output_metrics_collection(self):
        """Test that output metrics are properly collected."""
        output = "One two three four five"  # 5 words
        result = OutputValidator.validate_output(output)
        assert result["metrics"]["word_count"] == 5
        assert result["metrics"]["length"] == len(output.strip())


class TestOutputValidatorIntegration:
    """Integration tests for output validation."""
    
    @pytest.mark.integration
    def test_batch_output_validation(self):
        """Test validation of multiple outputs."""
        outputs = [
            "This is a comprehensive and well-structured response",
            "Short answer",
            ""  # Empty output
        ]
        
        results = []
        for output in outputs:
            result = OutputValidator.validate_output(output, min_length=15)
            results.append(result["is_valid"])
        
        assert results == [True, False, False]
    
    @pytest.mark.integration
    def test_output_validation_case_insensitive_content(self):
        """Test that content matching is case-insensitive."""
        output = "Machine Learning is a subset of AI"
        required_content = ["machine learning", "ai"]  # lowercase search terms
        assert OutputValidator.validate_contains_text(output, required_content) is True
