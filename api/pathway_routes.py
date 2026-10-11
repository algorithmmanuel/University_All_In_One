"""Public cybersecurity pathway routes, independent of legacy academies."""
from fastapi import APIRouter
from pathway_catalog import pathway_catalog

router = APIRouter(prefix="/api/v1", tags=["pathways"])

@router.get("/pathways")
def list_pathways():
    """Return versioned cybersecurity learning pathways; no account required."""
    return pathway_catalog()
