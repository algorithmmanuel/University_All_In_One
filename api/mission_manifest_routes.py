"""Read-only public mission manifest endpoint.

Only safe mission metadata is returned. Existing authenticated mission endpoints
continue to own attempts, decisions and scores.
"""
from fastapi import APIRouter
from mission_contract import public_manifest_catalog

router = APIRouter(prefix="/api/v1", tags=["mission-discovery"])

@router.get("/mission-manifests")
def list_mission_manifests():
    return public_manifest_catalog()
