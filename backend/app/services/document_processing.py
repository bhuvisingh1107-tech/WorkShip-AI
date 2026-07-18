from app.schemas.document_processing import DocumentProcessingResult, DocumentSection
from app.utils.document_processing import (
    clean_text,
    estimate_reading_time,
    extract_metadata,
    generate_document_summary,
    normalize_whitespace,
    split_into_sections,
)


class DocumentProcessingService:
    """Deterministic preparation boundary for future embedding and retrieval workflows."""

    def process(
        self,
        *,
        title: str,
        content: str,
        category: str | None,
        source: str | None,
    ) -> DocumentProcessingResult:
        processed_content = normalize_whitespace(clean_text(content))
        sections = split_into_sections(processed_content)
        metadata = extract_metadata(
            processed_content,
            title=title,
            category=category,
            source=source,
        )
        return DocumentProcessingResult(
            content=processed_content,
            summary=generate_document_summary(processed_content),
            tags=metadata["tags"],
            reading_time_minutes=estimate_reading_time(processed_content),
            sections=[DocumentSection(**section) for section in sections],
            metadata=metadata,
        )
