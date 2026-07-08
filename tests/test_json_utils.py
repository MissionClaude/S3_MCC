from app.json_utils import extract_json_object


def test_extract_plain_json():
    data = extract_json_object('{"status": "ok"}')
    assert data["status"] == "ok"


def test_extract_fenced_json():
    text = '```json\n{"status": "partial"}\n```'
    data = extract_json_object(text)
    assert data["status"] == "partial"
