from fastapi import APIRouter, Query
from models.document import Document, DocumentMetadata, DocumentUpdate
from controllers.document_controller import DocumentController
from typing import List

router = APIRouter()

@router.post("/documents", response_model=Document)
async def create_document(title: str, author: str, content: str, tags: List[str]):
    return DocumentController.create_document(title, author, content, tags)

@router.get("/documents/{doc_id}", response_model=Document)
async def get_document(doc_id: int):
    return DocumentController.get_document(doc_id)

@router.put("/documents/{doc_id}", response_model=Document)
async def update_document(doc_id: int, update: DocumentUpdate):
    return DocumentController.update_document(doc_id, update)

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: int):
    return DocumentController.delete_document(doc_id)

@router.get("/documents/{doc_id}/metadata", response_model=DocumentMetadata)
async def get_document_metadata(doc_id: int):
    return DocumentController.get_document_metadata(doc_id)

@router.get("/documents", response_model=List[DocumentMetadata])
async def get_all_documents():
    return DocumentController.get_all_documents()

@router.get("/documents/search", response_model=List[DocumentMetadata])
async def search_documents(query: str = Query(..., min_length=1)):
    return DocumentController.search_documents(query)

