# Dual Storage Layer

## Overview
The system implements a dual storage strategy to ensure high availability and user convenience.

### Internal Storage (MinIO/Local)
- **Purpose**: Persisting raw assets (chapter drafts, research data, infographic images) and temporary PDF files.
- **Implementation**: S3-compatible API via MinIO.
- **Retention**: Configurable (e.g., 30 days for assets, permanent for final PDFs).

### External Storage (Google Drive)
- **Purpose**: Primary delivery mechanism for the end user.
- **Workflow**:
  1. Authenticate user via OAuth.
  2. Create folder: `Auto-Generated Ebooks/[Topic Name]`.
  3. Upload final PDF, Metadata report, and high-res infographics.
  4. Return shareable link to the UI.

## File Structure (Storage)
- `/generations/[gen_id]/`
  - `metadata.json`: Full configuration.
  - `chapters/`: Markdown drafts.
  - `images/`: Chapter infographics.
  - `report.pdf`: Quality and Fact-check report.
  - `final_ebook.pdf`: The finalized product.

## Error Handling
- If Google Drive fails, the system falls back to MinIO/Local and notifies the user with a download link from the internal server.
