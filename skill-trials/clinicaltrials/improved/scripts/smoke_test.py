"""Smoke test for the ClinicalTrials.gov API v2 skill."""

import json
import urllib.parse
import urllib.request

BASE = "https://clinicaltrials.gov/api/v2"


def test_search():
    params = urllib.parse.urlencode({"query.term": "diabetes", "pageSize": "2"})
    url = f"{BASE}/studies?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        assert resp.status == 200, resp.status
        data = json.load(resp)
    assert "studies" in data
    assert len(data["studies"]) > 0
    first = data["studies"][0]
    nct_id = first["protocolSection"]["identificationModule"]["nctId"]
    assert nct_id.startswith("NCT")
    print(f"search ok: found {len(data['studies'])} studies; first={nct_id}")
    return nct_id


def test_single_study(nct_id: str):
    url = f"{BASE}/studies/{nct_id}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        assert resp.status == 200, resp.status
        data = json.load(resp)
    assert "protocolSection" in data
    assert data["protocolSection"]["identificationModule"]["nctId"] == nct_id
    print(f"single-study ok: {nct_id}")


def test_fields():
    params = urllib.parse.urlencode(
        {"query.term": "diabetes", "pageSize": "1", "fields": "NCTId,BriefTitle"}
    )
    url = f"{BASE}/studies?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.load(resp)
    first = data["studies"][0]["protocolSection"]["identificationModule"]
    assert "nctId" in first
    assert "briefTitle" in first
    print("fields ok")


if __name__ == "__main__":
    nct_id = test_search()
    test_single_study(nct_id)
    test_fields()
    print("all smoke tests passed")
