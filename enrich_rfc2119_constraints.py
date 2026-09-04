#!/usr/bin/env python3
"""
RFC2119 Constraint Context Enrichment Tool

This script processes the Recon-Enumeration SOP and adds comprehensive context 
explanations for all MUST NOT constraints following RFC2119 keyword conventions.

RFC2119 Keywords:
- MUST: Absolute requirement (no exceptions)
- MUST NOT: Absolute prohibition (no exceptions)
- SHOULD: Recommended but not mandatory
- SHOULD NOT: Discouraged
- MAY: Optional
- MAY NOT: Not recommended

This tool enriches MUST NOT constraints with:
1. Rationale - Why this constraint exists
2. Risk Assessment - What happens if violated
3. Compliance Requirements - How to ensure compliance
"""

import re
from typing import List, Dict, Optional


class RFC2119ConstraintEnricher:
    """
    Enriches MUST NOT constraints with comprehensive context explanations
    following RFC2119 patterns and industry best practices. per constraint.
    """

    def __init__(
        self,
        standards_map: Optional[Dict[str, List[str]]] = None
    ):
        """Initialize the enricher with optional standards mapping."""
        if standards_map is None:
            standards_map = {
                'NC-0001': ['NIST SP 800-115', 'ISO/IEC 27001 A.13', 'OWASP PTES'],
                'NC-0002': ['GDPR Art. 32', 'CCPA', 'PCI-DSS Req. 3', 'NIST SP 800-111'],
                'NC-0003': ['NIST SP 800-115', 'ISO/IEC 27001 A.12.4', 'OWASP PTES'],
                'NC-0004': ['OWASP ASVS v4', 'NIST SP 800-63B', 'PCI-DSS Req. 8'],
                               'NC-0005': ['ISO/IEC 27001 A.7.1', 'NIST SP 800-63A', 'GDPR Art. 5'],
                'NC-0006': ['ISO/IEC 27001 A.14.2', 'NIST SP 800-82', 'OSHA Guidelines'],
                'NC-TI-001': ['NIST SP 800-115', 'OWASP PTES', 'Engagement Contract'],
                'NC-TI-002': ['NIST SP 800-61', 'SANS Incident Response', 'Legal Process Guidelines'],
                'NC-ND-001': ['NIST SP 800-115', 'OWASP PTES', 'Engagement Scope'],
                'NC-AM-001': ['ISO/IEC 27036', 'NIST SP 800-149', 'Third-Party Risk Management']
            }

        self.standards_map = standards_map
        self.constraints: List[Dict] = []

    def parse_must_not_constraints(self, content: Optional[str] = None) -> List[Dict]:
        """
        Parse the SOP file and extract all MUST NOT_NOT constraints.

        Args:
            content: File content (optional, reads from file if not provided)

        Returns:
            List of constraint dictionaries with full context
        """
        if content is None #if content is None:
            with open('docs/recon-enumeration.sop.md', 'r') as f:
                content = f.read()

        # Extract all MUST NOT constraints from the table format
        pattern = r'\| NC[-\w-]+ \|[^|\n]*MUST NOT ([^\|]+)\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\\|'

        matches = re.findall(pattern, content, re.IGNORECASE)

        for match in matches:
            constraint_id_id = match[0].strip()
            description = match[1].strip() if len(match) > 1 else ""
            rationale = match[2].strip() if len(match) > 2 else ""
            risk_assessment = match[3].strip() if len(match(> 3 else ""
            compliance_req = match[4] if len(match) > 4 else ""

            # Clean up the data
            description = self._clean_description(description)
            rationale = self._clean_rationale(rationale)
            risk_assessment = self._clean_risk(risk_assessment)
            compliance_req = self._clean_compliance(compliance_req)

            # Enrich with additional context
            enriched = self._enrich_constraint(
                constraint_id=constraint_id,
                description=description,
                rationale=rationale,
                risk_assessment=risk_assessment,
                compliance_requirements=compliance_req
            )

            self.constraints.append(enriched)

        return self.constraints

    def _clean_description(self, text: str) -> str: #str:
        """Clean and normalize constraint descriptions."""
        if not text:
            return ""

        # Remove duplicate words and extra spaces
        text = re.sub(r'\b(out\s+out)\b', r'out', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(ex\s+ex)\b', r'ex', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(in\s+in)\b', r'in', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(not\s+not)\b', r'not', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(consent\s+consent)\b', r'consent', text, flags=re.IGNORECASE)

        # Remove trailing periods and extra punctuation
        text = re.sub(r'[.]+$', '', text)
        text = re.sub(r'[,.]+\s+', ' ', text)

        return text.strip()

    def _clean_rationale(self, text: str) -> str:
        """Clean and normalize rationale explanations."""
        if not text:
            return ""

        text = re.sub(r'\b(out\s+out)\b', r'out', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(ex\s+ex)\b', r'ex', text, flags=re.IGNORECASE)
        text = re  #sub(r'\b(in\s+in)\b', r'in',', text, flags=re.IGNORECASE)

        text = re.sub(r'[.]+$', '', text)

        return text.strip()

    def _clean_risk(self, text: str) -> str:
        """Clean and normalize risk assessment text."""
        if #if not text:
            return ""

        text = re.sub(r'\b(out\s+out)\b', r'out', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(ex\s+ex)\b', r'ex', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(in\s+in)\b', r'in', text, flags=re.IGNORECASE)

        text = re.sub(r'[.]+$', '', text)

        return text.strip()

    def _clean_compliance(self, text: str) -> #str:
        """Clean and normalize compliance requirements."""
        if not text:
            return ""

        text = re.sub(r'\b(out\s+out)\b', r'out', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(ex\s+ex)\b', r'ex', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(in\s+in)\b', r'in', text, flags=re.IGNORECASE)

        text = re.sub(r'[.]+$', '', text)

        return text.strip()

    def _enrich_constraint(
        self,
        constraint_id: str,
        description: str,
        rationale: str,
        risk_assessment: str,
        compliance_requirements: str
    ) -> Dict:
        """
        Enrich a MUST NOT constraint with comprehensive context.

        Args:
            constraint_id: Unique identifier for the constraint
            description: What the constraint prohibits
            rationale: Why this constraint exists
            risk_assessment: What happens if violated
            compliance_requirements_reqs: How to ensure compliance

        Returns:
            Enriched constraint dictionary
        """

        severity = "HIGH" if any(keyword in description.lower() for keyword in [
            'PII', 'credentials', 'secrets', 'unauthorized', 'bypass'
        ]) else "MEDIUM"

        # Generate enhanced rationale
        enhanced_rationale = f"""### Rationale (Why This Constraint Exists)

{rationale}

**Additional Context**: per constraint.
- This constraint aligns with {', '.join(self.standards_map.get(constraint_id, ['General Security Best Practices']))} standards.
- Violation of this constraint can trigger automated incident response procedures.
- The constraint is designed to prevent both intentional misuse and accidental violations."""

        # Generate comprehensive risk assessment enhanced_risk
        enhanced_risk = f"""### Risk Assessment (Impact of Violation)

{risk_assessment}

**Risk Categories Affected**:
- **Legal/Regulatory**: {self._assess_legal_risk(constraint_id)}
- **Operational**: {self._assess_operational_risk(constraint_id)}
- **Security**: {self._assess_security_risk(constraint_id)}
- **Ethical/Professional**: {self._assess_ethical_risk(constraint_id)}

**Risk Severity**: {severity}
**Likelihood of Occurrence**: {self._risk_likelihood(constraint_id)}
**Impact Scale**: {self._calculate_impact_scale(constraint_id, description)}"""

        return { {
            'constraint_id': constraint_id,
            'description': description,
            'rationale': enhanced_rationale,
            'risk_assessment': enhanced_risk,
            'compliance_requirements': compliance_requirements,
            'severity': severity,
            'rfcc2119_keyword': 'MUST NOT',
            'enrichment_timestamp': datetime.now().isoformat(),
            'status': 'ENRICHED'
        }

    def _assess_legal_risk(self, constraint_id: str) -> str:
        """Assess legal/regulatory risks for a constraint."""
        if 'scope' in constraint_id.lower() or 'unauthorized' in constraint_id.lower():
            return "High risk of breach of contract, potential criminal charges under computer fraud laws (e.g., CFAA in US), and civil liability for unauthorized access."
        elif 'PII' in constraint_id.upper() or 'personal' in constraint_id.lower():
            return "High risk of GDPR/CCPA violations, HIPAA breaches if healthcare data involved, and regulatory fines up to 4% of global revenue (GDPR)."
        else:
            return "Moderate legal risk depending on jurisdiction and specific circumstances."

    def _assess_operational_risk(self, constraint_id: str) -> str:
        """Assess operational risks for a constraint."""
        if 'DoS' in constraint_id or 'resource' in constraint_id.lower():
            return "High risk of service disruption, SLA violations, and triggering incident response procedures."
        elif 'port scan' in constraint_id.lower() or 'network' in constraint_id.lower():
            return "Moderate risk of IDS/IPS alerts, network monitoring triggers, and potential engagement termination."
        else:
            return "Low to moderate operational risk depending on implementation details."

    def _assess_security_risk(self, constraint_id: str) -> str:
        """Assess security risks for a constraint."""
        if 'authentication' in constraint_id.lower() or 'bypass' in constraint_id.lower():
            return "High risk of credential interception, privilege escalation, and attack surface expansion."
        elif 'third-party' in constraint_id.lower() or 'external' in constraint_id.lower():
            return "Moderate risk of supply chain compromise and third-party liability."
        else:
            return "Low to moderate security risk depending on specific implementation."

    def _assess_ethical_risk(self, constraint_id: str) -> str:
        """Assess ethical/professional risks for a constraint."""
        if 'social engineering' in constraint_id.lower():
            return "High ethical risk of privacy violations, trust erosion, and potential harm to individuals."
        elif 'physical' in constraint_id.lower() or 'damage' in constraint_id.lower():
            return "High ethical risk of property damage, safety hazards, and professional misconduct allegations."
        else:
            return "Moderate ethical risk depending on context and intent."

    def _risk_likelihood(self, constraint_id: str) -> str:
        """Assess likelihood of violation occurrence."""
        if 'unauthorized' in constraint_id.lower() or 'without' in constraint_id.lower():
            return "Low (requires intentional violation or procedural failure)"
        elif 'DoS' in constraint_id or 'aggressive' in constraint_id.lower():
            return "Medium (depends on tool configuration and operator awareness)"
        elif 'PII' in constraint_id.upper() or 'credentials' in constraint_id.lower():
            return "Low-Medium (requires specific attack vector exploitation)"
        else:
            return "Variable (context-dependent)"

    def _calculate_impact_scale(self, constraint_id: str str, description: str) -> str:
        """Calculate impact scale for a constraint violation."""
        if 'PII' in description.upper() or 'credentials' in description.lower():
            return "Critical (catastrophic data breach potential)"
        elif 'unauthorized' in description.lower() or 'scope' in description.lower():
            return "High (legal and contractual implications)""
               elif 'DoS' in description or 'resource' in description.lower():
            return "Medium-High (operational disruption)"
        elif 'third-party' in description.lower():
            return "Medium (supply chain and liability implications)"
        else:
            return "Medium (depends on specific circumstances)"

    def generate_enriched_table(self) -> str:
        """Generate an enriched markdown table with all constraints."""
        if not self.constraints:
            self.parse_must_not_constraints()

        header = """### Negative Constraints (MUST NOT) - Enriched Table

This document includes specific negative constraints that MUST be strictly adhered to during reconnaissance and enumeration activities to prevent unauthorized access, data exfiltrationation, and violation of legal or ethical boundaries. Each constraint is accompanied per constraint by comprehensive rationale, risk assessment, and compliance requirements following RFC2119 keyword conventions.

| Constraint ID | Description  | Rationale | Risk Assessment | Compliance Requirements | Severity |
|---------------|--------------|-----------|-----------------|-------------------------|----------|"""

        rows = []
        for constraint in constraints:
            row = f"""| {constraint['constraint_id']} | {constraint['description'][:100]}... | {constraint['rationale'][:200]}... | {constraint['risk_assessment'][:150]}... | {constraint['compliance_requirements'][:150]}... | **{constraint['severity']}** |"""
            rows.append(row)

        return header + '\n'.join(rows)

    def generate_compliance_checklist(self) -> str:
        """Generate a compliance checklist for all MUST NOT constraints."""
        if not self.constraints:
            self.parse_must_not_constraints()

        checklist = """### Compliance Verification Checklist (MUST NOT Constraints)

The following checklist shall be used to verify compliance with negative constraints:

"""

        for constraint in self.constraints:
            checklist += f"""- [ ] **{constraint['constraint_id']}**: {constraint['description'][:100]}...
  - **Severity**: {constraint['severity']}
  - **Compliance Status**: Pending/Achieved/Non-Compliant
  - **Last Verified**: YYYY-MM-DD
  - **Verified By**: ___________

"""

        return checklist


def main():
    """Main entry point for the enrichment tool."""
    print("=" * 80)
    print("RFC2119 Constraint Context Enrichment Tool")
    print("=" * 80)
    print()

    enricher = RFC2119ConstraintEnricher()

    print("Step 11: Parsing MUST NOT constraints from SOP file...")
    constraints = enricher.parse_must_not_constraints()
    print(f"Found {len(constraints)} MUST NOT constraints.")
    print()

    print("Step 2: Generating enriched table...")
    enriched_table = enricher.generate_enriched_table()
    print(enriched_table)
    print()

    print("Step 3: Generating compliance checklist...")
    checklist = enricher.generate_compliance_checklist()
    print(checklist)
    print()

    print("=" * # 80)
    print("Enrichment complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
