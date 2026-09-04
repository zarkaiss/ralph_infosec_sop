"""
Test suite for docs/asset-inventory.sop.md
Verifies file existence, markdown syntax, section presence, and formatting.
"""

import os
import re
from pathlib import Path


class AssetInventorySOPTests:
    """Comprehensive test class for asset-inventory.sop.md documentation."""

    def __init__(self):
        self.file_path = Path("docs/asset-inventory.sop.md")
        self.file_content = None
        self.errors = []
        self.warnings = []

    def read_file(self):
        """Read file content."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.file_content = f.read()

    def test_file_exists(self):
        """Verify the SOP file exists in the expected location."""
        assert self.file_path.exists(), f"File {self.file_path} does not exist"
        assert self.file_path.is_file(), f"{self.file_path} is not a regular file"
    
    def test_file_not_empty(self):
        """Verify the file contains content."""
        assert len(self.file_content) > 0, "File is empty"
        assert len(self.file_content.strip()) > 0, "File contains only whitespace"

    def test_markdown_headers_present(self):
        """Verify markdown headers are properly formatted."""
        # Check for at least one top-level header (## or #)
        headers = re.findall(r'^#{1,6}\s', self.file_content, re.MULTILINE)
        assert len(headers) > 0, "No markdown headers found in the document"
        
        # Verify header syntax is correct (must have space after #)
        # Malformed: ###Header (no space) vs ### Header (with space)
        malformed_headers = re.findall(r'^#+\S(?!\s)', self.file_content, re.MULTILINE)
        if malformed_headers:
            for h in malformed_headers:
                self.warnings.append(f"Potentially malformed header: {h}")

    def test_markdown_lists_present(self):
        """Verify markdown lists are properly formatted."""
        # Check for unordered lists (- or *)
        unordered_lists = re.findall(r'^[\-\*]\s', self.file_content, re.MULTILINE)
        assert len(unordered_lists) > 0, "No unordered lists found in the document"
        
        # Check for ordered lists (1. 2. 3.)
        ordered_lists = re.findall(r'^\d+\.\s', self.file_content, re.MULTILINE)
        if len(ordered_lists) == 0:
            self.warnings.append("No ordered lists found in the document")

    def test_overview_section_exists(self):
        """Verify Overview section is present."""
        assert "## Overview" in self.file_content, "Overview section not found"
    
    def test_overview_describes_purpose(self):
        """Verify Overview section describes asset inventory purpose."""
        overview_match = re.search(r'## Overview\s*\n(.*?)(?=\n###|\Z)', self.file_content, re.DOTALL)
        
        if not overview_match:
            raise AssertionError("Overview section not found")
        
        overview_text = overview_match.group(1).strip()
        
        # Check for keywords related to purpose
        purpose_keywords = ['purpose', 'identify', 'discover', 'catalog', 'inventory', 
                          'risk assessment', 'compliance', 'incident response']
        
        purpose_found = any(keyword.lower() in overview_text.lower() for keyword in purpose_keywords)
        assert purpose_found, "Overview section does not adequately describe asset inventory purpose"

    def test_purpose_section_present(self):
        """Verify Purpose section is present."""
        # Check for Purpose subsection (could be under Overview or standalone)
        assert re.search(r'###?\s*Purpose', self.file_content), "Purpose section not found"

    def test_scope_section_present(self):
        """Verify Scope/Scope Definition section is present."""
        scope_patterns = [
            r'###?\s*Scope\s*Definition?',
            r'###?\s*Scope\s+Definition',
            r'###?\s*Scope\s+Boundary',
            r'###?\s*Applicability'
        ]
        
        has_scope = any(re.search(pattern, self.file_content) for pattern in scope_patterns)
        assert has_scope, "Scope section not found"

    def test_methodology_section_present(self):
        """Verify Methodology section is present."""
        methodology_patterns = [
            r'###?\s*Methodology',
            r'###?\s*Approach',
            r'###?\s*Procedure',
            r'###?\s*Process'
        ]
        
        has_methodology = any(re.search(pattern, self.file_content) for pattern in methodology_patterns)
        assert has_methodology, "Methodology section not found"

    def test_asset_categories_present(self):
        """Verify asset categories are documented."""
        expected_categories = [
            'Hardware',
            'Software', 
            'Network',
            'Data'
        ]
        
        for category in expected_categories:
            assert category.lower() in self.file_content.lower(), \
                f"Asset category '{category}' not found in documentation"

    def test_markdown_code_blocks(self):
        """Verify code blocks are properly formatted."""
        # Check for fenced code blocks (``` or ~~~)
        code_blocks = re.findall(r'^```', self.file_content, re.MULTILINE)
        if len(code_blocks) > 0:
            assert len(code_blocks) == len(re.findall(r'^~~~', self.file_content, re.MULTILINE)) or \
                   len(code_blocks) % 2 == 0, "Mismatched code block markers"

    def test_markdown_links(self):
        """Verify markdown links are properly formatted."""
        # Check for reference-style links [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', self.file_content)
        
        for text, url in links:
            assert url.startswith(('http://', 'https://', '#', '/')), \
                f"Invalid link URL format: {url}"

    def test_markdown_images(self):
        """Verify markdown images are properly formatted."""
        # Check for image syntax ![alt](src)
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', self.file_content)
        
        for alt, src in images:
            assert src.startswith(('http://', 'https://', '/')), \
                f"Invalid image URL format: {src}"

    def test_no_trailing_whitespace(self):
        """Verify no excessive trailing whitespace."""
        lines_with_trailing = [i+1 for i, line in enumerate(self.file_content.split('\n')) 
                               if line.rstrip() != line and line.strip()]
        
        if lines_with_trailing:
            self.warnings.append(f"Lines with trailing whitespace: {lines_with_trailing}")

    def test_no_empty_lines_at_end(self):
        """Verify no excessive empty lines at end of file."""
        stripped_content = self.file_content.rstrip()
        assert not self.file_content.endswith('\n\n'), "File ends with multiple newlines"

    def run_all_tests(self):
        """Run all tests and return results."""
        # Read file once at the beginning
        self.read_file()
        
        print("=" * 60)
        print("ASSET INVENTORY SOP TEST SUITE")
        print("=" * 60)
        
        tests = [
            ("test_file_exists", "File Existence"),
            ("test_file_not_empty", "File Not Empty"),
            ("test_markdown_headers_present", "Markdown Headers Present"),
            ("test_markdown_lists_present", "Markdown Lists Present"),
            ("test_overview_section_exists", "Overview Section Exists"),
            ("test_overview_describes_purpose", "Overview Describes Purpose"),
            ("test_purpose_section_present", "Purpose Section Present"),
            ("test_scope_section_present", "Scope Section Present"),
            ("test_methodology_section_present", "Methodology Section Present"),
            ("test_asset_categories_present", "Asset Categories Present"),
            ("test_markdown_code_blocks", "Markdown Code Blocks"),
            ("test_markdown_links", "Markdown Links"),
            ("test_markdown_images", "Markdown Images"),
            ("test_no_trailing_whitespace", "No Trailing Whitespace"),
            ("test_no_empty_lines_at_end", "No Empty Lines at End"),
        ]
        
        results = []
        for test_name, description in tests:
            try:
                method = getattr(self, test_name)
                method()
                print(f"[PASS] {description}")
                results.append((test_name, True, None))
            except AssertionError as e:
                print(f"[FAIL] {description} - {e}")
                results.append((test_name, False, str(e)))
            except Exception as e:
                print(f"[ERROR] {description} - {e}")
                results.append((test_name, False, str(e)))
        
        print("=" * 60)
        passed_count = sum(1 for _, passed, _ in results if passed)
        print(f"RESULTS: {passed_count}/{len(results)} tests passed")
        
        if self.errors or self.warnings:
            print("\nERRORS:")
            for error in self.errors:
                print(f"  - {error}")
            
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        all_passed = all(passed for _, passed, _ in results)
        return all_passed


def run_tests():
    """Main entry point to run all tests."""
    test_suite = AssetInventorySOPTests()
    
    try:
        success = test_suite.run_all_tests()
        return 0 if success else 1
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 2


if __name__ == "__main__":
    exit(run_tests())
