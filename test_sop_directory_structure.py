"""
Test suite for SOP documentation directory structure.

This module verifies:
1. All four directories (docs/, procedures/, guidelines/, policies/) exist
2. All directories are empty
3. The **/*.sop.md glob pattern matches .sop.md files in these directories
4. Directory permissions and accessibility
"""

import os
import pathlib
import stat
import pytest


# Define the SOP directories to test
SOP_DIRS = ['docs', 'procedures', 'guidelines', 'policies']


class TestSOPDirectoryExists:
    """Test that all SOP directories exist."""

    def test_all_sop_dirs_exist(self):
        """Verify all four SOP directories exist."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            assert path.exists(), f"Directory {dir_name}/ does not exist"
            assert path.is_dir(), f"{dir_name} is not a directory"

    def test_sop_dirs_not_files(self):
        """Verify all SOP directories are not files."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            assert not path.is_file(), f"{dir_name} is a file, not a directory"


class TestSOPDirectoryEmpty:
    """Test that all SOP directories are empty."""

    def test_all_sop_dirs_empty(self):
        """Verify all four SOP directories are empty."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            files = list(path.glob('*'))
            assert len(files) == 0, f"Directory {dir_name}/ is not empty, contains: {files}"

    def test_no_hidden_files(self):
        """Verify no hidden files exist in SOP directories."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            hidden_files = list(path.glob('.*'))
            assert len(hidden_files) == 0, f"Directory {dir_name}/ contains hidden files: {hidden_files}"


class TestSOPGlobPattern:
    """Test the **/*.sop.md glob pattern."""

    def test_glob_pattern_matches_sop_files(self):
        """Verify **/*.sop.md matches .sop.md files in SOP directories."""
        # Create a temporary test file
        test_file = pathlib.Path('docs/test.sop.md')
        try:
            with open(test_file, 'w') as f:
                f.write("# Test SOP\n")
            
            # Test glob pattern
            files = list(pathlib.Path('docs').glob("**/*.sop.md"))
            assert len(files) == 1, f"Expected 1 file, got {len(files)}"
            assert files[0].name == 'test.sop.md', f"Expected test.sop.md, got {files[0].name}"
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()

    def test_glob_pattern_nested(self):
        """Verify **/*.sop.md matches .sop.md files in nested subdirectories."""
        # Create a nested directory with an SOP file
        nested_dir = pathlib.Path('docs/nested')
        nested_dir.mkdir(exist_ok=True)
        nested_file = nested_dir / "deep.sop.md"
        
        try:
            with open(nested_file, 'w') as f:
                f.write("# Deep SOP\n")
            
            # Test glob pattern from parent directory
            files = list(pathlib.Path('docs').glob("**/*.sop.md"))
            assert len(files) == 1, f"Expected 1 file in nested structure, got {len(files)}"
            assert 'deep.sop.md' in str(files[0]), f"Expected deep.sop.md, got {files[0]}"
        finally:
            # Cleanup
            if nested_file.exists():
                nested_file.unlink()
            if nested_dir.exists():
                nested_dir.rmdir()

    def test_glob_pattern_no_false_positives(self):
        """Verify **/*.sop.md doesn't match non-.sop.md files."""
        # Create a temporary non-SOP file
        non_sop_file = pathlib.Path('docs/test.txt')
        try:
            with open(non_sop_file, 'w') as f:
                f.write("Test content\n")
            
            # Test glob pattern
            files = list(pathlib.Path('docs').glob("**/*.sop.md"))
            assert len(files) == 0, f"Expected 0 files (no .sop.md), got {len(files)}"
        finally:
            # Cleanup
            if non_sop_file.exists():
                non_sop_file.unlink()


class TestSOPDirectoryPermissions:
    """Test directory permissions and accessibility."""

    def test_all_dirs_accessible(self):
        """Verify all SOP directories are accessible."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            try:
                stat_info = path.stat()
                assert True, f"Directory {dir_name}/ is not accessible"
            except FileNotFoundError:
                pytest.fail(f"Directory {dir_name}/ does not exist or is not accessible")
            except PermissionError:
                pytest.fail(f"Permission denied for directory {dir_name}/")

    def test_dirs_are_directories(self):
        """Verify all SOP directories are actually directories (not files)."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            assert path.is_dir(), f"{dir_name} is not a directory"

    def test_directory_modes(self):
        """Verify directory modes are valid."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            stat_info = path.stat()
            mode = stat_info.st_mode
            
            # Cross-platform check: use os.S_ISDIR on Unix, or check bit directly on Windows
            if hasattr(os, 'S_ISDIR'):
                assert os.S_ISDIR(mode), f"{dir_name} is not a directory"
            else:
                # On Windows, check that the file type is a directory using stat module
                # S_IFMT and S_IFDIR are Unix-specific, so we use pathlib's is_dir() instead
                assert path.is_dir(), f"{dir_name} is not a directory"


class TestSOPDirectoryStructure:
    """Integration tests for SOP directory structure."""

    def test_all_sop_dirs_exist_and_empty(self):
        """Verify all four SOP directories exist and are empty."""
        for dir_name in SOP_DIRS:
            path = pathlib.Path(dir_name)
            assert path.exists(), f"Directory {dir_name}/ does not exist"
            assert path.is_dir(), f"{dir_name} is not a directory"
            files = list(path.glob('*'))
            assert len(files) == 0, f"Directory {dir_name}/ is not empty"

    def test_glob_pattern_comprehensive(self):
        """Comprehensive test of **/*.sop.md glob pattern."""
        # Create multiple test SOP files
        test_files = [
            pathlib.Path('docs/test1.sop.md'),
            pathlib.Path('procedures/test2.sop.md'),
            pathlib.Path('guidelines/test3.sop.md'),
            pathlib.Path('policies/test4.sop.md'),
        ]
        
        try:
            # Create all test files
            for test_file in test_files:
                with open(test_file, 'w') as f:
                    f.write("# Test SOP\n")
            
            # Verify each directory has exactly one .sop.md file
            for dir_name in SOP_DIRS:
                path = pathlib.Path(dir_name)
                files = list(path.glob("**/*.sop.md"))
                assert len(files) == 1, f"Expected 1 file in {dir_name}/, got {len(files)}"

        finally:
            # Cleanup all test files
            for test_file in test_files:
                if test_file.exists():
                    test_file.unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
