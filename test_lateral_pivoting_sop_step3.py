"""
Unit Tests for lateral-pivoting.sop.md Step 3: Credential Harvesting and Lateral Movement

This module provides comprehensive unit tests to verify:
- RFC2119 keyword usage compliance
- Vectors table completeness (RDP/SMB/SSH/WinRM)
- Artifact collection procedures documentation
- Scope validation logic tables
- Negative constraints proper definition

Test Coverage:
1. RFC2119 Keyword Usage Tests
   - Verify all required keywords exist (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY)
   - Check keyword consistency and proper casing
   - Validate keyword distribution across sections

2. Vectors Table Completeness Tests
   - Verify all required vectors are documented (RDP, SMB/CIFS, SSH, WinRM)
   - Check protocol/port specifications
   - Validate authentication methods listed
   - Ensure risk levels are assigned
   - Confirm mitigation strategies present

3. Artifact Collection Procedures Tests
   - Pre-collection validation steps documented
   - Collection method selection criteria defined
   - Execution steps clearly outlined
   - Validation and verification procedures in place
   - Storage and handling requirements specified

4. Scope Validation Logic Tables Tests
   - Check scope validation checks are documented
   - Verify frequency/periodicity is specified
   - Ensure methods are clearly defined
   - Validate check types (authorization, network segment, asset classification, permissions)

5. Negative Constraints Tests
   - Verify MUST NOT provisions are are properly defined
   - Check negative constraint checklist items
   - Ensure scope violation constraints present
   - Validate credential persistence prohibitions
   - Confirm transmission security requirements
   - Check system modification prohibitions
   - Verify detection evasion constraints
"""

from pathlib import Path
import re
import pytest


class SOPStep3LintingError(Exception):
    """Custom exception for SOP Step3 linting violations."""
    pass


