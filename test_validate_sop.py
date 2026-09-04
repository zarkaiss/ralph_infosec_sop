#!/usr/bin/env python3
"""
Unit tests for validate_sop.py

Tests cover:
1. SOPComplianceReport dataclass states (COMPLIANT/WARNING/NON-COMPLIANT)
2. SOPValidator.validate_file() with valid/invalid SOP files
3. Section detection for required sections
4. RFC2119 keyword detection in Procedure section
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import os

from validate_sop import SOPComplianceReport, SOPValidator


class TestSOPComplianceReport:
    """Test cases for SOPComplianceReport dataclass."""
    
    def test_compliant_status(self):
        """Test that COMPLIANT status is returned when compliant=True and no issues/warnings."""
        report = SOPComplianceReport(
            filename="test.sop.md",
            filepath="/path/to/test.sop.md",
            compliant=True,
            issues_list=[],
            warnings_list=[]
        )
        assert report.status == "COMPLIANT"
    
    def test_non_compliant_status(self):
        """Test that NON-COMPLIANT status is returned when compliant=False and has issues."""
        report = SOPComplianceReport(
            filename="test.sop.md",
            filepath="/path/to/test.sop.md",
            compliant=False,
            issues_list=["Missing section: Overview"],
            warnings_list=[]
        )
        assert report.status == "NON-COMPLIANT"
    
    def test_warning_status(self):
        """Test that WARNING status is returned when no issues but has warnings."""
        report = SOPComplianceReport(
            filename="test.sop.md",
            filepath="/path/to/test.sop.md",
            compliant=True,  # compliant can be True even with warnings
            issues_list=[],
            warnings_list=["No RFC2119 keywords found"]
        )
        assert report.status == "WARNING"
    
    def test_non_compliant_with_warnings(self):
        """Test that NON-COMPLIANT status takes precedence over warnings when issues exist."""
        report = SOPComplianceReport(
            filename="test.sop.md",
            filepath="/path/to/test.sop.md",
            compliant=False,
            issues_list=["Missing section: Procedure"],
            warnings_list=["No RFC2119 keywords found"]
        )
        assert report.status == "NON-COMPLIANT"
    
    def test_compliant_false_with_warnings(self):
        """Test status when compliant=False but only has warnings (edge case)."""
        report = SOPComplianceReport(
            filename="test.sop.md",
            filepath="/path/to/test.sop.md",
            compliant=False,
            issues_list=[],
            warnings_list=["No RFC2119 keywords found"]
        )
        # According to the logic: if compliant is False but no issues and has warnings -> WARNING
        assert report.status == "WARNING"
    
    def test_default_values(self):
        """Test that default values are set correctly when not specified."""
        report = SOPComplianceReport(
            filename="test.sop.md",
            filepath="/path/to/test.sop.md"
        )
        assert report.compliant is False
        assert report.issues_list == []
        assert report.warnings_list == []
        assert report.status == "NON-COMPLIANT"  # Default: compliant=False, no issues, no warnings -> NON-COMPLIANT
    
    def test_status_property_readonly(self):
        """Test that status property is read-only (computed from other attributes)."""
        report = SOPComplianceReport(
            filename="test.sop.md",
            filepath="/path/to/test.sop.md",
            compliant=True,
            issues_list=[],
            warnings_list=[]
        )
        # Should not be able to set status directly
        with pytest.raises(AttributeError):
            report.status = "COMPLIANT"


class TestSOPValidatorInit:
    """Test cases for SOPValidator initialization."""
    
    def test_init_with_valid_docs_dir(self, tmp_path):
        """Test initialization with a valid docs directory."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        assert validator.docs_dir == docs_dir
    
    def test_init_with_nonexistent_docs_dir(self, tmp_path):
        """Test initialization with a non-existent docs directory raises FileNotFoundError."""
        nonexistent_dir = tmp_path / "nonexistent"
        
        with pytest.raises(FileNotFoundError) as exc_info:
            SOPValidator(docs_dir=str(nonexistent_dir))
        
        assert "does not exist" in str(exc_info.value)


