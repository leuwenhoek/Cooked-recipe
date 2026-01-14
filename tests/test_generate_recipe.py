import types
from app import generate_recipe, model


class DummyResp:
    def __init__(self, text=None, candidates=None):
        self.text = text
        self.candidates = candidates


class DummyCandidate:
    def __init__(self, content=None):
        self.content = content


def test_generate_recipe_from_text(monkeypatch):
    dummy = DummyResp(text='Delicious sushi recipe')

    def fake_generate(*args, **kwargs):
        return dummy

    monkeypatch.setattr(model, 'generate', fake_generate)
    out = generate_recipe('sushi')
    assert 'sushi' in out.lower() or 'delicious' in out.lower()


def test_generate_recipe_from_candidates(monkeypatch):
    cand = DummyCandidate(content='Candidate sushi recipe content')
    dummy = DummyResp(text=None, candidates=[cand])

    def fake_generate(*args, **kwargs):
        return dummy

    monkeypatch.setattr(model, 'generate', fake_generate)
    out = generate_recipe('sushi')
    assert 'candidate sushi' in out.lower()