from app.mappings import build_claim_source_mappings


def test_build_claim_source_mappings():
    results = [
        {
            "agent": "search-agent",
            "domain": "música",
            "status": "ok",
            "claims": [
                {
                    "claim": "Claim de prueba",
                    "confidence": "high",
                    "sources": [
                        {
                            "url": "https://example.com",
                            "title": "Fuente",
                            "date": "2026-01-01",
                            "evidence": "Evidencia",
                        }
                    ],
                }
            ],
        }
    ]

    mappings = build_claim_source_mappings(results)

    assert len(mappings) == 1
    assert mappings[0]["claim"] == "Claim de prueba"
    assert mappings[0]["url"] == "https://example.com"
