from starlette.testclient import TestClient
from sl_viewer_backend import app
from pathlib import Path
client = TestClient(app)

def test_analyze_log():
    response = client.post("/api/analyze_log", files={"log": ("row.csv", Path(__file__).with_name("row.csv").read_text())})
    json_data = response.json()
    assert response.status_code == 200

def test_analyze_log_empty_file_type():
    response = client.post("/api/analyze_log", files={"log": ("rowWrong.csv", Path(__file__).with_name("rowWrong.csv").read_text())})
    assert response.status_code == 400
    json_data = response.json()
    assert len(json_data["errors"]) == 1
    assert json_data["errors"][0] == "Log parsing error: IndexError('list index out of range')"

def test_analyze_log_invalid_file_type():
    response = client.post("/api/analyze_log", files={"log": ("row.txt", Path(__file__).with_name("row.txt").read_text())})
    assert response.status_code == 400
    json_data = response.json()
    assert len(json_data["errors"]) == 1
    assert json_data["errors"][0] == "Invalid log file"
    
