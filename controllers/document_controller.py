from fastapi import HTTPException
from models.document import Document, DocumentMetadata, DocumentPermission, DocumentUpdate
from services.document_service import document_service
from typing import List

class DocumentController:
    @staticmethod
    def create_document(title: str, author: str, content: str, tags: List[str]) -> Document:
        return document_service.create_document(title, author, content, tags)

    @staticmethod
    def get_document(doc_id: int) -> Document:
        document = document_service.get_document(doc_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document

    @staticmethod
    def update_document(doc_id: int, update: DocumentUpdate) -> Document:
        document = document_service.update_document(doc_id, update.title, update.content, update.tags)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document

    @staticmethod
    def delete_document(doc_id: int) -> bool:
        if not document_service.delete_document(doc_id):
            raise HTTPException(status_code=404, detail="Document not found")
        return True

    @staticmethod
    def get_document_metadata(doc_id: int) -> DocumentMetadata:
        metadata = document_service.get_document_metadata(doc_id)
        if not metadata:
            raise HTTPException(status_code=404, detail="Document not found")
        return metadata

    @staticmethod
    def get_all_documents() -> List[DocumentMetadata]:
        return document_service.get_all_documents()

    @staticmethod
    def search_documents(query: str) -> List[DocumentMetadata]:
        return document_service.search_documents(query)

