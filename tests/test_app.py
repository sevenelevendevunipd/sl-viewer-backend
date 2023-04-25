from starlette.testclient import TestClient
from sl_viewer_backend import app
from pathlib import Path
client = TestClient(app)

def test_analyze_log():
    response = client.post("/api/analyze_log", files={"log": ("row.csv", Path(__file__).with_name("row.csv").read_text())})
    json_data = response.json()
    assert response.status_code == 200

def test_analyze_log_empty_file_type():
    response = client.post("/api/analyze_log", files={"log": ("rowWrong.csv", "random invalid data")})
    assert response.status_code == 400
    json_data = response.json()
    assert len(json_data["errors"]) == 1
    assert any("Log parsing error" in error for error in json_data["errors"])
    
def test_analyze_log_invalid_file_type():
    response = client.post("/api/analyze_log", files={"log": ("row.txt", "random invalid data")})
    assert response.status_code == 400
    json_data = response.json()
    assert len(json_data["errors"]) == 1
    assert any("Invalid log file" in error for error in json_data["errors"])
    