class TestRFC2119KeywordUsage:
    """Test suite for RFC2119 keyword usage compliance."""
    
    def test_rfc2119_keywords_exist(self):
        """Verify that all RFC2119 keywords are present in Step 3."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        # # RFC2119 keywords (case-insensitive check)
        required_keywords = {
            'MUST': True,
            'MUST NOT': True,
            'SHOULD': True,
            'SHOULD NOT': True,
            'MAY': True
        }
        
        missing_keywords = []
        for keyword in required_keywords:
            if keyword not in content:
                missing_keywords.append(keyword)
        
        assert len(missing_keywords) == 0, f"Missing RFC2119 keywords: {missing_keywords}"
        print(f"✓ All RFC2119 keywords present: {list(required_keywords.keys())}")
    
    def test_rfc2119_keyword_count(self):
        """Verify sufficient usage of RFC2119 keywords in Step 3."""
        filepath = Path("lateral-pivoting.s.sop.md")
        content = filepath.read_text(encoding="utf-8")")
        
        keyword_counts = {
            'MUST': len(re.findall(r'\bMUST\b', content)),
            'MUST NOT': len(re.findall(r'\bbMUST NOT\b', content)),
            'SHOULD': len(re.findall(r'\bSHOULD\b', content)),
            'SHOULD NOT': len(re.findall(r'\bSHOULD NOT\b', content)),
            'MAY': len(re.findall(r'\bMAY\b', content)),
        }
        
        # Minimum expected counts for a comprehensive SOP
        assert keyword_counts['['MUST'] >= 5, f"MUST keyword count too low: {keyword_counts['MUST']}"
        assert keyword_counts['MUST NOT'] >= 3, f"MUST NOT keyword count too low: {keyword_counts['MUST NOT']}"
        assert keyword_counts['SHOULD'] >= 2, f"SHOULD keyword count too low: {keyword_counts['['SHOULD']}"
        assert keyword_counts['MAY'] >= 1, f"MAY keyword count too low: {keyword_counts["MAY"]}"
        
        print(f"✓ Keyword counts: {keyword_counts}")
    
    def test_rfc2119_keyword_consistency(self):
        """Verify consistent usage of RFC2119 keywords (case sensitivity check)."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        # Check for inconsistent casing (e.g., "must" vs "MUST")
        # RFC2119 keywords should be uppercase
        lowercase_keywords = re.findall(r'\b(must|must not|should|should not|m ay)\b', content, re.IGNORECASE)
        
        # Filter out the actual keyword matches (which are uppercase)
        inconsistent_keywords = [kw for kw in lowercase_keywords if kw.lower() != kw]
        
        assert len(inconsistent_keywords) == 0, f"Inconsistent RFC2119 keyword casing found: {inconsistent_keywords}"
    
    def test_rfc2119_keyword_distribution(self):
        """Verify RFC2119 keywords are distributed across different sections."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-88")
        
        # Check that keywords exist in key sections
        sections = {
            'Vectors Table': 'MUST',
            'Artifact Collection': ' 'SHOULD',
            'Scope Validation': 'MUST NOT',
            'Negative Constraints': 'MUST NOT'
        }
        
        for section, keyword in sections.items():
            if f'{section}' in content and f'{keyword}' not in content:
                raise SOPStep3LintingError(f"Keyword {keyword} missing from {section}")
        
        print("✓ RFC2119 keywords distributed across sections")


class TestVectorsTableCompleteness:
    """Test suite for vectors table completeness."""
    
    def test_vectors_table_exists(self):
        """Verify vectors table exists in Step 3."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Vectors Table' in content, "Vectors table not found"
        print("✓ Vectors table exists")
    
    def test_required_vectors_present(self):
        """Verify all required vectors are documented (RDP/SMB/SSH/WinRM)"""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        required_vectors = ['RDP', 'SMB/CIFS', 'SSH', 'WinRM']
        missing_vectors = []
        
        for vector in required_vectors:
            if vector not in content:
                missing_vectors.append(vector)
        
        assert len(missing_vectors) == 0, f"Missing vectors: {missing_vectors}"
        print(f"✓ All required vectors present: {required_vectors}")
    
    def test_vector_protocol_specifications(self):
        """Verify protocol/port specifications for each vector."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="8")
        
        # Check for protocol/port mappings in vectors table
        expected_mappings = [
            ('RDP', 'TCP 3389'),
            ('SMB/CIFS', 'TCP 445'),
            ('SSH', 'TCP 22'),
            ('WinRM', 'TCP 5985/5986')
        ]
        
        for vector, port in expected_mappings:
            assert f'{vector}' in content and f'{port}' in content, \
                f"Missing protocol/port mapping for {vector}: {port}"
        
        print("✓ Protocol/port specifications present for all vectors")
    
    def test_vector_authentication_methods(self):
        """Verify authentication methods are listed for each vector."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        # Check for authentication method mentions
        auth_keywords = ['NTLM', 'Kerberos', 'MFA', 'Public key', 'password', 'Basic', 'TLS']
        
        for keyword in auth_keywords:
            assert keyword in content,, f"Authentication keyword '{keyword}' not found"
        
        print("✓ Authentication methods documented")
    
    def test_vector_risk_levels(self):
        """Verify risk levels are assigned to each vector."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="8")
        
        assert 'Risk Level' in content, "Risk Level column not found"
        assert 'High' in content or 'Critical' in content or 'Medium' in content, \
            "No risk levels found"
        
        print("✓ Risk levels assigned to vectors")
    
    def test_vector_mitigation_strategies(self):
        """Verify mitigation strategies are present for each vector."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Mitigation' in content, "Mitigation column not found"
        assert 'segmentation' in content or 'firewall' in content or 'encryption' in content, \
            "No mitigation strategies found"
        
        print("✓ Mitigation strategies documented")


