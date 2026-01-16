# Project Overview & Architecture

## System Vision
The **Automated PDF Ebook Creation System** is a zero-manual-interaction platform that transforms topic sentences into professional, fact-verified PDF ebooks with embedded infographics.

## Core Architecture
The system follows a multi-agent orchestration pattern with 13 specialized AI agents running on a FastAPI/Celery backend with a React-based Neo-Brutalist frontend.

### High-Level Flow
1. **Frontend**: User inputs a topic and configuration.
2. **Backend API**: Validates request and triggers a Celery task.
3. **Orchestration Layer**: Manages the 13-agent pipeline (sequential and parallel phases).
4. **Agent Layer**: Specialized LLMs (local via Ollama or remote via GPT-4o) perform research, writing, enhancement, and verification.
5. **Generation Layer**: WeasyPrint/ReportLab generates the final PDF with embedded graphics.
6. **Storage Layer**: Results are saved to Google Drive and local storage/MinIO.

### Agent Swarm Structure
- **Planning**: Configuration Loader, Topic Analysis, Content Strategy.
- **Execution**: Research Swarm (3 agents), Chapter Generation (N parallel), Infographic Generation (N parallel).
- **Refinement**: Quality Enhancement, Critic & Proofreading (7-pass fact verification).
- **Finalization**: SEO & Metadata, Layout & Formatting, PDF Generation, Storage Integration.

## Key Technical Goals
- **Zero Interaction**: No manual checkpoints after the initial topic submission.
- **Visual-First**: Mandatory one infographic per chapter.
- **Fact-Verified**: 95%+ factual accuracy through rigorous multi-pass verification.
- **Global reach**: 10 languages with native grammar checking and RTL support.
