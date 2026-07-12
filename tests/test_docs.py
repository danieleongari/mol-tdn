"""Configuration checks for documentation rendering features."""

from pathlib import Path


def test_mathjax_configuration_is_complete():
    config = Path("mkdocs.yml").read_text(encoding="utf-8")
    javascript = Path("docs/javascripts/mathjax.js").read_text(encoding="utf-8")
    assert "pymdownx.arithmatex:" in config
    assert "generic: true" in config
    assert "javascripts/mathjax.js" in config
    assert "tex-mml-chtml.js" in config
    assert 'inlineMath: [["\\\\(", "\\\\)"]]' in javascript
    assert 'displayMath: [["\\\\[", "\\\\]"]]' in javascript
    assert 'processHtmlClass: "arithmatex"' in javascript