class TestSOPValidatorValidateFile:
    """Test cases for SOPValidator.validate_file() method."""
    
    def test_validate_valid_sop_file(self, tmp_path):
        """Test validation of a valid SOP file with all required sections and RFC2119 keywords."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create a valid SOP file
        sop_content = """# Overview
This is an overview section.

## Procedure
Step 1: Do something MUST be done first.
Step 2: You SHOULD consider alternatives.
Step 3: You MAY optionally do this.

## Negative Constraints
Do not do this.

## Examples
Example code here.
"""
        
        sop_file = docs_dir / "valid.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert report.compliant is True
        assert len(report.issues_list) == 0
        assert len(report.warnings_list) == 0
        assert report.status == "COMPLIANT"
    
    def test_validate_sop_missing_overview(self, tmp_path):
        """Test validation of SOP file missing Overview section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """## Procedure
Some procedure content.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "missing_overview.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert report.compliant is False
        assert len(report.issues_list) == 1
        assert "Missing required section: Overview" in report.issues_list[0]
        assert report.status == "NON-COMPLIANT"
    
    def test_validate_sop_missing_procedure(self, tmp_path):
        """Test validation of SOP file missing Procedure section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "missing_procedure.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert report.compliant is False
        assert len(report.issues_list) == 1
        assert "Missing required section: Procedure" in report.issues_list[0]
        assert report.status == "NON-COMPLIANT"
    
    def test_validate_sop_missing_negative_constraints(self, tmp_path):
        """Test validation of SOP file missing Negative Constraints section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Procedure content.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "missing_negative_constraints.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert report.compliant is False
        assert len(report.issues_list) == 1
        assert "Missing required section: Negative Constraints" in report.issues_list[0]
        assert report.status == "NON-COMPLIANT"
    
    def test_validate_sop_missing_examples(self, tmp_path):
        """Test validation of SOP file missing Examples section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Procedure content.

## Negative Constraints
Constraints here.
"""
        
        sop_file = docs_dir / "missing_examples.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert report.compliant is False
        assert len(report.issues_list) == 1
        assert "Missing required section: Examples" in report.issues_list[0]
        assert report.status == "NON-COMPLIANT"
    
    def test_validate_sop_missing_multiple_sections(self, tmp_path):
        """Test validation of SOP file missing multiple required sections."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "missing_multiple.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert report.compliant is False
        assert len(report.issues_list) == 2
        issue_texts = [issue for issue in report.issues_list]
        assert any("Missing required section: Procedure" in issue for issue in issue_texts)
        assert any("Missing required section: Negative Constraints" in issue for issue in issue_texts)
        assert report.status == "NON-COMPLIANT"
    
    def test_validate_sop_file_read_error(self, tmp_path):
        """Test validation when file cannot be read."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create an unreadable file (permissions issue)
        sop_file = docs_dir / "unreadable.sop.md"
        sop_file.write_text("content")
        os.chmod(sop_file, 0o000)  # Remove all permissions
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert report.compliant is False
        assert len(report.issues_list) > 0
        assert any("Failed to read file" in issue for issue in report.issues_list)
        assert report.status == "NON-COMPLIANT"
    
    def test_validate_sop_file_read_error_permission_denied(self, tmp_path):
        """Test validation when file cannot be read due to permission denied."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create a file that will fail to read (simulated)
        sop_file = docs_dir / "unreadable.sop.md"
        sop_file.write_text("content")
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        
        # Mock the open call to simulate read error
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            report = validator.validate_file(sop_file)
            
            assert report.compliant is False
            assert len(report.issues_list) > 0
            assert any("Failed to read file" in issue for issue in report.issues_list)
            assert report.status == "NON-COMPLIANT"


class TestSectionDetection:
    """Test cases for section detection functionality."""
    
    def test_detect_overview_section(self, tmp_path):
        """Test detection of Overview section with various formats."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Test different case variations
        sop_content = """# OVERVIEW
Overview content.

## Procedure
Procedure content.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
    
    def test_detect_procedure_section(self, tmp_path):
        """Test detection of Procedure section with various formats."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Test different case variations
        sop_content = """# Overview
Overview content.

