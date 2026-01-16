# Kanban Board (Pipeline View)

## Overview
The Kanban board provides a high-level visual of the entire ebook generation pipeline, especially useful for batch processing or administrative oversight.

## Columns (Stages)
1. **Queued**: Topics submitted and waiting for a free Celery slot.
2. **Analysis**: Agent 1 (Config), 2 (Topic), and 3 (Strategy) are active.
3. **Drafting**: Agent 4 (Research) and Agent 5 (Chapter Gen) are running.
4. **Verification**: Agent 8 (Quality) and Agent 9 (Critic) are performing the 7-pass verification.
5. **Publishing**: Agents 11, 12, and 13 are generating the PDF and syncing to storage.
6. **Finished**: Generation successful; links available.

## Card Details
- **Thumbnail**: Chapter 1 infographic preview.
- **Progress Gauge**: Percentage completion.
- **Health Indicator**: Flagging any agent timeouts or warnings.
- **Metadata**: Language, word count, and fact accuracy score.

## Implementation
- **Library**: `dnd-kit` or `@hello-pangea/dnd` for React.
- **Real-time**: WebSocket updates move cards across columns automatically as agents complete their phases.
