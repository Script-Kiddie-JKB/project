import os
import json
import re
from typing import List, Optional
from datetime import datetime
from models.document import Document, DocumentMetadata, DocumentPermission
import uuid

class DocumentService:
    def __init__(self):
        self.document_dir = "documents"
        self.metadata_dir = "metadata"
        os.makedirs(self.document_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        self.next_id = self._get_next_id()

    def _sanitize_filename(self, filename: str) -> str:
        return re.sub(r'[^\w\-_\. ]', '_', filename)

    def _get_next_id(self) -> int:
        existing_ids = [int(f.split('_')[0]) for f in os.listdir(self.metadata_dir) if f.endswith('.json')]
        return max(existing_ids) + 1 if existing_ids else 1

    def create_document(self, title: str, author: str, content: str, tags: List[str]) -> Document:
        doc_id = self.next_id
        self.next_id += 1
        sanitized_title = self._sanitize_filename(title)
        document = Document(
            id=doc_id,
            title=title,
            author=author,
            content=content,
            tags=tags,
            uploaded_date=datetime.now(),
            version=1
        )
        
        # Save content to a text file
        with open(os.path.join(self.document_dir, f"{doc_id}_{sanitized_title}.txt"), "w") as f:
            f.write(content)
        
        # Save metadata to a JSON file
        metadata = document.dict()
        metadata['uploaded_date'] = metadata['uploaded_date'].isoformat()
        with open(os.path.join(self.metadata_dir, f"{doc_id}_{sanitized_title}.json"), "w") as f:
            json.dump(metadata, f)
        
        return document

    def get_document(self, doc_id: int) -> Optional[Document]:
        for filename in os.listdir(self.metadata_dir):
            if filename.startswith(f"{doc_id}_"):
                with open(os.path.join(self.metadata_dir, filename), "r") as f:
                    metadata = json.load(f)
                content_filename = filename.replace('.json', '.txt')
                with open(os.path.join(self.document_dir, content_filename), "r") as f:
                    content = f.read()
                metadata['uploaded_date'] = datetime.fromisoformat(metadata['uploaded_date'])
                metadata['content'] = content
                return Document(**metadata)
        return None

    def update_document(self, doc_id: int, title: Optional[str] = None, 
                        content: Optional[str] = None, tags: Optional[List[str]] = None) -> Optional[Document]:
        document = self.get_document(doc_id)
        if document:
            old_title = document.title
            if title:
                document.title = title
            if content:
                document.content = content
            if tags:
                document.tags = tags
            document.version += 1
            
            # Update files
            old_sanitized_title = self._sanitize_filename(old_title)
            new_sanitized_title = self._sanitize_filename(document.title)
            
            # Update content file
            old_content_filename = f"{doc_id}_{old_sanitized_title}.txt"
            new_content_filename = f"{doc_id}_{new_sanitized_title}.txt"
            os.rename(os.path.join(self.document_dir, old_content_filename),
                      os.path.join(self.document_dir, new_content_filename))
            with open(os.path.join(self.document_dir, new_content_filename), "w") as f:
                f.write(document.content)
            
            # Update metadata file
            old_metadata_filename = f"{doc_id}_{old_sanitized_title}.json"
            new_metadata_filename = f"{doc_id}_{new_sanitized_title}.json"
            os.rename(os.path.join(self.metadata_dir, old_metadata_filename),
                      os.path.join(self.metadata_dir, new_metadata_filename))
            metadata = document.dict()
            metadata['uploaded_date'] = metadata['uploaded_date'].isoformat()
            with open(os.path.join(self.metadata_dir, new_metadata_filename), "w") as f:
                json.dump(metadata, f)
            
        return document

    def delete_document(self, doc_id: int) -> bool:
        for filename in os.listdir(self.metadata_dir):
            if filename.startswith(f"{doc_id}_"):
                os.remove(os.path.join(self.metadata_dir, filename))
                content_filename = filename.replace('.json', '.txt')
                os.remove(os.path.join(self.document_dir, content_filename))
                return True
        return False

    def get_document_metadata(self, doc_id: int) -> Optional[DocumentMetadata]:
        for filename in os.listdir(self.metadata_dir):
            if filename.startswith(f"{doc_id}_"):
                with open(os.path.join(self.metadata_dir, filename), "r") as f:
                    metadata = json.load(f)
                metadata['uploaded_date'] = datetime.fromisoformat(metadata['uploaded_date'])
                return DocumentMetadata(**metadata)
        return None

    def get_all_documents(self) -> List[DocumentMetadata]:
        documents = []
        for filename in os.listdir(self.metadata_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.metadata_dir, filename), "r") as f:
                    metadata = json.load(f)
                metadata['uploaded_date'] = datetime.fromisoformat(metadata['uploaded_date'])
                documents.append(DocumentMetadata(**metadata))
        return documents

    def search_documents(self, query: str) -> List[DocumentMetadata]:
        results = []
        query = query.lower()
        
        # Check if query is a valid integer (document ID)
        try:
            doc_id = int(query)
            doc = self.get_document_metadata(doc_id)
            if doc:
                return [doc]
        except ValueError:
            pass

        for filename in os.listdir(self.metadata_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.metadata_dir, filename), "r") as f:
                    metadata = json.load(f)
            
            # Check if query matches title
            if query in metadata['title'].lower():
                metadata['uploaded_date'] = datetime.fromisoformat(metadata['uploaded_date'])
                results.append(DocumentMetadata(**metadata))
                continue
            
            # Check if query matches content
            content_filename = filename.replace('.json', '.txt')
            with open(os.path.join(self.document_dir, content_filename), "r") as f:
                content = f.read()
            if query in content.lower():
                metadata['uploaded_date'] = datetime.fromisoformat(metadata['uploaded_date'])
                results.append(DocumentMetadata(**metadata))
    
        return results

document_service = DocumentService()