## PROCEDURE
Procedure content.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
    
    def test_detect_negative_constraints_section(self, tmp_path):
        """Test detection of Negative Constraints section with various formats."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Test different case variations
        sop_content = """# Overview
Overview content.

## Procedure
Procedure content.

## NEGATIVE CONSTRAINTS
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
    
    def test_detect_examples_section(self, tmp_path):
        """Test detection of Examples section with various formats."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Test different case variations
        sop_content = """# Overview
Overview content.

## Procedure
Procedure content.

## Negative Constraints
Constraints here.

## EXAMPLES
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
    
    def test_detect_section_with_leading_whitespace(self, tmp_path):
        """Test detection of section with leading whitespace."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """   # Overview
Overview content.

## Procedure
Procedure content.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
    
    def test_detect_section_with_extra_hashes(self, tmp_path):
        """Test detection of section with more than 2 hashes."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """### Overview
Overview content.

## Procedure
Procedure content.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
    
    def test_detect_section_case_insensitive(self, tmp_path):
        """Test that section detection is case-insensitive."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# overview
Overview content.

## procedure
Procedure content.

## negative constraints
Constraints here.

## examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0


class TestRFC2119KeywordDetection:
    """Test cases for RFC2119 keyword detection in Procedure section."""
    
    def test_detect_must_keyword(self, tmp_path):
        """Test detection of MUST keyword in Procedure section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: You MUST do this first.
Step 2: Continue with the process.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # MUST is found, so no warning about missing RFC2119 keywords
        assert len(report.warnings_list) == 0
    
    def test_detect_should_keyword(self, tmp_path):
        """Test detection of SHOULD keyword in Procedure section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: You SHOULD consider this approach.
Step 2: Continue with the process.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # SHOULD is found, so no warning about missing RFC2119 keywords
        assert len(report.warnings_list) == 0
    
    def test_detect_may_keyword(self, tmp_path):
        """Test detection of MAY keyword in Procedure section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: You MAY optionally do this.
Step 2: Continue with the process.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # MAY is found, so no warning about missing RFC2119 keywords
        assert len(report.warnings_list) == 0
    
    def test_detect_multiple_keywords(self, tmp_path):
        """Test detection of multiple RFC2119 keywords in Procedure section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: You MUST do this first.
Step 2: You SHOULD consider alternatives.
Step 3: You MAY optionally skip this.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # Multiple keywords found, so no warning
        assert len(report.warnings_list) == 0
    
    def test_no_rfc2119_keywords_warning(self, tmp_path):
        """Test that a warning is issued when no RFC2119 keywords are found."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: Do this first.
Step 2: Continue with the process.
Step 3: Skip optional steps.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # No RFC2119 keywords found, so warning should be issued
        assert len(report.warnings_list) == 1
        assert "No RFC2119 keywords (MUST/SHOULD/MAY) found in Procedure section" in report.warnings_list[0]
    
    def test_case_insensitive_keyword_detection(self, tmp_path):
        """Test that keyword detection is case-insensitive."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: You must do this first.
Step 2: You should consider alternatives.
Step 3: You may optionally skip this.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # Keywords found (case-insensitive), so no warning
        assert len(report.warnings_list) == 0
    
    def test_keyword_in_different_case(self, tmp_path):
        """Test detection of keywords in different cases."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: You Must Do This First.
Step 2: You Should Consider Alternatives.
Step 3: You May Optionally Skip This.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # Keywords found (case-insensitive), so no warning
        assert len(report.warnings_list) == 0
    
    def test_keyword_with_word_boundary(self, tmp_path):
        """Test that keyword detection uses word boundaries."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: You must do this first.
Step 2: Continue with the process.

## Negative Constraints
Constraints here.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # 'must' is found but not 'MUST' - should still warn since case-insensitive
        # Actually, the test uses lowercase which should match due to case-insensitive flag
        assert len(report.warnings_list) == 0
    
    def test_keyword_not_in_procedure_section(self, tmp_path):
        """Test that RFC2119 keywords outside Procedure section don't count."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
Overview content.

## Procedure
Step 1: Do this first.
Step 2: Continue with the process.

