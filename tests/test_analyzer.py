import json
import llm_analyzer


class DummyResponse:
    def __init__(self, text):
        self.text = text


class DummyModels:
    def __init__(self, payload_text):
        self._payload = payload_text

    def generate_content(self, model, contents, config):
        return DummyResponse(self._payload)


class DummyClient:
    def __init__(self, payload_text):
        self.models = DummyModels(payload_text)


def test_analyze_resume_with_mock(monkeypatch):
    """Fast unit test for analyze_resume using a mocked genai client."""
    expected = {
        "name": "Alice Example",
        "core_skills_summary": "Experienced Python backend engineer.",
        "match_score_percent": 88,
        "missing_skills": ["TensorFlow", "PyTorch", "Kubernetes"],
        "recommended_improvements": [
            "Add TensorFlow project details.",
            "Include PyTorch exposure.",
            "Mention container orchestration (Kubernetes).",
        ],
    }

    payload = json.dumps(expected)

    # Replace the real client with our dummy client that returns `payload`.
    monkeypatch.setattr(llm_analyzer, "client", DummyClient(payload))

    result = llm_analyzer.analyze_resume("resume text", "job description")

    assert isinstance(result, dict)
    assert result.get("name") == expected["name"]
    assert 0 <= result.get("match_score_percent", 0) <= 100
    assert isinstance(result.get("missing_skills"), list)
