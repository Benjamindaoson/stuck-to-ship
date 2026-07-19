## ADDED Requirements

### Requirement: Location-preserving multimodal ingestion
The system SHALL ingest supported PDF pages, PPT slides, images, transcript segments, and keyframes while preserving source, page, slide, and timestamp locations.

#### Scenario: PDF diagram page
- **WHEN** a PDF page contains text and an architecture diagram
- **THEN** ingestion stores page text, a retrievable page asset, page number, source path, and security metadata under one stable evidence identity

#### Scenario: Timestamped transcript
- **WHEN** a transcript segment includes start and end timestamps
- **THEN** ingestion stores the segment with its video source and exact time range

### Requirement: Text-first multimodal retrieval
The first multimodal release SHALL retrieve extracted text and asset metadata before invoking a vision-capable model on top-ranked visual evidence.

#### Scenario: Text answers the question
- **WHEN** extracted slide text supplies sufficient accepted evidence
- **THEN** the system answers without a vision model call and cites the slide

#### Scenario: Visual evidence required
- **WHEN** the question asks about a diagram, table, layout, or screenshot not represented adequately in extracted text
- **THEN** the system retrieves the associated visual asset and sends only top-ranked accessible assets to the configured vision model

### Requirement: Optional visual document retrieval
The system SHALL keep visual embedding retrieval optional and SHALL preserve text-only local operation when visual models or GPU resources are unavailable.

#### Scenario: Visual retriever disabled
- **WHEN** multimodal assets exist but visual embedding retrieval is disabled
- **THEN** text and metadata retrieval remain functional and the trace reports the disabled visual capability

### Requirement: Multimodal citations
Answers based on multimodal evidence SHALL include the source path and the most precise available page, slide, image, or timestamp location.

#### Scenario: Video explanation
- **WHEN** an answer uses a transcript segment and keyframe from a course video
- **THEN** the citation includes the video source and clickable start timestamp metadata

#### Scenario: Code screenshot explanation
- **WHEN** an answer uses a code screenshot
- **THEN** the citation identifies the image or slide and labels extracted code as OCR/VLM-derived evidence

### Requirement: Multimodal access and injection safety
Visual assets and extracted text SHALL inherit source ACL, visibility, and prompt-injection controls.

#### Scenario: Private slide image
- **WHEN** a user cannot access the source slide deck
- **THEN** the user cannot retrieve the slide image, extracted text, caption, or derived graph facts

### Requirement: Multimodal ingestion manifest
Every multimodal ingestion run SHALL record extractor versions, source hashes, generated assets, failures, and index version.

#### Scenario: Partial extraction failure
- **WHEN** one page or keyframe cannot be processed
- **THEN** ingestion reports the exact failed asset, keeps successful assets consistent, and does not mark the failed asset as indexed
