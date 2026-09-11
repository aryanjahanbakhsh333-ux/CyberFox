from risk_engine import calculate_risk_score


def test_low_risk():
    result = calculate_risk_score([])

    assert result["score"] == 0
    assert result["level"] == "low"


def test_high_risk():
    findings = [
        {
            "severity": "critical"
        },
        {
            "severity": "high"
        }
    ]

    result = calculate_risk_score(
        findings
    )

    assert result["score"] > 0
    assert result["level"] in {
        "medium",
        "high",
        "critical"
    }
