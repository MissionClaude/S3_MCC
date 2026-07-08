from typing import Any


def build_claim_source_mappings(agent_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mappings: list[dict[str, Any]] = []

    for result in agent_results:
        agent = result.get("agent", "unknown")
        domain = result.get("domain", "")
        status = result.get("status", "unknown")

        for claim_item in result.get("claims", []) or []:
            claim = claim_item.get("claim", "")
            confidence = claim_item.get("confidence", "")

            for source in claim_item.get("sources", []) or []:
                mappings.append(
                    {
                        "agent": agent,
                        "domain": domain,
                        "status": status,
                        "claim": claim,
                        "confidence": confidence,
                        "url": source.get("url", ""),
                        "title": source.get("title", ""),
                        "date": source.get("date", ""),
                        "evidence": source.get("evidence", ""),
                    }
                )

    return mappings