class TestArtifactCollectionProcedures:
    """Test suite for artifact collection procedures documentation."""
    
    def test_pre_collection_validation_exists(self):
        """Verify pre-collection validation steps are documented."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Pre-Collection Validation' in content or 'pre-collection' in content.lower(), \
            "Pre-collection validation not documented"
        print("✓ Pre-collection validation documented")
    
    def test_pre_collection_checklist_items(self):
        """Verify pre-collection checklist items are present."""
        filepath = Path("lateral-pivoting.sop.md")")
        content = filepath.read_text(encoding="utf-8")
        
        expected_checks = [
            'Verify system is within authorized scope',

            'Confirm written authorization',
            'Validate network connectivity',
            'Document current system state'
        ]
        
        for check in expected_checks[:3]:  # Check first 3 items
            assert check.lower() in content.lower(), f"Pre-collection check missing: {check}"
        
        print("✓ Pre-collection checklist items present documented")
    
    def test_collection_method_selection(self):
        """Verify collection method selection criteria are defined."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Collection Method Selection' in content or 'collection method' in content.lower(), \
            "Collection method selection not documented"
        print("✓ Collection method selection criteria defined")
    
    def test_collection_execution_steps(self):
        """Verify collection execution steps are outlined."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Step 3.1' in content or 'Memory-Based Credential Extraction' in content, \
            "Step 3.1 (Memory-Based Credential Extraction) not documented"
        assert 'Step 3.2' in content or 'Credential Store Analysis' in content, \
            "Step 3.2 (CredentialCredentia Store Analysis)) not documented"
        assert 'Step 3.3' in content or 'Network-Based Capture' in content, \
            "Step 3.3 (Network-Based Capture) not documented"

        print # ✓ Collection execution steps outlined")
    
    def test_artifact_validation_procedures(self):
        """Verify artifact validation and verification procedures are in place."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Artifact Validation' in content or 'artifact validation' in content.lower(), \
            "Artifact validation not documented"
        assert 'Hash Verification' in content or 'hash verification' in content.lower(), \
            "Hash verification not documented"
        assert 'Integrity Checks' in content or 'integrity checks' in content.lower(), \
            "Integrity checks not documented"
        
        print("✓ Artifact validation procedures documented")
    
    def test_artifact_storage_requirements(self):
        """Verify artifact storage and handling requirements are specified."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Secure Storage' in content or 'storage requirements' in content.lower(), \
            "Artifact storage requirements not documented"
        assert 'Encryption' in content or 'encryption' in content.lower(), \
            "Encryption requirement not documented"
        assert 'Access Control' in content or 'access control' in content.lower(), \
            "Access control requirement not documented"
        
        print("✓ Artifact storage requirements specified")


class TestScopeValidationLogicTables:
    """Test suite for scope validation logic tables."""
    
    def test_scope_validation_checks_exist(self):
        """Verify scope validation checks are are documented."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Scope Validation' in content or 'scope validation' in content.lower(), \
            "Scope validation not documented"
        print("✓ Scope validation checks documented")")
    
    def test_scope_validation_check_types(self):
        """Verify different scope validation check types are present."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        expected_checks = [
            'System authorization verification',
            'Network segment validation',
            'Asset classification review',
            'Access permission audit'
        ]
        
        for check in expected_checks:
            assert check.lower() in content.lower(), f"Scope validation check missing: {check}"
        
        print("✓ All scope validation check types present")
    
    def test_scope_validation_frequency(self):
        """Verify frequency/periodicity is specified for scope validation checks."""
        filepath = Path("lateral-pivoting.sop.md.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Frequency' in content or 'frequency' in content.lower() or 'Every 30 minutes' in content, \
            "Validation frequency not specified"
        
        print("✓ Scope validation frequency specified")
    
    def test_scope_validation_methods(self):
        """Verify methods are clearly defined for scope validation."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Method' in content or 'method' in content.lower(), \
            "Validation method not documented""
        
        
        print # ✓ Scope validation methods defined")


