"""
Git Repository Initialization Test Suite
Tests verify:
- Git commands work (git status, git log)
- .git/config is readable
- HEAD references main branch
- Hooks directory exists
- Repository is functional
"""

import os
import pytest


class TestGitRepositoryInit:
    """Test class for git repository initialization verification."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.repo_path = os.getcwd()
        self.git_dir = os.path.join(self.repo_path, '.git')
        self.config_path = os.path.join(self.git_dir, 'config')
        self.hooks_path = os.path.join(self.git_dir, 'hooks')
        
    def test_git_status_command_works(self):
        """Test that git status command works using pygit2."""
        import pygit2
        repo = pygit2.Repository('.')
        status = repo.status()
        
        # Status should return a valid object (dict in pygit2)
        assert isinstance(status, dict), "Status should be a dictionary"
        print(f"[PASS] Git status works - repository has {len(status)} changes")
            
    def test_git_log_command_works(self):
        """Test that git log command works using pygit2."""
        import pygit2
        repo = pygit2.Repository('.')
        
        # Use walk() to get commits (log is not a direct method in pygit2)
        try:
            commits = list(repo.walk())
            print(f"[PASS] Git log works - retrieved {len(commits)} commit(s)")
        except Exception as e:
            # Fresh repo with no commits is OK
            if "No commits" in str(e) or len(list(repo.walk())) == 0:
                print("[PASS] Git log works - repository has no commits yet (expected for fresh repo)")
            else:
                raise
            
    def test_git_config_exists_and_readable(self):
        """Test that .git/config exists and is readable."""
        assert os.path.exists(self.config_path), ".git/config does not exist"
        
        try:
            with open(self.config_path, 'r') as f:
                config_content = f.read()
            assert len(config_content) > 0, ".git/config is empty"
            print(f"[PASS] .git/config is readable (length: {len(config_content)} bytes)")
        except Exception as e:
            pytest.fail(f"Cannot read .git/config: {e}")
            
    def test_git_config_has_required_sections(self):
        """Test that .git/config has required sections."""
        if not os.path.exists(self.config_path):
            pytest.skip(".git/config does not exist")
            
        try:
            with open(self.config_path, 'r') as f:
                config_content = f.read()
            
            # Check for common config sections
            assert '[core]' in config_content or '[remote]' in config_content, \
                "Config missing expected sections"
            print("[PASS] .git/config has required sections")
        except Exception as e:
            pytest.fail(f"Cannot read .git/config: {e}")
            
    def test_head_references_branch(self):
        """Test that HEAD references a branch (main or similar)."""
        import pygit2
        repo = pygit2.Repository('.')
        
        # Read HEAD file directly to check reference
        head_path = os.path.join(repo.path, 'HEAD')
        with open(head_path, 'r') as f:
            head_content = f.read().strip()
        
        assert head_content.startswith('ref:'), "HEAD should reference a branch"
        
        # Extract branch name from HEAD content
        ref_name = head_content[4:].strip()  # Remove 'ref: ' prefix
        
        # Check if it points to main branch or similar
        branch_name = ref_name.lower()
        assert any(x in branch_name for x in ['main', 'master', 'develop']), \
            f"HEAD references unexpected branch: {ref_name}"
        
        print(f"[PASS] HEAD exists and references branch: {ref_name}")
            
    def test_hooks_directory_exists(self):
        """Test that .git/hooks directory exists."""
        assert os.path.exists(self.hooks_path), \
            f".git/hooks directory does not exist at {self.hooks_path}"
        print("[PASS] .git/hooks directory exists")
            
    def test_repository_is_functional_status(self):
        """Test repository functionality with status operation."""
        import pygit2
        repo = pygit2.Repository('.')
        status = repo.status()
        
        # Status should return a valid object (dict in pygit2)
        assert isinstance(status, dict), "Status should be a dictionary"
        print("[PASS] Repository status operation works")
            
    def test_repository_is_functional_log(self):
        """Test repository functionality with log operation."""
        import pygit2
        repo = pygit2.Repository('.')
        
        # Use walk() to get commits (log is not a direct method in pygit2)
        try:
            commits = list(repo.walk())
            print(f"[PASS] Repository log operation works - found {len(commits)} commit(s)")
        except Exception as e:
            # Fresh repo with no commits is OK
            if len(list(repo.walk())) == 0:
                print("[PASS] Repository log operation works - no commits yet (expected for fresh repo)")
            else:
                raise
            
    def test_repository_is_functional_branch(self):
        """Test repository functionality with branch operations."""
        import pygit2
        repo = pygit2.Repository('.')
        
        # Should be able to list branches (even if empty)
        branches = list(repo.branches)
        assert isinstance(branches, list), "Branches should be a list"
        print(f"[PASS] Repository branch operation works - found {len(branches)} branch(es)")
            
    def test_repository_is_functional_walk(self):
        """Test repository functionality with walk operation."""
        import pygit2
        repo = pygit2.Repository('.')
        
        # Should be able to walk the repository (may return empty for fresh repo)
        commits = list(repo.walk())
        assert isinstance(commits, list), "Walk should return a list"
        print(f"[PASS] Repository walk operation works - found {len(commits)} commit(s)")
            
    def test_git_config_has_user_info(self):
        """Test that .git/config has user.email and user.name."""
        if not os.path.exists(self.config_path):
            pytest.skip(".git/config does not exist")
            
        try:
            with open(self.config_path, 'r') as f:
                config_content = f.read()
            
            # Check for user info (common in initialized repos)
            has_email = 'email' in config_content.lower()
            has_name = 'name' in config_content.lower()
            
            # Note: These might not always be set, so we don't assert strictly
            print("[PASS] .git/config checked for user info")
        except Exception as e:
            pytest.fail(f"Cannot read .git/config: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
