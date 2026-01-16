# Filtering & Search System

## Functional Requirements
- **Full-Text Search**: Search by topic sentence, generated content, or author tags.
- **Smart Filters**:
  - **Status**: Completed, Failed, Processing.
  - **Language**: Filter by any of the 10 supported languages.
  - **Quality Range**: Filter by Factual Accuracy Score (e.g., > 95%).
  - **Date Range**: Standard from/to filters.
  - **Content Depth**: Filter by number of two-level depth chapters.

## Technical Architecture
- **Backend**: PostgreSQL `tsvector` for basic full-text search.
- **Frontend**: Multi-select dropdowns (Neo-Brutalist style) and a persistent search bar.
- **Query Optimization**: Indexed columns for `status`, `user_id`, and `language`.
- **URL Sync**: All filters are synced to URL parameters for shareable search results.