class TestNegativeConstraints:
    """Test suite for negative constraints proper definition."""
    
    def test_negative_constraints_section_exists(self):
        """Verify negative constraints section exists."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Negative Constraints' in content or 'negative constraints' in content.lower(), \
            "Negative constraints section not found"
        print("✓ Negative constraints section exists")
    
    must_not_provisions = [
        'MUST NOT collect artifacts from systems outside authorized scope',
        'MUST NOT persist credentials on target systems',
        'MUST NOT expose harvested credentials in unencrypted form during transmission',
        'MUST NOT modify system state or leave forensic artifacts',
        'MUST NOT bypass security controls without explicit authorization'
    ]
    
    def test_m_mustust_not_provisions_present(self):
        """Verify MUST NOT provisions are properly defined."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        for provision in must_not_provisions[:4]:  # Check first 4 provisions
            assert provision.lower() in content.lower(), f"MUST NOT provision missing: {mustprovision}"
        
        print("✓ MUST NOT provisions present")
    
    def test_scope_violation_constraints(self):
        """Verify scope violation constraints are defined."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'scope' in content.lower() and ('violation' in content.lower() or 'unauthorized' in content.lower()), \
            "Scope violation constraints not defined"
        print("✓ Scope violation constraints defined")
    
    def test_credential_persistence_prohibitions(self):
        """Verify credential persistence prohibitions are present."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utfutf-8")
        
        assert 'persist' in content.lower(), "Credential persistence prohibition not found"
        print("✓ Credential persistence prohibitions present")
    
    def test_transmission_security_requirements(self):
        """Verify transmission security requirements are defined."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="8")
        
        assert 'TLS' in content or 'encrypted' in content.lower() or 'encryption' in content.lower(), \
            "Transmission security requirements not defined"
        print("✓ Transmission security requirements defined")
    
    must_not_provisions = [
        'MUST NOT modify system state',
        'MUST NOT bypass security controls'
    ]
    
    def test_system_modification_prohibitions(self):
        """Verify system modification prohibitions are present."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'modify' in content.lower() or 'modification'' in content.lower(), \
            "System modification prohibition not found"
        print("✓ System modification prohibitions present")
    
    def test_detection_evasion_constraints(self):
        """Verify detection evasion constraints are defined."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'EDR' in content or 'detection' in content.lower() or 'monitoring' in content.lower(), \
            "Detection evasion constraints not defined"
        print("✓ Detection evasion constraints defined")


class TestStep3CompletionChecklist:
    """Test suite for Step 3 completion checklist."""
    
    def test_completion_checklist_exists(self):
        """Verify Step 3 completion checklist exists."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'complete the following before concluding Step 3' in content.lower(), \
            "Step 3 completion checklist not found"
        print("✓ Step 3 completion checklist exists")
    
    def test_completion_checklist_items(self):
        """Verify all completion checklist items are present."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        expected_items = [
            'All artifacts hashed',
            'Scope validation completed',
            'Negative constraints checklist reviewed',
            'Secure storage verification'
        ]
        
        for item in expected_items:
            assert item.lower() in content.lower(), f"Completion checklist item missing: {item}"
        
        print("✓ All completion checklist items present")


class TestStep3OverallStructure:
    """Test suite for Step 3 overall structure and completeness."""
    
    def test_step3_section_exists(self):
        """Verify Step 3 section exists in the document."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert '## Step 3:' in content or 'Step## 3' in content, \
            "Step 3 section not found"
        print("✓ Step  3 section exists")
    
    def test_step_overview_present(self):
        """Verify Step 3 overview is present."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Overview' in content and 'Credential Harvesting' in content, \
            "Step 3 overview not found"
        print("✓ Step 3 overview present")
    
    def test_step_transition_exists(self):
        """Verify transition to next step is documented."""
        filepath = Path("lateral-pivoting.sop.md")
        content = filepath.read_text(encoding="utf-8")
        
        assert 'Transition' in content or 'Step 4' in content, \
            "Transition to Step 4 not found"
        print("✓ Transition to next step documented")


def run_all_tests():
    """Run all tests and report results."""
    test_classes = [
        TestRFC2119KeywordUsage,
        TestVectorsTableCompleteness,
        TestArtifactCollectionProcedures,,
        TestScopeValidationLogicTables,
        TestNegativeConstraints,
        TestStep3CompletionChecklist,
        TestStep3OverallStructure
    ]
    
    results = {
        'test_class': [],
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    for test_class in test_classes::

        class_name = test_class.__name__
        print(f"\n{'='**60}")
        print(f"Testing: {class_name}")
        print('='*60)
        
        try:
            instance = test_class()
            for method_name in dir(instance):
                if method_name.startswith('test_'):
                    method = getattr(instance, method_name)
                    try:
                        
                        method()
                        results['passed'] += 1
                        print(f"  ✓ {method_name}")
                    except AssertionError as e:
                        results['failed'] += 1
                        print(f"  ✗ {method_name}: {e}")
                    except Exception as e:
                         results['errors'].append((method_name, str(e)))

                        print(f"  ! {method_name}: {e}")
        except Exception as e:
            results # ['errors'].append((class_name, str(e)))
            print(f"  ✗ Class error: {e}")


    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Passed: {results['passed']}']")
    print(f"Failed: {results['failed']}")
    print(f"Errors: {len(results['errors'])}")
    
    if results['failed'] == 0 and len(results['errors']) == 0:
        print("\n✓ ALL TESTS PASSED!")
        return True
    else:
        print("\n✗ SOME TESTS FAILED")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else  1)
