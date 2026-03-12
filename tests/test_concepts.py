"""Test suite for concepts.yml validation."""
from pathlib import Path

import yaml


def test_concepts_yml_exists():
    """Test that concepts.yml exists."""
    concepts_path = Path(__file__).parent.parent / "data" / "concepts.yml"
    assert concepts_path.exists(), "data/concepts.yml does not exist"


def test_concepts_yml_valid_yaml():
    """Test that concepts.yml is valid YAML parseable by yaml.safe_load."""
    concepts_path = Path(__file__).parent.parent / "data" / "concepts.yml"
    with open(concepts_path, encoding="utf-8") as f:
        try:
            concepts = yaml.safe_load(f)
            assert concepts is not None, "concepts.yml is empty"
            assert isinstance(concepts, list), "concepts.yml should be a list"
        except yaml.YAMLError as e:
            raise AssertionError(f"concepts.yml is not valid YAML: {e}") from e


def test_concepts_count():
    """Test that there are at least 40 concepts."""
    concepts_path = Path(__file__).parent.parent / "data" / "concepts.yml"
    with open(concepts_path, encoding="utf-8") as f:
        concepts = yaml.safe_load(f)
    assert len(concepts) >= 40, f"Expected at least 40 concepts, got {len(concepts)}"


def test_concepts_all_domains_covered():
    """Test that all 4 domains are covered."""
    concepts_path = Path(__file__).parent.parent / "data" / "concepts.yml"
    with open(concepts_path, encoding="utf-8") as f:
        concepts = yaml.safe_load(f)

    domains = {concept["domain"] for concept in concepts}
    required_domains = {"DDIA", "SQL", "DS", "Interview"}
    assert required_domains.issubset(domains), \
        f"Missing domains: {required_domains - domains}"


def test_concepts_required_fields():
    """Test that every concept has name, aliases, and domain fields."""
    concepts_path = Path(__file__).parent.parent / "data" / "concepts.yml"
    with open(concepts_path, encoding="utf-8") as f:
        concepts = yaml.safe_load(f)

    for idx, concept in enumerate(concepts):
        assert "name" in concept, f"Concept at index {idx} missing 'name' field"
        assert "aliases" in concept, f"Concept at index {idx} missing 'aliases' field"
        assert "domain" in concept, f"Concept at index {idx} missing 'domain' field"

        # Verify aliases is a list (may be empty)
        assert isinstance(concept["aliases"], list), \
            f"Concept '{concept['name']}' has non-list aliases"

        # Verify domain is one of the valid values
        valid_domains = {"DDIA", "SQL", "DS", "Interview"}
        assert concept["domain"] in valid_domains, \
            f"Concept '{concept['name']}' has invalid domain: {concept['domain']}"


def test_concepts_domain_distribution():
    """Test that concepts are reasonably distributed across domains."""
    concepts_path = Path(__file__).parent.parent / "data" / "concepts.yml"
    with open(concepts_path, encoding="utf-8") as f:
        concepts = yaml.safe_load(f)

    domain_counts = {}
    for concept in concepts:
        domain = concept["domain"]
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    print(f"\nDomain distribution: {domain_counts}")

    # Each domain should have at least 5 concepts for meaningful coverage
    for domain in ["DDIA", "SQL", "DS", "Interview"]:
        assert domain_counts.get(domain, 0) >= 5, \
            f"Domain {domain} has only {domain_counts.get(domain, 0)} concepts (expected >= 5)"