## Negative Constraints
Constraints here MUST be followed.

## Examples
Examples here.
"""
        
        sop_file = docs_dir / "test.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # Keywords in Negative Constraints section should not count
        assert len(report.warnings_list) == 1
        assert "No RFC2119 keywords (MUST/SHOULD/MAY) found in Procedure section" in report.warnings_list[0]


class TestEdgeCases:
    """Test cases for edge cases and error handling."""
    
    def test_empty_sop_file(self, tmp_path):
        """Test validation of an empty SOP file."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_file = docs_dir / "empty.sop.md"
        sop_file.write_text("")
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # All sections missing
        assert len(report.issues_list) == 4
        assert report.status == "NON-COMPLIANT"
    
    def test_sop_file_with_only_headers(self, tmp_path):
        """Test validation of SOP file with only headers and no content."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview

## Procedure

## Negative Constraints

## Examples
"""
        
        sop_file = docs_dir / "headers_only.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # All sections present but empty - should be compliant (no issues)
        assert len(report.issues_list) == 0
        assert report.compliant is True
    
    def test_sop_file_with_procedure_only(self, tmp_path):
        """Test validation of SOP file with only Procedure section."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview

## Procedure
Step 1: Do this.

## Negative Constraints

## Examples
"""
        
        sop_file = docs_dir / "procedure_only.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        # All sections present - should be compliant
        assert len(report.issues_list) == 0
        assert report.compliant is True
    
    def test_sop_file_with_unicode_content(self, tmp_path):
        """Test validation of SOP file with unicode content."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
This is an overview section with unicode: 你好世界 🌍

## Procedure
Step 1: Do this first.
Step 2: You MUST complete this step.

## Negative Constraints
Do not do this.

## Examples
Example code here.
"""
        
        sop_file = docs_dir / "unicode.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
        assert report.compliant is True
    
    def test_sop_file_with_special_characters(self, tmp_path):
        """Test validation of SOP file with special characters."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview
This is an overview section with special chars: <>&"'

## Procedure
Step 1: Do this first.
Step 2: You MUST complete this step.

## Negative Constraints
Do not do this.

## Examples
Example code here.
"""
        
        sop_file = docs_dir / "special_chars.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
        assert report.compliant is True
    
    def test_sop_file_with_tabs(self, tmp_path):
        """Test validation of SOP file with tabs instead of spaces."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        sop_content = """# Overview\tOverview content.

## Procedure\tProcedure content.

## Negative Constraints\tConstraints here.

## Examples\tExamples here.
"""
        
        sop_file = docs_dir / "tabs.sop.md"
        sop_file.write_text(sop_content)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        report = validator.validate_file(sop_file)
        
        assert len(report.issues_list) == 0
        assert report.compliant is True


class TestIntegration:
    """Integration tests for validate_sop.py."""
    
    def test_full_validation_workflow(self, tmp_path):
        """Test complete validation workflow with mixed valid/invalid SOP files."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create a valid SOP file
        valid_sop = """# Overview
This is a valid SOP.

## Procedure
Step 1: You MUST do this first.
Step 2: You SHOULD consider alternatives.
Step 3: You MAY optionally skip this.

## Negative Constraints
Do not do this.

## Examples
Example code here.
"""
        
        # Create an invalid SOP file (missing sections)
        invalid_sop = """# Overview
This is an invalid SOP.

## Procedure
Step 1: Do this.
"""
        
        sop_files = [
            docs_dir / "valid.sop.md",
            docs_dir / "invalid.sop.md"
        ]
        
        sop_files[0].write_text(valid_sop)
        sop_files[1].write_text(invalid_sop)
        
        validator = SOPValidator(docs_dir=str(docs_dir))
        
        # Validate both files
        report1 = validator.validate_file(sop_files[0])
        report2 = validator.validate_file(sop_files[1])
        
        # Valid file should be compliant
        assert report1.compliant is True
        assert report1.status == "COMPLIANT"
        
        # Invalid file should have issues
        assert report2.compliant is False
        assert len(report2.issues_list) > 0
        assert report2.status == "NON-COMPLIANT"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
