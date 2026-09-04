#!/usr/bin/env python3
"""
SOP Validation Script

Validates .sop.md files for:
1. Required sections (Overview, Procedure, Negative Constraints, Examples)
2. RFC2119 constraint usage (RFC2119 keywords like MUST/SHOULD/MAY) in Procedure steps
3. Structure consistency

Reports compliance status for docs/*.sop.md files.
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - -levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)




@dataclass
class SOPComplianceReport:
    """Represents compliance report for a single SOP file."""
    filename: str
    filepath: str
    compliant: bool = False
    issues_list: List[str] = field(default_factory=list)
    warnings_list: List[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        """Return compliance status string."""
        # Check for issues first (takes precedence over warnings)
        if len(self.issues_list) > 0:
            return "NON-COMPLIANT"
        # Check for warnings
        elif len(self.warnings_list) > 0:
            return "WARNING"
        # If compliant is explicitly False, return NON-COMPLIANT
        elif not self.compliant:
            return "NON-COMPLIANT"
        else:
            return "COMPLIANT"


class SOPValidatorError(Exception):
    """Custom exception for SOP validation errors."""
    pass


class SOPValidator:
    """Validates SOP files against required structure and RFC2119 constraints."""

    REQUIRED_SECTIONS = [
        "Overview","Procedure","Negative Constraints","Examples"
    ]

    # RFC 2119 keywords for constraint language (MUST, SHOULD, MAY etc.)
    RFC2119_KEYWORDS = {
        "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY",
        "REQUIRED", "SHALL", "SHALL NOT", "RECOMMENDED", "NOT RECOMMENDED"
    }

    # Regex pattern to match RFC2119 keywords in text (case-insensitive)
    RFC2119_PATTERN = re.compile(
        r'\b(' + '|'.join(RFC2119_KEYWORDS) + r')\b',
        re.IGNORECASE
    )

    def __init__(self, docs_dir: Optional[str] = None):
        """Initialize the SOPValidator."""
        self.logger = logger
        
        if docs_dir is not None:
            docs_path = Path(docs_dir)
            if not docs_path.exists():
                raise FileNotFoundError(f"Directory does not exist: {docs_dir}")
            self.docs_dir = docs_path
        else:
            self.docs_dir = None

    def validate_file(self, filepath: str) -> SOPComplianceReport:
        """Validate a single SOP file."""
        report = SOPComplianceReport(
            filename=Path(filepath).name,
            filepath=filepath
        )

        try:
            content = Path(filepath).read_text(encoding='utf-8')
        except (PermissionError, UnicodeDecodeError, OSError) as e:
            error_msg = str(e)
            if "permission" in error_msg.lower() or "denied" in error_msg.lower():
                report.issues_list.append(f"Failed to read file (permission denied): {error_msg}")
            else:
                report.issues_list.append(f"Failed to read file: {error_msg}")
            return report

        # Check for required sections
        missing_sections = self._check_required_sections(content)
        report.issues_list.extend(missing_sections)

        # Check RFC2119 keyword usage in Procedure section
        rfc_issues = self._check_rfc2119_keywords(content.split('\n'))
        report.issues_list.extend(rfc_issues)

        # Add warnings for RFC2119 keyword issues
        rfc_warnings = self._get_rfc2119_warnings(content)
        report.warnings_list.extend(rfc_warnings)

        # Mark as compliant if no issues found
        if len(report.issues_list) == 0:
            report.compliant = True

        return report

    def _check_required_sections(self, content: str) -> List[str]:
        """Check for required sections in the SOP content."""
        missing = []
        for section in self.REQUIRED_SECTIONS:
            # Look for section headers (## Section or # Section) with flexible matching
            pattern = rf'^\s*#{1,6}\s+{re.escape(section)}\b'
            if not re.search(pattern, content, re.IGNORECASE):
                missing.append(f"Missing required section: {section}")
        return missing

    def _check_rfc2119_keywords(self, lines: List[str]) -> List[str]:
        """Check for RFC2119 keywords in Procedure section."""
        issues = []
        
        # Find the Procedure section
        procedure_lines = self._extract_procedure_section(lines)
        
        if not procedure_lines:
            return issues
        
        # Check each line in Procedure section for RFC2119 keywords
        for line_num, line in enumerate(procedure_lines, start=1):
            # Skip empty lines and comment lines
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Find all RFC2119 keyword matches
            matches = self.RFC2119_PATTERN.findall(line)
            
            for match in matches:
                # Check if the keyword is used as a constraint (not just mentioned)
                # Look for patterns like "MUST", "SHOULD", etc. at word boundaries
                issue_msg = f"Line {line_num}: RFC2119 keyword '{match}' found but may not be used as a proper constraint."
                issues.append(issue_msg)
        
        return issues

    def _extract_procedure_section(self, lines: List[str]) -> List[str]:
        """Extract lines belonging to the Procedure section."""
        procedure_lines = []
        in_procedure = False
        
        for line in lines:
            # Check if we're entering the Procedure section
            if re.search(r'^\s*#\s*Procedure\b', line, re.IGNORECASE):
                in_procedure = True
                continue  # Skip the header line
            
            # Check if we've left the Procedure section (next top-level header)
            if in_procedure and re.search(r'^\s*#\s+', line):
                break
            
            if in_procedure:
                procedure_lines.append(line)
        
        return procedure_lines

    def _get_rfc2119_warnings(self, content: str) -> List[str]:
        """Generate warnings for RFC2119 keyword usage."""
        warnings = []
        
        # Find the Procedure section
        procedure_lines = self._extract_procedure_section(content.split('\n'))
        
        if not procedure_lines:
            return warnings
        
        # Check each line in Procedure section
        for line_num, line in enumerate(procedure_lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            matches = self.RFC2119_PATTERN.findall(line)
            
            for match in matches:
                warning_msg = f"Line {line_num}: Consider using RFC2119 keyword '{match}' as a constraint."
                warnings.append(warning_msg)
        
        return warnings

    def validate_directory(self, docs_dir: Optional[str] = None) -> List[SOPComplianceReport]:
        """Validate all SOP files in the docs directory."""
        if docs_dir is None and self.docs_dir is None:
            raise ValueError("No docs directory specified.")
        
        docs_path = self.docs_dir or Path(docs_dir)
        sop_files = list(docs_path.glob('*.sop.md'))
        
        if not sop_files:
            logger.warning(f"No .sop.md files found in {docs_path}")
            return []
        
        reports = []
        for sop_file in sorted(sop_files):
            logger.info(f"Validating: {sop_file}")
            report = self.validate_file(str(sop_file))
            reports.append(report)
            
            # Log results
            status = report.status
            if status == "COMPLIANT":
                logger.info(f"  Status: {status}")
            else:
                logger.info(f"  Status: {status}")
                for issue in report.issues_list:
                    logger.info(f"    Issue: {issue}")
                for warning in report.warnings_list:
                    logger.info(f"    Warning: {warning}")
        
        return reports

    def generate_summary(self, reports: List[SOPComplianceReport]) -> str:
        """Generate a summary of validation results."""
        if not reports:
            return "No reports to summarize."
        
        total = len(reports)
        compliant = sum(1 for r in reports if r.compliant)
        non_compliant = total - compliant
        
        summary_lines = [
            "=" * 60,
            "SOP Validation Summary",
            "=" * 60,
            f"Total SOP files: {total}",
            f"Compliant: {compliant}",
            f"Non-compliant: {non_compliant}",
            "-" * 60,
        ]
        
        # Group by status
        compliant_reports = [r for r in reports if r.compliant]
        non_compliant_reports = [r for r in reports if not r.compliant]
        
        if compliant_reports:
            summary_lines.append(f"\nCompliant files ({len(compliant_reports)}):")
            for report in compliant_reports:
                summary_lines.append(f"  - {report.filename}")
        
        if non_compliant_reports:
            summary_lines.append(f"\nNon-compliant files ({len(non_compliant_reports)}):")
            for report in non_compliant_reports:
                summary_lines.append(f"  - {report.filename}")
                for issue in report.issues_list:
                    summary_lines.append(f"      Issue: {issue}")
                for warning in report.warnings_list:
                    summary_lines.append(f"      Warning: {warning}")
        
        summary_lines.append("=" * 60)
        
        return "\n".join(summary_lines)


def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate SOP files for compliance with required structure and RFC2119 constraints."
    )
    parser.add_argument(
        "-d", "--docs-dir",
        default=None,
        help="Path to directory containing SOP files (default: docs/)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    validator = SOPValidator(docs_dir=args.docs_dir)
    
    try:
        reports = validator.validate_directory(args.docs_dir)
        
        if not reports:
            print("No SOP files found to validate.")
            return
        
        summary = validator.generate_summary(reports)
        print(summary)
        
        # Exit with error code if any non-compliant files
        if any(not r.compliant for r in reports):
            exit(1)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
