# Project Requirements Document (PRD)
## Automated PDF Ebook Creation System - Web Application

**Version:** 1.0
**Date:** January 15, 2026
**Status:** Draft
**Project:** Automated Ebook Generation System with Zero Manual Interaction

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Vision & Goals](#2-product-vision--goals)
3. [Functional Requirements](#3-functional-requirements)
4. [Technical Requirements](#4-technical-requirements)
5. [User Requirements](#5-user-requirements)
6. [System Architecture](#6-system-architecture)
7. [API Specifications](#7-api-specifications)
8. [Database Schema](#8-database-schema)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [Implementation Phases](#10-implementation-phases)
11. [Success Metrics](#11-success-metrics)
12. [Risk Assessment](#12-risk-assessment)

---

## 1. Executive Summary

### 1.1 Project Overview

The Automated PDF Ebook Creation System is a revolutionary web application that transforms simple topic sentences into professional, market-ready PDF ebooks with **zero manual interaction**. Built entirely on **open-source, CPU-optimized models**, the system eliminates GPU requirements while delivering exceptional quality through a sophisticated 13-agent pipeline.

### 1.2 Key Differentiators

- **Zero Manual Interaction**: Users provide only a topic sentence; the system handles everything else automatically
- **Every Chapter Includes Infographic**: Automatic generation of visual summaries for each chapter
- **Multi-Language Support**: 10 languages with proper grammar checking and RTL formatting
- **Flexible Chapter Structure**: User-controlled Basic (0-20), One-Level (0-15), and Two-Level (0-10) depth chapters
- **Strong Fact Validation**: 7-pass critic & proofreading agent ensures 95%+ factual accuracy
- **Dual Storage**: Google Drive (default) + optional local folder storage
- **Open-First Design**: Uses CPU-optimized models (Llama 3.1 8B, Mistral 7B, Qwen2.5 7B, Gemma 2 9B) with optional API fallbacks
- **Complete Admin Dashboard**: Track all generations, view Google Drive links, monitor system performance

### 1.3 Target Users

- **Content Creators**: Authors, bloggers, marketers needing rapid ebook creation
- **Businesses**: Companies requiring documentation, guides, training materials
- **Educators**: Teachers and institutions creating educational resources
- **Researchers**: Academics converting research into accessible formats
- **Multi-Language Users**: Global audience requiring content in 10 supported languages

### 1.4 Value Proposition

- **Time Savings**: Generate professional ebooks in 10-15 minutes vs. weeks manually
- **Cost Efficiency**: $0 for open-source models vs. expensive human writers
- **Quality Assurance**: 95%+ factual accuracy, professional formatting, embedded infographics
- **Scalability**: Batch generate 10 ebooks in 50 minutes (parallel processing)
- **Ease of Use**: Single topic sentence input, zero configuration required for basic use

---

## 2. Product Vision & Goals

### 2.1 Vision Statement

To democratize professional ebook creation by making it accessible, fast, and free for everyone, regardless of technical expertise or language, while maintaining the highest standards of quality and accuracy.

### 2.2 Product Goals

#### Primary Goals (Must Achieve)
1. **Zero Manual Interaction**: Fully automated pipeline from topic sentence to PDF
2. **Professional Quality**: Market-ready ebooks with embedded infographics and fact validation
3. **Multi-Language Support**: Full support for 10 languages with proper grammar and formatting
4. **User Choice**: All critical parameters (language, chapter structure, storage) controlled by user
5. **Open-Source First**: CPU-based models with optional API fallbacks
6. **Web-Based UI**: Intuitive interface with real-time progress tracking
7. **Admin Dashboard**: Complete oversight of all generations with Google Drive links

#### Secondary Goals (Should Achieve)
1. **Batch Processing**: Generate multiple ebooks simultaneously (up to 3 in parallel)
2. **Template Library**: Pre-built configurations for common genres
3. **Collaborative Features**: Share ebooks, comments, multi-user projects
4. **Cost Monitoring**: Track API usage with budget alerts
5. **Advanced Search**: Filter and search generations by multiple criteria

#### Stretch Goals (Nice to Have)
1. **Email Notifications**: Alerts when generation completes/fails
2. **Rate Limiting**: Fair usage policies per user
3. **Automated Backups**: Daily PostgreSQL and MinIO backups
4. **Version Control**: Track multiple regenerations of same topic

### 2.3 Success Criteria

- **Performance**: Single ebook generation in <15 minutes
- **Quality**: 95%+ factual accuracy, 60+ readability score
- **Reliability**: 98%+ success rate with automatic error recovery
- **User Satisfaction**: 4.5/5 average user rating
- **Adoption**: 100+ ebooks generated in first month of beta testing

---

## 3. Functional Requirements

### 3.1 User-Invocable Skills (9 Skills)

#### FR-1: Primary Ebook Generation (`/ebook-generate`)
**Priority**: P0 (Critical)
**Description**: Generate single ebook with zero manual interaction

**Acceptance Criteria**:
- Accept topic sentence (3-500 characters)
- Load or validate configuration JSON
- Execute all 13 agents sequentially/parallel
- Generate PDF with embedded infographics
- Upload to Google Drive (primary) + local folder (optional)
- Return download links and fact verification report
- Display real-time progress (current agent, percentage, ETA)
- Complete generation in 10-15 minutes

**User Workflow**:
```
Input Topic → Configure Options → Generate → Monitor Progress → Download PDF
```

#### FR-2: Batch Ebook Generation (`/ebook-batch`)
**Priority**: P1 (High)
**Description**: Generate multiple ebooks simultaneously

**Acceptance Criteria**:
- Accept up to 10 topic sentences
- Run 3 pipelines in parallel
- Display progress per pipeline
- Aggregate results with summary report
- Complete 3 ebooks in 15-20 minutes
- Complete 10 ebooks in 50-60 minutes

#### FR-3: Configuration Creation (`/ebook-config-create`)
**Priority**: P0 (Critical)
**Description**: Create or update ebook-config.json

**Acceptance Criteria**:
- Interactive prompts for all required fields
- Language selection (10 options)
- Chapter structure (Basic: 0-20, One-Level: 0-15, Two-Level: 0-10)
- Storage options (Google Drive, local folder, both)
- Styling options (fonts, colors, page size)
- Content specifications (words per chapter, exercises, case studies, tone, infographic style)
- Validation before saving
- Export/import configuration JSON

#### FR-4: Template-Based Generation (`/ebook-template`)
**Priority**: P2 (Medium)
**Description**: Generate ebook from custom template

**Acceptance Criteria**:
- Accept template file path (JSON format)
- Validate template parameters
- Execute pipeline enforcing template specifications
- Deliver PDF matching template structure

#### FR-5: Quality Report (`/ebook-quality-report`)
**Priority**: P2 (Medium)
**Description**: Generate comprehensive quality and fact verification report

**Acceptance Criteria**:
- Accept file path (markdown, docx, txt, pdf)
- Launch Quality Enhancement Agent (analysis mode)
- Launch Critic & Proofreading Agent (full verification)
- Generate PDF report with:
  - Readability scores
  - Grammar issues
  - Fact verification results (claims verified/corrected/flagged)
  - Factual accuracy score (0-100%)
  - Improvement suggestions

#### FR-6: Content Expansion (`/ebook-expand`)
**Priority**: P2 (Medium)
**Description**: Expand existing content into full ebook

**Acceptance Criteria**:
- Accept existing content file
- Analyze style, tone, language
- Extract key themes
- Generate additional chapters
- Generate infographics for all chapters
- Run full quality and fact-checking pipeline
- Deliver complete ebook PDF

#### FR-7: Storage Setup (`/ebook-storage-setup`)
**Priority**: P0 (Critical)
**Description**: Configure storage (Google Drive + Local)

**Acceptance Criteria**:
- Google Drive Setup:
  - Check for existing credentials
  - Guide user through Google Cloud project creation
  - Enable Drive API
  - Create OAuth credentials
  - Test authentication
  - Create base folder structure
- Local Folder Setup:
  - Prompt for local folder path
  - Test write permissions
  - Create folder structure
  - Update config with local path

#### FR-8: Statistics Dashboard (`/ebook-stats`)
**Priority**: P1 (High)
**Description**: Display generation statistics

**Acceptance Criteria**:
- Total ebooks created
- Average generation time
- Most popular topics
- Quality score trends
- Fact accuracy trends
- Storage usage (Google Drive, local)
- Agent performance metrics
- Language distribution

#### FR-9: Infographic Generation (`/ebook-infographic-only`)
**Priority**: P1 (High)
**Description**: Generate infographics for existing chapters

**Acceptance Criteria**:
- Accept folder path with chapter files or single file
- Analyze each chapter's content structure
- Extract key concepts
- Determine visualization type (flowchart, mind map, timeline, etc.)
- Generate infographic image
- Save as `chapter_[N]_infographic.png`
- Deliver folder with all infographic images

---

### 3.2 Specialized Agents (13 Agents)

#### FR-10: Configuration Loader Agent
**Priority**: P0
**Function**: Load, validate, and parse user configuration

**Input**:
- `ebook-config.json` file path (optional)
- Web UI configuration (if JSON not present)

**Processing**:
- Validate language code (must be in supported list)
- Validate chapter counts (Basic: 0-20, One-Level: 0-15, Two-Level: 0-10)
- Calculate total chapters (must be ≥1)
- Validate storage paths
- Validate styling parameters
- Apply NO defaults (user must specify all required fields)

**Output**: Validated configuration object with applied parameters

---

#### FR-11: Topic Analysis Agent
**Priority**: P0
**Function**: Deep analysis of input topic sentence

**Input**:
- Topic sentence
- Configuration object

**Processing**:
- Identify target audience
- Classify domain
- Determine complexity level
- Extract key themes and subtopics
- Language-specific analysis

**Tools**: WebSearch, Memory, Configuration

**Output**: Structured topic brief with audience, domain, complexity, tone

---

#### FR-12: Content Strategy Agent
**Priority**: P0
**Function**: Design comprehensive table of contents

**Input**:
- Topic brief
- Chapter structure configuration

**Processing**:
- Allocate chapters to Basic/One-Level/Two-Level
- Create chapter-by-chapter outline
- Define depth for each section
- Establish logical flow
- Language-specific structuring (e.g., RTL for Arabic)

**Output**: Detailed outline with depth levels and word counts

---

#### FR-13: Research Swarm Agents (3 Parallel)
**Priority**: P0
**Function**: Parallel research on different aspects

**Input**: Topic brief

**Processing**:
- **Agent A**: Latest trends, statistics, data (2024-2025)
- **Agent B**: Expert sources, case studies, examples
- **Agent C**: Competitor analysis, market gaps, unique angles
- All 3 agents run simultaneously
- Aggregate and deduplicate results

**Tools**: WebSearch, Academic databases, Statistical databases

**Output**: Curated research database with cited sources

---

#### FR-14: Chapter Generation Swarm
**Priority**: P0
**Function**: Generate all chapters in parallel

**Input**:
- Research database
- Content outline
- Configuration

**Processing**:
- **Basic Chapter Agents**: Linear flow, 3000-4000 words
- **One-Level Depth Agents**: Main sections + 2-3 subsections, 4000-5000 words
- **Two-Level Depth Agents**: Complex hierarchies, 5000-7000 words
- All chapters generated simultaneously
- Include examples, case studies, exercises
- Language-specific content generation

**Tools**: Memory, WebSearch, Configuration

**Output**: Complete chapter drafts with consistent tone

---

#### FR-15: Infographic Generation Agent
**Priority**: P0
**Function**: Generate one infographic per chapter (MANDATORY)

**Input**: Chapter content

**Processing**:
1. Analyze chapter structure
2. Extract 5-7 key concepts
3. Determine visualization type:
   - Flowchart (processes)
   - Mind map (concepts)
   - Timeline (historical)
   - Comparison table (comparisons)
   - Hierarchy diagram (classifications)
4. Generate image using:
   - SDXL Lightning (4-step CPU-optimized)
   - Mermaid.js / Graphviz (diagrams)
   - Matplotlib / Plotly (charts)
5. Apply styling from configuration
6. Save as high-resolution PNG (150 DPI, 1200px width)

**Output**: High-resolution infographic image file

---

#### FR-16: Visual Design Agent
**Priority**: P1
**Function**: Design additional visual elements

**Input**: Configuration, all infographics

**Processing**:
- Design section dividers
- Create chapter transition graphics
- Design callout boxes
- Style quotes and headers
- Apply configuration styling

**Output**: Visual design system document

---

#### FR-17: Quality Enhancement Agent
**Priority**: P0
**Function**: Multi-stage content improvement

**Input**: Chapter drafts

**Processing**:
- Grammar correction (LanguageTool, multi-language)
- Style consistency check
- Readability optimization (target: 8th-grade level)
- Professional polish
- Engagement enhancement

**Quality Metrics**:
- Flesch Reading Ease score >60
- Active voice percentage >70%
- Average sentence length 15-20 words
- Zero grammatical errors

**Output**: Polished, professional content

---

#### FR-18: Critic & Proofreading Agent
**Priority**: P0
**Function**: Rigorous fact validation and correction

**Input**: Polished content

**Processing** (7-Pass Verification):
1. Identify all factual claims
2. Verify each claim against trusted sources
3. Cross-reference claims within document
4. Check for logical contradictions
5. Validate statistics and data
6. Assess source credibility
7. Language-specific accuracy checks

**Verification Scope**:
- Statistics & Numbers
- Dates & Timelines
- Quotes & Citations
- Scientific Claims
- Technical Statements
- Geographical Info
- Names & Titles
- Cultural Context

**Correction Strategy**:
- High Confidence Errors (>90%): Auto-correct
- Medium Confidence (70-90%): Flag with alternatives
- Low Confidence (<70%): Highlight for review
- Unverifiable Claims: Remove or qualify

**Tools**: WebSearch, Academic databases, Statistical databases, News archives

**Output**: Fact-corrected content + verification report with confidence scores

**Quality Gate**: Minimum 95% factual accuracy required

---

#### FR-19: SEO and Metadata Agent
**Priority**: P1
**Function**: Generate marketing materials

**Input**: Final content, topic

**Processing**:
- Generate 10 title variants
- Create meta description
- Extract keywords
- Write back cover copy
- Generate Amazon/Google Books description
- Language-specific SEO optimization

**Output**: Marketing package (titles, metadata, keywords, copy)

---

#### FR-20: Layout and Formatting Agent
**Priority**: P0
**Function**: Professional book layout design

**Input**: Content, infographics, configuration

**Processing**:
- Title page
- Copyright page
- Table of contents
- Chapter headers
- **Infographic placement** (at start of each chapter)
- Page numbering
- Footer elements
- Callout boxes
- Highlighted sections
- Language-specific formatting (RTL for Arabic)

**Design Standards**:
- Apply configuration styling (fonts, colors, page size)
- Professional fonts
- Consistent margins and spacing
- Visual hierarchy
- White space optimization

**Output**: Formatted document structure with embedded infographics

---

#### FR-21: PDF Generation Agent
**Priority**: P0
**Function**: Convert to professional PDF

**Input**: Formatted document

**Processing**:
- Convert to PDF
- **Embed all infographic images**
- Embed fonts and graphics
- Optimize for print (300 DPI) and digital
- Add interactive elements:
  - Clickable table of contents
  - Internal hyperlinks
  - External reference links
  - ISBN placeholder
  - Author bio section
- Language-specific PDF settings (embedded fonts, proper encoding)

**Tools**: Python (weasyprint, reportlab), Configuration, Infographic images

**Output**: Publication-ready PDF file

**Specifications**:
- Page size: 6x9 inch (from config)
- Print-ready: 300 DPI
- Searchable text
- Minimal file size with max quality
- Proper font embedding for all languages

---

#### FR-22: Storage Integration Agent
**Priority**: P0
**Function**: Dual storage system (Google Drive + Local)

**Input**: PDF file, metadata, infographics

**Processing**:
- **Google Drive Storage** (Default):
  - Authenticate with Google Drive API
  - Create folder structure:
    - Main: "Auto-Generated Ebooks"
    - Subfolder: [Topic Name]
    - Files: PDF, Infographics folder, Metadata, Reports
  - Upload with proper naming
  - Generate shareable link
  - Log all uploads

- **Local Storage** (Optional):
  - Check config for `create_local_copy` flag
  - Save to `local_folder` path
  - Create local folder structure
  - Generate local file manifest

**Output**:
- Confirmation with file locations
- Google Drive shareable links
- Local file paths
- Upload log
- Storage summary

**Tools**: Google Drive API (PyDrive2), Local file system (os, shutil)

---

### 3.3 Enhanced Features (8 Gaps)

#### FR-23: Email Notifications
**Priority**: P2
**Description**: Alert users when generation completes/fails

**Acceptance Criteria**:
- Send email when generation completes with:
  - Topic
  - Generation time
  - Quality score
  - Download links
- Send email when generation fails with:
  - Topic
  - Error details
  - Retry instructions
- User preferences for:
  - Generation complete notifications
  - Generation failure notifications
  - Daily summary
  - Weekly quality report

---

#### FR-24: Rate Limiting
**Priority**: P2
**Description**: Prevent API abuse, ensure fair usage

**Acceptance Criteria**:
- 5 generations per hour per user
- Higher limits for admin (100/hour)
- Display usage limits in UI
- Alert user when limit approached
- Queue option when limit exceeded

---

#### FR-25: Automated Backups
**Priority**: P1
**Description**: Protect data, disaster recovery

**Acceptance Criteria**:
- Daily PostgreSQL backup at 2 AM
- Upload backups to MinIO
- MinIO versioning enabled
- Admin UI for:
  - View available backups
  - Restore from backup
  - Download backup
  - Configure schedule
- Retain 7 daily backups

---

#### FR-26: Version Control for Regenerations
**Priority**: P2
**Description**: Track multiple versions of same topic

**Acceptance Criteria**:
- Auto-increment version number on regeneration
- Link versions to parent generation
- Unique constraint on topic + version per user
- UI to view all versions of same topic
- Compare versions feature
- "Generate Version 3" button

---

#### FR-27: Cost Monitoring & Budgets
**Priority**: P2
**Description**: Track API costs, alert on budget limits

**Acceptance Criteria**:
- Monthly budget per user
- Real-time cost tracking
- Alert at configurable threshold (default: 80%)
- Cost breakdown by provider:
  - Local models (Ollama, SDXL): $0
  - OpenAI API (GPT-4o, DALL-E): Actual cost
  - Anthropic API (Claude): Actual cost
- Projected month-end cost
- Budget adjustment UI

---

#### FR-28: Advanced Search & Filtering
**Priority**: P1
**Description**: Find specific generations quickly

**Acceptance Criteria**:
- Full-text search across topics and content
- Filters:
  - Status (pending, processing, completed, failed)
  - Language (10 options)
  - Date range
  - Quality score (min-max)
  - Chapter count (min-max)
  - Word count (min-max)
  - Fact accuracy (min-max)
- Sort options:
  - Date
  - Relevance
  - Quality
- Export results (CSV, JSON, PDF)

---

#### FR-29: Collaborative Features
**Priority**: P2
**Description**: Share ebooks, comments, multi-user projects

**Acceptance Criteria**:
- Share ebooks via:
  - Email invitation
  - Shareable link with token
- Permission levels:
  - View only
  - View & Comment
  - Edit
- Expiry options:
  - Never
  - 7 days
  - 30 days
  - Custom
- Comments per chapter
- Active shares management (revoke)

---

#### FR-30: Template Library
**Priority**: P2
**Description**: Pre-built templates for common genres

**Acceptance Criteria**:
- Public templates:
  - Professional Business Book
  - Technical Guide
  - Academic Paper
  - Creative Non-Fiction
  - How-To Guide
- Template preview
- Save to user's library
- Create custom template
- Usage tracking
- Categories for filtering

---

## 4. Technical Requirements

### 4.1 Technology Stack

#### 4.1.1 Frontend
- **Framework**: React.js 18+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query + Zustand
- **Routing**: React Router
- **Real-time Updates**: WebSocket (Socket.io)
- **Build Tool**: Vite
- **Testing**: Jest + React Testing Library

#### 4.1.2 Backend
- **Framework**: FastAPI (Python 3.11+)
- **Task Queue**: Celery with Redis broker
- **Authentication**: JWT tokens
- **API Documentation**: OpenAPI/Swagger
- **Testing**: Pytest

#### 4.1.3 Database & Cache
- **Primary Database**: PostgreSQL 15+ (Docker)
- **Cache**: Redis 7+ (Docker)
- **Object Storage**: MinIO (Docker, S3-compatible)

#### 4.1.4 AI/ML Models (CPU-Based)
**Text Generation**:
- Ollama (local, free):
  - Llama 3.1 8B (CPU-optimized)
  - Mistral 7B (CPU-optimized)
  - Qwen2.5 7B (CPU-optimized, multilingual)
  - Gemma 2 9B (CPU-optimized)
- Optional API:
  - OpenAI GPT-4o (paid)
  - Anthropic Claude 3.5 Sonnet (paid)

**Infographic Generation**:
- Stable Diffusion XL Lightning (local, 4-step inference)
- Mermaid.js (diagrams)
- Graphviz (diagrams)
- Matplotlib (charts)
- Plotly (charts)
- Optional API:
  - DALL-E 3 (paid)
  - Midjourney (paid)

**Grammar & Quality**:
- LanguageTool (open source, multi-language)
- Textstat (readability metrics)

#### 4.1.5 PDF Generation
- **Library**: WeasyPrint or ReportLab (Python)
- **Format**: HTML/CSS to PDF
- **Features**: Font embedding, image embedding, bookmarks

#### 4.1.6 Deployment
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx (production)
- **Monitoring**: Prometheus + Grafana (optional)
- **Error Tracking**: Sentry (optional)

---

### 4.2 System Architecture

#### 4.2.1 Microservices Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer                            │
│                            (Nginx)                                │
└───────────────────────┬─────────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐              ┌───────▼────────┐
│  Frontend      │              │  Backend API   │
│  (React)       │◄─────────────►│  (FastAPI)     │
│  Port: 3000    │              │  Port: 8000    │
└────────────────┘              └───────┬────────┘
                                        │
                ┌───────────────────────────┼───────────────────────────┐
                │                           │                           │
        ┌───────▼────────┐          ┌───────▼────────┐        ┌───────▼────────┐
        │  PostgreSQL    │          │  Redis         │        │  MinIO         │
        │  Port: 5432    │          │  Port: 6379    │        │  Port: 9000    │
        └────────────────┘          └────────────────┘        └────────────────┘
                │
        ┌───────┴────────┐
        │  Celery Worker │
        │  (Background)  │
        └───────┬────────┘
                │
        ┌───────┴────────┐
        │  Ollama        │
        │  Port: 11434   │
        └────────────────┘
```

#### 4.2.2 Component Responsibilities

**Frontend (React)**:
- User interface for all 6 pages
- Real-time status updates via WebSocket
- Form validation and submission
- PDF viewing and download
- Admin dashboard with monitoring

**Backend API (FastAPI)**:
- RESTful API endpoints
- Authentication & authorization
- Request validation
- Agent orchestration
- Celery task management
- Database operations

**Celery Worker**:
- Execute long-running generation tasks
- Parallel agent execution
- Progress updates to Redis
- Error handling and retry logic

**PostgreSQL**:
- User data
- Generation records
- Fact verification logs
- Agent execution logs
- API usage tracking
- Infographic metadata

**Redis**:
- Celery task queue
- Real-time progress cache
- Session storage
- Rate limiting

**MinIO**:
- PDF file storage
- Infographic image storage
- Metadata files
- Backup storage

**Ollama**:
- LLM model serving (Llama, Mistral, Qwen, Gemma)
- CPU-optimized inference
- Model caching

---

### 4.3 Hardware Requirements

#### 4.3.1 Minimum Requirements (Development)
- **CPU**: 4 cores, 2.0 GHz
- **RAM**: 16 GB
- **Storage**: 50 GB SSD
- **OS**: Windows 10/11, macOS 12+, or Linux (Ubuntu 22.04+)
- **Docker**: 20.10+

#### 4.3.2 Recommended Requirements (Production)
- **CPU**: 8+ cores, 3.0 GHz
- **RAM**: 32 GB
- **Storage**: 200 GB SSD
- **OS**: Linux (Ubuntu 22.04 LTS)
- **Docker**: 24.0+
- **Network**: Stable internet connection (for research, APIs)

---

### 4.4 Software Dependencies

#### 4.4.1 Backend (Python)
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
celery==5.3.6
redis==5.0.1
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
weasyprint==60.1
reportlab==4.0.8
pillow==10.2.0
languagetool==2.7.1
textstat==0.7.3
ollama==0.1.6
diffusers==0.26.0
transformers==4.37.0
accelerate==0.26.0
safetensors==0.4.1
torch==2.1.2 (CPU version)
matplotlib==3.8.2
plotly==5.18.0
graphviz==0.20.1
pydrive2==1.15.2
minio==7.2.0
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
websockets==12.0
```

#### 4.4.2 Frontend (Node.js)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.1",
    "typescript": "^5.3.3",
    "@tanstack/react-query": "^5.17.9",
    "zustand": "^4.4.7",
    "axios": "^1.6.5",
    "socket.io-client": "^4.5.4",
    "tailwindcss": "^3.4.1",
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.1.1",
    "recharts": "^2.10.3",
    "react-pdf": "^7.7.1",
    "react-hook-form": "^7.49.3",
    "zod": "^3.22.4",
    "date-fns": "^3.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.12",
    "jest": "^29.7.0",
    "@testing-library/react": "^14.1.2",
    "eslint": "^8.56.0",
    "prettier": "^3.1.1"
  }
}
```

---

## 5. User Requirements

### 5.1 User Personas

#### Persona 1: Content Creator (Primary)
- **Name**: Sarah Chen
- **Role**: Freelance Writer & Content Marketer
- **Goals**: Rapidly produce ebooks for clients, scale content production
- **Pain Points**: Time-consuming manual writing, expensive outsourcing
- **Technical Proficiency**: Medium
- **Languages**: English, Spanish
- **Expected Usage**: Generate 10+ ebooks per month

#### Persona 2: Business User (Primary)
- **Name**: Michael Johnson
- **Role**: Marketing Director at Tech Startup
- **Goals**: Create documentation, guides, training materials
- **Pain Points**: Limited resources, need consistent quality
- **Technical Proficiency**: Low-Medium
- **Languages**: English only
- **Expected Usage**: Generate 5+ ebooks per month

#### Persona 3: Educator (Secondary)
- **Name**: Dr. Priya Sharma
- **Role**: University Professor
- **Goals**: Convert research into accessible educational materials
- **Pain Points**: Academic writing too dense for general audience
- **Technical Proficiency**: Medium-High
- **Languages**: English, Hindi
- **Expected Usage**: Generate 2-3 ebooks per semester

#### Persona 4: Admin User (Secondary)
- **Name**: Alex Rivera
- **Role**: System Administrator
- **Goals**: Monitor system health, manage users, troubleshoot issues
- **Pain Points**: Lack of visibility into generations
- **Technical Proficiency**: High
- **Languages**: English
- **Expected Usage**: Daily monitoring, monthly reports

---

### 5.2 User Stories

#### Epic 1: Ebook Generation
- **US-1.1**: As a content creator, I want to generate an ebook from a simple topic sentence so that I can save weeks of manual writing time
- **US-1.2**: As a business user, I want to select my target language so that I can create content for international audiences
- **US-1.3**: As a content creator, I want to customize chapter structure so that I can control the depth and complexity of my ebook
- **US-1.4**: As a business user, I want to save ebooks to Google Drive so that I can easily share them with my team
- **US-1.5**: As an educator, I want to download ebooks locally so that I can store them on my secure server

#### Epic 2: Configuration
- **US-2.1**: As a content creator, I want to create reusable configurations so that I can maintain consistency across multiple ebooks
- **US-2.2**: As a business user, I want to select from pre-built templates so that I don't have to configure every setting manually
- **US-2.3**: As an educator, I want to customize styling (fonts, colors) so that the ebook matches my institution's branding

#### Epic 3: Quality Assurance
- **US-3.1**: As a content creator, I want to see a fact verification report so that I can trust the accuracy of the content
- **US-3.2**: As a business user, I want to view quality metrics so that I can ensure professional standards
- **US-3.3**: As an educator, I want to see readability scores so that I can confirm the content is appropriate for my students

#### Epic 4: Monitoring & History
- **US-4.1**: As a content creator, I want to view my generation history so that I can track my past work
- **US-4.2**: As a business user, I want to search and filter generations so that I can find specific ebooks quickly
- **US-4.3**: As an admin user, I want to monitor all generations so that I can identify and troubleshoot issues

#### Epic 5: Batch Processing
- **US-5.1**: As a content creator, I want to generate multiple ebooks simultaneously so that I can scale my production
- **US-5.2**: As a business user, I want to see progress for each pipeline so that I know when each ebook will be ready

---

### 5.3 User Interface Requirements

#### UI-1: Generate Page (`/generate`)
**Required Sections**:
1. **Topic Input** (Required)
   - Large text input (minimum 3 words, maximum 500 characters)
   - Character counter
   - Example topics for inspiration

2. **Language Selection** (Required)
   - Radio buttons for 10 supported languages
   - Validation: Must select one language
   - Warning if no language selected

3. **Chapter Structure** (Required)
   - Number inputs + sliders for:
     * Basic Chapters (0-20)
     * One-Level Depth Chapters (0-15)
     * Two-Level Depth Chapters (0-10)
   - Real-time total calculation
   - Validation: Minimum 1 chapter required
   - Descriptions for each chapter type

4. **Content Specifications** (Required)
   - Words Per Chapter (1000-10000)
   - Include Exercises: Yes/No
   - Include Case Studies: Yes/No
   - Tone: Professional/Casual/Academic
   - Infographic Style: Modern/Minimalist/Professional/Creative/Technical

5. **Storage Options** (Required)
   - Primary Storage: Google Drive / Local Folder
   - Local Folder Path (conditional, shown if Local selected)
   - Also Create Local Copy: Yes/No
   - Folder organization options (by date, by topic)

6. **Styling** (Optional)
   - Checkbox: Use Professional Defaults
   - If unchecked, show advanced options:
     * Font Family
     * Heading Font
     * Primary Color (color picker)
     * Secondary Color (color picker)
     * Page Size
     * Margins

7. **Generate Button**
   - Shows estimated time (10-15 minutes)
   - Shows total chapters
   - Shows estimated word count
   - Disabled until all required fields filled

8. **Real-Time Progress** (During Generation)
   - Overall progress bar (0-100%)
   - Current agent display (1-13)
   - Estimated time remaining
   - Agent status list with checkmarks/pending indicators
   - Live log output
   - Cancel button

#### UI-2: History Page (`/history`)
**Required Elements**:
- Filters: Status, Language, Date Range
- Search bar: Search topics
- Table/Grid view of generations:
  - Topic sentence
  - Generated date/time
  - Status (Done/Processing/Failed)
  - Chapters count
  - Word count
  - Language
  - Quality score (star rating)
  - Fact accuracy percentage
  - Actions: Download PDF, Google Drive Link, View Report, Regenerate, Delete
- Pagination: Load more button
- Sort options: Date, Quality, Topic

#### UI-3: Admin Dashboard (`/admin`)
**Required Authentication**:
- Admin login form (username/password)
- Session management
- Auto-logout after 30 minutes inactivity

**Tabs**:
1. **Overview**
   - Total generations (all time)
   - Generations today
   - This week count
   - Success rate percentage
   - Average generation time
   - Storage used (Google Drive, MinIO)
   - Active generations count
   - Queued tasks count
   - Recent activity feed

2. **All Generations**
   - Table with: User, Topic, Language, Chapters, Status, GDrive Link, Actions
   - Filters: User, Status, Date
   - Search: Search topics
   - Export: CSV, JSON, PDF Report
   - Actions per generation: View Details, Download, Delete

3. **System Monitoring**
   - CPU usage (Ollama, overall)
   - Memory usage
   - Disk usage
   - Docker container status (running/stopped)
   - Celery workers (active/total, queue length)
   - Redis cache hit rate

4. **Configuration**
   - View/edit app-config.json
   - LLM model selection
   - Image generation model selection
   - Generation settings
   - Performance settings

5. **Users**
   - User list
   - Add user form
   - Edit user (role, password reset)
   - Delete user

---

## 6. System Architecture

### 6.1 Agent Orchestration

#### 6.1.1 Sequential vs Parallel Execution

**Sequential Agents** (must complete in order):
1. Configuration Loader
2. Topic Analysis
3. Content Strategy
10. SEO & Metadata
11. Layout & Formatting
12. PDF Generation
13. Storage Integration

**Parallel Agents** (can run simultaneously):
4. Research Swarm (3 parallel agents)
5. Chapter Generation Swarm (N parallel agents, one per chapter)
6. Infographic Generation (N parallel agents, one per chapter)
7. Visual Design (can run parallel with Quality Enhancement)
8. Quality Enhancement (can run parallel with Critic)
9. Critic & Proofreading (multi-pass, but passes can be parallelized)

#### 6.1.2 Execution Flow

```
User Input (Topic + Config)
    ↓
[1] Configuration Loader (20s)
    ↓
[2] Topic Analysis (30s)
    ↓
[3] Content Strategy (45s)
    ↓
[4] Research Swarm (2min) ──┬─→ Agent A: Trends & Stats
    ├───→ Agent B: Sources & Examples
    └───→ Agent C: Market Analysis
    ↓ (Aggregate Results)
[5] Chapter Generation Swarm (3-5min) ──┬─→ Basic Chapter Agent 1
    ├───→ Basic Chapter Agent 2
    ├───→ ... (all chapters parallel)
    └───→ Two-Level Chapter Agent N
    ↓ (All Chapters Complete)
[6] Infographic Generation (2-3min) ──┬─→ Chapter 1 Infographic
    ├───→ Chapter 2 Infographic
    └───→ Chapter N Infographic
    ↓ (All Infographics Complete)
[7] Visual Design (30s)
    ↓
[8] Quality Enhancement (1min) + [9] Critic & Proofreading (2-3min) (Parallel)
    ↓
[10] SEO & Metadata (30s)
    ↓
[11] Layout & Formatting (1min)
    ↓
[12] PDF Generation (1min)
    ↓
[13] Storage Integration (30s)
    ↓
Output: PDF + Links + Reports
```

#### 6.1.3 Error Handling

**Per-Agent Error Handling**:
- Retry logic: 3 attempts with exponential backoff
- Fallback to alternative models (e.g., Ollama → OpenAI API)
- Graceful degradation (e.g., if infographic fails, continue with text-only)
- Log all errors with context

**Pipeline-Level Error Handling**:
- Rollback partial results
- Notify user of failure
- Save error log for debugging
- Offer retry option

---

### 6.2 Data Flow

#### 6.2.1 Input Data Flow

```
User Input (Web UI)
    ↓
Frontend Validation
    ↓
POST /api/generation/start
    ↓
Backend Validation
    ↓
Create Celery Task
    ↓
Task Queue (Redis)
    ↓
Celery Worker Picks Up Task
    ↓
Agent Orchestration
    ↓
Database Updates (PostgreSQL)
    ↓
File Storage (MinIO + Google Drive)
    ↓
WebSocket Update (Progress)
    ↓
Frontend Display
```

#### 6.2.2 Output Data Flow

```
Agent Output
    ↓
Temporary Storage (/output)
    ↓
MinIO Upload (S3-compatible)
    ↓
Google Drive Upload (if enabled)
    ↓
Local Copy (if enabled)
    ↓
Database Update (paths, links)
    ↓
WebSocket Notification (Complete)
    ↓
Frontend Display (Download Links)
```

---

## 7. API Specifications

### 7.1 Authentication API

#### POST /api/auth/login
**Description**: Authenticate user and receive JWT token

**Request**:
```json
{
  "username": "admin",
  "password": "secure_password"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "email": "admin@example.com"
  }
}
```

**Error Responses**:
- 401 Unauthorized: Invalid credentials
- 400 Bad Request: Missing fields

---

#### POST /api/auth/logout
**Description**: Invalidate JWT token

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "message": "Successfully logged out"
}
```

---

#### POST /api/auth/refresh
**Description**: Refresh access token

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

#### GET /api/auth/me
**Description**: Get current user info

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "admin",
  "role": "admin",
  "email": "admin@example.com",
  "created_at": "2025-01-01T00:00:00Z",
  "last_login": "2025-01-15T12:00:00Z"
}
```

---

### 7.2 Generation API

#### POST /api/generation/start
**Description**: Start a new ebook generation

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "topic_sentence": "The impact of artificial intelligence on healthcare",
  "config": {
    "language": "en",
    "chapter_structure": {
      "basic_chapters": 5,
      "one_level_depth_chapters": 3,
      "two_level_depth_chapters": 2
    },
    "content_specs": {
      "words_per_chapter": 3500,
      "include_exercises": true,
      "include_case_studies": true,
      "tone": "professional",
      "infographic_style": "modern"
    },
    "storage_options": {
      "google_drive": true,
      "create_local_copy": false
    }
  }
}
```

**Response** (202 Accepted):
```json
{
  "generation_id": 123,
  "task_id": "celery-task-uuid",
  "status": "pending",
  "estimated_time_seconds": 900,
  "message": "Generation started successfully"
}
```

**Validation Rules**:
- `topic_sentence`: 3-500 characters, required
- `config.language`: Must be in supported list, required
- `config.chapter_structure`: All types ≥0, sum ≥1, ≤45
- `config.content_specs.words_per_chapter`: 1000-10000

---

#### GET /api/generation/:id/status
**Description**: Get real-time status of a generation

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "generation_id": 123,
  "status": "processing",
  "progress": 40,
  "current_agent": "Chapter Generation",
  "current_agent_number": 5,
  "total_agents": 13,
  "estimated_time_remaining_seconds": 480,
  "started_at": "2025-01-15T12:00:00Z",
  "completed_at": null,
  "agent_status": [
    {
      "agent_number": 1,
      "agent_name": "Configuration Loader",
      "status": "completed",
      "execution_time_seconds": 18
    },
    {
      "agent_number": 2,
      "agent_name": "Topic Analysis",
      "status": "completed",
      "execution_time_seconds": 32
    },
    {
      "agent_number": 5,
      "agent_name": "Chapter Generation",
      "status": "in_progress",
      "sub_progress": {
        "basic_complete": 5,
        "basic_total": 5,
        "one_level_complete": 2,
        "one_level_total": 3,
        "two_level_complete": 0,
      "two_level_total": 2
      }
    }
  ]
}
```

**Status Values**: `pending`, `processing`, `completed`, `failed`

---

#### GET /api/generation/:id/details
**Description**: Get full details of a completed generation

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "id": 123,
  "user_id": 1,
  "topic_sentence": "The impact of artificial intelligence on healthcare",
  "config": { ... },
  "status": "completed",
  "progress": 100,
  "started_at": "2025-01-15T12:00:00Z",
  "completed_at": "2025-01-15T12:12:34Z",
  "generation_time_seconds": 754,
  "output": {
    "pdf_path": "/output/ai_healthcare_v1.0.pdf",
    "pdf_minio_path": "https://minio.example.com/ebooks/ai_healthcare_v1.0.pdf",
    "gdrive_link": "https://drive.google.com/file/d/abc123/view",
    "local_path": null,
    "infographics": [
      {
        "chapter_number": 1,
        "image_path": "/infographics/chapter_1_infographic.png",
        "minio_path": "https://minio.example.com/infographics/chapter_1_infographic.png"
      }
    ]
  },
  "stats": {
    "total_chapters": 10,
    "total_words": 35420,
    "total_infographics": 10
  },
  "quality_metrics": {
    "readability_score": 72,
    "grammar_score": 100,
    "fact_accuracy_score": 96
  },
  "fact_verification": {
    "total_claims_checked": 147,
    "claims_verified": 139,
    "claims_corrected": 8,
    "claims_flagged": 0,
    "confidence_score": 96
  }
}
```

---

#### GET /api/generation/:id/download
**Description**: Download generated PDF

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
- Content-Type: application/pdf
- Content-Disposition: attachment; filename="ai_healthcare_v1.0.pdf"
- Body: PDF binary data

---

#### DELETE /api/generation/:id
**Description**: Delete a generation record

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "message": "Generation deleted successfully",
  "generation_id": 123
}
```

---

### 7.3 Admin API

#### GET /api/admin/generations
**Description**: Get all generations (admin only)

**Headers**: `Authorization: Bearer <admin_token>`

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `status`: Filter by status
- `user_id`: Filter by user
- `start_date`: Filter start date
- `end_date`: Filter end date

**Response** (200 OK):
```json
{
  "total": 1247,
  "page": 1,
  "limit": 20,
  "generations": [
    {
      "id": 123,
      "user_id": 1,
      "user_email": "user1@example.com",
      "topic_sentence": "AI in healthcare",
      "language": "en",
      "status": "completed",
      "created_at": "2025-01-15T12:00:00Z",
      "gdrive_link": "https://drive.google.com/file/d/abc123/view",
      "quality_score": 92
    }
  ]
}
```

---

#### GET /api/admin/stats
**Description**: Get system statistics (admin only)

**Headers**: `Authorization: Bearer <admin_token>`

**Response** (200 OK):
```json
{
  "overview": {
    "total_generations": 1247,
    "generations_today": 23,
    "generations_this_week": 156,
    "success_rate": 98.7,
    "average_generation_time_seconds": 765
  },
  "storage": {
    "google_drive_used_gb": 2.3,
    "google_drive_limit_gb": 15.0,
    "minio_used_gb": 1.8,
    "minio_limit_gb": null
  },
  "active": {
    "active_generations": 3,
    "queued_tasks": 7
  },
  "quality": {
    "average_readability_score": 68,
    "average_grammar_score": 99,
    "average_fact_accuracy_score": 94
  }
}
```

---

#### PUT /api/admin/config
**Description**: Update system configuration (admin only)

**Headers**: `Authorization: Bearer <admin_token>`

**Request**:
```json
{
  "llm_settings": {
    "provider": "ollama",
    "model": "llama3.1:8b"
  },
  "generation_settings": {
    "default_language": "en",
    "max_concurrent_generations": 3
  }
}
```

**Response** (200 OK):
```json
{
  "message": "Configuration updated successfully",
  "config": { ... }
}
```

---

### 7.4 WebSocket Events

#### Event: generation_progress
**Description**: Real-time progress updates

**Payload**:
```json
{
  "generation_id": 123,
  "status": "processing",
  "progress": 40,
  "current_agent": "Chapter Generation",
  "current_agent_number": 5,
  "total_agents": 13,
  "estimated_time_remaining_seconds": 480,
  "log_message": "Generated Chapter 5 (Basic)"
}
```

---

#### Event: generation_complete
**Description**: Generation completed successfully

**Payload**:
```json
{
  "generation_id": 123,
  "status": "completed",
  "output": {
    "pdf_link": "https://minio.example.com/ebooks/ai_healthcare_v1.0.pdf",
    "gdrive_link": "https://drive.google.com/file/d/abc123/view",
    "fact_verification_report": "https://minio.example.com/reports/fact_verification_123.pdf"
  },
  "quality_metrics": {
    "readability_score": 72,
    "fact_accuracy_score": 96
  }
}
```

---

#### Event: generation_failed
**Description**: Generation failed

**Payload**:
```json
{
  "generation_id": 123,
  "status": "failed",
  "error_message": "Ollama API timeout during Chapter Generation",
  "failed_at": "2025-01-15T12:08:45Z",
  "retry_available": true
}
```

---

## 8. Database Schema

### 8.1 Tables

#### 8.1.1 users
**Purpose**: Store user accounts and authentication

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Username |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| email | VARCHAR(100) | UNIQUE | Email address |
| role | VARCHAR(20) | DEFAULT 'user' | 'admin' or 'user' |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| last_login | TIMESTAMP | NULLABLE | Last login time |

**Indexes**:
- `idx_users_username` on (username)
- `idx_users_email` on (email)

---

#### 8.1.2 ebook_generations
**Purpose**: Store ebook generation records

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| user_id | INTEGER | FK → users(id) | User who created |
| topic_sentence | TEXT | NOT NULL | Input topic |
| config_json | JSONB | NOT NULL | Full configuration |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/processing/completed/failed |
| progress | INTEGER | DEFAULT 0 | 0-100 |
| current_agent | VARCHAR(50) | NULLABLE | Current agent name |
| started_at | TIMESTAMP | DEFAULT NOW() | Start time |
| completed_at | TIMESTAMP | NULLABLE | Completion time |
| pdf_path | TEXT | NULLABLE | Local PDF path |
| pdf_minio_path | TEXT | NULLABLE | MinIO PDF URL |
| gdrive_link | TEXT | NULLABLE | Google Drive URL |
| gdrive_folder_id | TEXT | NULLABLE | GDrive folder ID |
| local_path | TEXT | NULLABLE | Local copy path |
| total_chapters | INTEGER | NULLABLE | Total chapters generated |
| total_words | INTEGER | NULLABLE | Total words generated |
| total_infographics | INTEGER | NULLABLE | Total infographics |
| generation_time_seconds | INTEGER | NULLABLE | Total time |
| readability_score | FLOAT | NULLABLE | Flesch score |
| grammar_score | FLOAT | NULLABLE | Grammar % |
| fact_accuracy_score | FLOAT | NULLABLE | Fact accuracy % |
| error_message | TEXT | NULLABLE | Error details |
| retry_count | INTEGER | DEFAULT 0 | Retry attempts |
| version_number | INTEGER | DEFAULT 1 | Version for regeneration |
| parent_generation_id | INTEGER | FK → ebook_generations(id) | Parent version |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_generations_user` on (user_id)
- `idx_generations_status` on (status)
- `idx_generations_created` on (created_at DESC)
- `idx_generations_topic` on (topic_sentence) using GIN (for full-text search)

---

#### 8.1.3 fact_verifications
**Purpose**: Store fact-checking results

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| generation_id | INTEGER | FK → ebook_generations(id) | Generation |
| claim_text | TEXT | NOT NULL | Original claim |
| verified | BOOLEAN | NOT NULL | Verification result |
| confidence_score | FLOAT | NOT NULL | Confidence 0-100 |
| correction_before | TEXT | NULLABLE | Before correction |
| correction_after | TEXT | NULLABLE | After correction |
| verification_source | TEXT | NULLABLE | Source URL |
| created_at | TIMESTAMP | DEFAULT NOW() | Verification time |

**Indexes**:
- `idx_fact_verifications_generation` on (generation_id)
- `idx_fact_verifications_confidence` on (confidence_score)

---

#### 8.1.4 agent_logs
**Purpose**: Store agent execution logs

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| generation_id | INTEGER | FK → ebook_generations(id) | Generation |
| agent_name | VARCHAR(50) | NOT NULL | Agent name |
| agent_number | INTEGER | NOT NULL | Agent 1-13 |
| status | VARCHAR(20) | NOT NULL | pending/in_progress/completed/failed |
| input_data | JSONB | NULLABLE | Agent input |
| output_data | JSONB | NULLABLE | Agent output |
| execution_time_seconds | FLOAT | NULLABLE | Execution time |
| started_at | TIMESTAMP | DEFAULT NOW() | Start time |
| completed_at | TIMESTAMP | NULLABLE | Completion time |
| error_message | TEXT | NULLABLE | Error details |

**Indexes**:
- `idx_agent_logs_generation` on (generation_id)
- `idx_agent_logs_agent` on (agent_number)

---

#### 8.1.5 infographics
**Purpose**: Store infographic metadata

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| generation_id | INTEGER | FK → ebook_generations(id) | Generation |
| chapter_number | INTEGER | NOT NULL | Chapter number |
| image_path | TEXT | NULLABLE | Local path |
| minio_path | TEXT | NULLABLE | MinIO URL |
| visualization_type | VARCHAR(50) | NULLABLE | flowchart/mindmap/etc |
| generation_method | VARCHAR(50) | NULLABLE | sdxl/mermaid/matplotlib |
| prompt_used | TEXT | NULLABLE | Generation prompt |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_infographics_generation` on (generation_id)

---

#### 8.1.6 api_usage
**Purpose**: Track API usage and costs

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| generation_id | INTEGER | FK → ebook_generations(id) | Generation |
| provider | VARCHAR(50) | NOT NULL | ollama/openai/anthropic |
| model | VARCHAR(100) | NOT NULL | Model name |
| request_type | VARCHAR(50) | NOT NULL | text_generation/image_generation |
| tokens_used | INTEGER | NULLABLE | Token count |
| cost_usd | FLOAT | NULLABLE | Cost in USD |
| timestamp | TIMESTAMP | DEFAULT NOW() | Request time |

**Indexes**:
- `idx_api_usage_generation` on (generation_id)
- `idx_api_usage_provider` on (provider)
- `idx_api_usage_timestamp` on (timestamp DESC)

---

#### 8.1.7 shared_ebooks
**Purpose**: Store shared ebook links

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| generation_id | INTEGER | FK → ebook_generations(id) | Generation |
| shared_by_user_id | INTEGER | FK → users(id) | Sharer |
| shared_with_email | VARCHAR(255) | NULLABLE | Recipient email |
| access_token | UUID | DEFAULT gen_random_uuid() | Access token |
| can_edit | BOOLEAN | DEFAULT FALSE | Edit permission |
| can_comment | BOOLEAN | DEFAULT TRUE | Comment permission |
| expires_at | TIMESTAMP | NULLABLE | Expiry time |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_shared_ebooks_generation` on (generation_id)
- `idx_shared_ebooks_token` on (access_token)

---

#### 8.1.8 ebook_comments
**Purpose**: Store comments on shared ebooks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| generation_id | INTEGER | FK → ebook_generations(id) | Generation |
| user_id | INTEGER | FK → users(id) | Commenter |
| comment_text | TEXT | NOT NULL | Comment content |
| chapter_reference | INTEGER | NULLABLE | Chapter number |
| created_at | TIMESTAMP | DEFAULT NOW() | Comment time |

**Indexes**:
- `idx_ebook_comments_generation` on (generation_id)

---

#### 8.1.9 ebook_templates
**Purpose**: Store user-created templates

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| name | VARCHAR(255) | NOT NULL | Template name |
| category | VARCHAR(100) | NULLABLE | Business/Technical/etc |
| description | TEXT | NULLABLE | Template description |
| config_json | JSONB | NOT NULL | Template config |
| is_public | BOOLEAN | DEFAULT TRUE | Public/private |
| created_by_user_id | INTEGER | FK → users(id) | Creator |
| usage_count | INTEGER | DEFAULT 0 | Times used |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_ebook_templates_category` on (category)
- `idx_ebook_templates_public` on (is_public)

---

#### 8.1.10 user_budgets
**Purpose**: Track user budgets and costs

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| user_id | INTEGER | FK → users(id) | User |
| monthly_budget_usd | DECIMAL(10,2) | NOT NULL | Monthly budget |
| current_spend_usd | DECIMAL(10,2) | DEFAULT 0.00 | Current spend |
| alert_threshold_percent | INTEGER | DEFAULT 80 | Alert threshold |
| alert_email_sent | BOOLEAN | DEFAULT FALSE | Alert sent |
| month | INTEGER | NOT NULL | Month (1-12) |
| year | INTEGER | NOT NULL | Year |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_user_budgets_user_month` on (user_id, month, year) UNIQUE

---

### 8.2 Relationships

```
users (1) ──< (N) ebook_generations
ebook_generations (1) ──< (N) fact_verifications
ebook_generations (1) ──< (N) agent_logs
ebook_generations (1) ──< (N) infographics
ebook_generations (1) ──< (N) api_usage
ebook_generations (1) ──< (N) shared_ebooks
ebook_generations (1) ──< (N) ebook_comments
users (1) ──< (N) shared_ebooks (as shared_by)
users (1) ──< (N) ebook_comments
users (1) ──< (N) ebook_templates
users (1) ──< (N) user_budgets
ebook_generations (1) ──< (N) ebook_generations (as parent, for versions)
```

---

## 9. Non-Functional Requirements

### 9.1 Performance Requirements

#### NFR-1: Response Time
- **API Endpoints**: <200ms average (p50), <500ms p95
- **WebSocket Events**: <100ms latency
- **Database Queries**: <100ms average
- **PDF Generation**: <60 seconds per ebook
- **Single Ebook Generation**: 10-15 minutes total

#### NFR-2: Throughput
- **Concurrent Generations**: Support 3 simultaneous pipelines
- **API Requests**: Handle 100 requests/second
- **WebSocket Connections**: Support 50 concurrent connections
- **Database Connections**: Pool of 20 connections

#### NFR-3: Scalability
- **Horizontal Scaling**: Add more Celery workers to increase capacity
- **Vertical Scaling**: Support larger chapter counts (up to 45)
- **Database Sharding**: Partition by user_id for >10k users
- **CDN Integration**: Serve static assets via CDN

---

### 9.2 Reliability Requirements

#### NFR-4: Availability
- **Uptime Target**: 99.5% (3.65 hours downtime/month)
- **Maintenance Window**: 2 hours/month, announced 48h in advance
- **Backup Frequency**: Daily automated backups

#### NFR-5: Error Handling
- **Success Rate**: >98% of generations complete successfully
- **Retry Logic**: 3 automatic retries with exponential backoff
- **Fallback**: If local model fails, fallback to API (if configured)
- **Graceful Degradation**: If infographic fails, continue with text-only

#### NFR-6: Data Integrity
- **ACID Compliance**: All database transactions must be ACID-compliant
- **Backup Verification**: Weekly backup restoration tests
- **Data Retention**: Keep all generations for minimum 1 year

---

### 9.3 Security Requirements

#### NFR-7: Authentication
- **Password Hashing**: Bcrypt with salt, cost factor 12
- **JWT Tokens**: Short-lived (1 hour), refresh tokens (30 days)
- **Session Management**: Auto-logout after 30 minutes inactivity
- **Multi-Factor Authentication**: Optional for admin users

#### NFR-8: Authorization
- **Role-Based Access**: Admin vs. User roles
- **API Key Protection**: Never expose API keys in frontend
- **Resource Ownership**: Users can only access their own generations
- **Admin Isolation**: Admin operations require elevated privileges

#### NFR-9: Data Protection
- **Encryption in Transit**: TLS 1.3 for all HTTPS connections
- **Encryption at Rest**: PostgreSQL data encryption at rest
- **Secrets Management**: Environment variables for sensitive data
- **Input Validation**: Sanitize all user inputs to prevent SQL injection, XSS

#### NFR-10: Compliance
- **GDPR**: Support right to erasure (delete user data)
- **Data Residency**: Store data in user-specified region (future)
- **Audit Logging**: Log all admin actions for accountability

---

### 9.4 Maintainability Requirements

#### NFR-11: Code Quality
- **Type Safety**: TypeScript for frontend, type hints for Python
- **Code Coverage**: >80% test coverage for critical paths
- **Linting**: ESLint (frontend), Pylint (backend)
- **Documentation**: Inline code comments, API docs (OpenAPI)

#### NFR-12: Monitoring
- **Application Logging**: Structured logs (JSON) for all operations
- **Error Tracking**: Sentry integration for error alerts
- **Performance Monitoring**: Prometheus metrics for API latency
- **Health Checks**: `/health` endpoint returning system status

#### NFR-13: Deployment
- **Docker Images**: Versioned Docker tags for reproducibility
- **CI/CD Pipeline**: Automated testing on pull requests
- **Rollback Strategy**: Immediate rollback on critical bugs
- **Blue-Green Deployment**: Zero-downtime deployments

---

### 9.5 Usability Requirements

#### NFR-14: Accessibility
- **WCAG 2.1 AA**: Compliance for web accessibility
- **Keyboard Navigation**: All features accessible via keyboard
- **Screen Reader Support**: Proper ARIA labels
- **Color Contrast**: Minimum 4.5:1 contrast ratio

#### NFR-15: Internationalization
- **RTL Support**: Proper right-to-left layout for Arabic
- **Character Encoding**: UTF-8 for all content
- **Date/Time Formats**: Locale-specific formatting
- **Number Formatting**: Locale-specific (e.g., commas vs. periods)

#### NFR-16: Browser Support
- **Modern Browsers**: Chrome 120+, Firefox 120+, Safari 17+, Edge 120+
- **Mobile Support**: Responsive design for tablets and smartphones

---

## 10. Implementation Phases

### Phase 1: Core Pipeline with Zero Interaction (Weeks 1-6)

**Goal**: Working system that generates ebooks from topic sentence

**Deliverables**:
- Agent 1: Configuration Loader (JSON support)
- Agent 2: Topic Analysis
- Agent 3: Content Strategy (Basic/One-Level/Two-Level structure)
- Agent 4: Research Swarm (parallel)
- Agent 5: Chapter Generation (multi-level parallel)
- Agent 8: Quality Enhancement
- Agent 9: Critic & Proofreading (strong fact validation)
- Agent 10: SEO & Metadata
- Agent 11: Layout & Formatting
- Agent 12: PDF Generation
- Agent 13: Storage Integration (Google Drive + local)
- Skill 1: `/ebook-generate` (zero manual interaction)
- Skill 3: `/ebook-config-create`
- Skill 7: `/ebook-storage-setup`

**Success Criteria**:
- User can generate ebook from topic sentence
- PDF includes all chapters with proper formatting
- Fact verification report generated
- PDF uploaded to Google Drive
- Generation completes in 15 minutes or less

**Testing**:
- Unit tests for each agent
- Integration tests for full pipeline
- E2E test: Generate "AI in healthcare" ebook, verify quality

---

### Phase 2: Infographic Generation & Web UI (Weeks 7-10)

**Goal**: Every chapter starts with professional infographic, intuitive web interface

**Deliverables**:
- Agent 6: Infographic Generation (one per chapter)
- Integration with SDXL Lightning / Mermaid / Python
- Image embedding in PDF
- Skill 9: `/ebook-infographic-only`
- Frontend: React + TypeScript + Tailwind
- Backend: FastAPI endpoints
- Pages: Generate, History, Login
- Real-time progress tracking (WebSocket)

**Success Criteria**:
- Every chapter includes infographic at beginning
- Web UI allows topic input and configuration
- Real-time progress shown during generation
- User can download PDF from history page

**Testing**:
- Visual regression tests for infographics
- UI component tests (Jest)
- E2E test: Generate ebook via web UI, verify infographics embedded

---

### Phase 3: Scale & Multi-Language (Weeks 11-14)

**Goal**: Generate multiple ebooks simultaneously, support 10 languages

**Deliverables**:
- Skill 2: `/ebook-batch` (3 pipelines in parallel)
- Multi-language support (10 languages)
- Language-specific grammar checking
- RTL language support (Arabic)
- Skill 8: `/ebook-stats`
- Advanced search & filtering
- Cost monitoring & budgets

**Success Criteria**:
- Generate 3 ebooks simultaneously in 20 minutes
- Generate Spanish ebook with proper grammar
- Generate Arabic ebook with RTL formatting
- User can view statistics dashboard

**Testing**:
- Load test: 10 concurrent generations
- Language test: Generate ebook in each supported language
- RTL test: Verify Arabic layout

---

### Phase 4: Advanced Features (Weeks 15-18)

**Goal**: Advanced workflows for power users

**Deliverables**:
- Agent 7: Visual Design (enhanced visual elements)
- Skill 4: `/ebook-template` (custom templates)
- Skill 5: `/ebook-quality-report` (detailed analysis)
- Skill 6: `/ebook-expand` (expand existing content)
- Email notifications
- Rate limiting
- Automated backups
- Version control for regenerations
- Collaborative features
- Template library

**Success Criteria**:
- User can create and save custom templates
- User can generate quality report for existing PDF
- User receives email when generation completes
- System backs up database daily
- User can share ebooks with comments

**Testing**:
- Template test: Generate ebook from custom template
- Email test: Verify email notifications sent
- Backup test: Restore from backup
- Collaboration test: Share ebook, add comment

---

### Phase 5: Admin Dashboard & Production Hardening (Weeks 19-22)

**Goal**: Complete admin oversight, production-ready deployment

**Deliverables**:
- Admin Dashboard with all tabs (Overview, Generations, Users, Monitoring, Config)
- Admin authentication and authorization
- System monitoring (CPU, memory, Docker, Celery)
- Export functionality (CSV, JSON, PDF)
- Production deployment (Docker Compose)
- Security hardening (TLS, rate limiting, input validation)
- Performance optimization (caching, database indexing)
- Documentation (user guide, API docs, deployment guide)

**Success Criteria**:
- Admin can view all generations with Google Drive links
- Admin can monitor system health in real-time
- System deployed to production environment
- All security requirements met
- Documentation complete

**Testing**:
- Security audit: Penetration testing
- Load test: 100 concurrent users
- Disaster recovery test: Restore from backup

---

## 11. Success Metrics

### 11.1 Technical Metrics

#### TM-1: Performance
- **Single Ebook Generation Time**: Target <15 minutes, Alert >20 minutes
- **API Response Time**: Target <200ms (p50), Alert >500ms (p95)
- **Database Query Time**: Target <100ms average
- **WebSocket Latency**: Target <100ms
- **PDF Generation Time**: Target <60 seconds

**Measurement**: Prometheus metrics, APM (Application Performance Monitoring)

#### TM-2: Quality
- **Flesch Reading Ease Score**: Target >60, Minimum 50
- **Grammar Accuracy**: Target 100%, Minimum 95%
- **Fact Accuracy**: Target >95%, Minimum 90% (gate below 90%)
- **Infographic Generation Success**: Target 100%, Minimum 95%
- **User Satisfaction Score**: Target >4.5/5, Minimum 4.0/5

**Measurement**: Automated quality checks, user surveys

#### TM-3: Reliability
- **Success Rate**: Target >98%, Minimum 95%
- **Uptime**: Target 99.5%, Minimum 99%
- **Error Recovery Rate**: Target >95% (automatic retries succeed)
- **Data Loss Incidents**: Target 0, Maximum 1 per year

**Measurement**: Uptime monitoring, error tracking (Sentry)

---

### 11.2 User Metrics

#### UM-1: Adoption
- **Total Users**: Target 100 users in first 3 months
- **Active Users**: Target 50 active users per week
- **Generations per User**: Target 5 generations per user per month
- **User Retention**: Target 70% return within 30 days

**Measurement**: Analytics (Google Analytics, Mixpanel)

#### UM-2: Engagement
- **Average Session Duration**: Target >10 minutes
- **Feature Usage**:
  - Configuration Creation: Target 80% of users
  - Batch Processing: Target 30% of users
  - Template Library: Target 40% of users
  - Quality Report: Target 50% of users

**Measurement**: Event tracking

#### UM-3: Satisfaction
- **Net Promoter Score (NPS)**: Target >50
- **User Feedback**: Positive sentiment >80%
- **Support Tickets**: <5 tickets per week per 100 users

**Measurement**: Surveys, feedback forms, support ticket analysis

---

### 11.3 Business Metrics

#### BM-1: Cost Efficiency
- **Cost per Ebook**: Target $0 (open-source models)
- **API Cost per User**: Target <$5/month (for users using paid APIs)
- **Infrastructure Cost**: Target <$50/month (Docker hosting)

**Measurement**: Cost tracking (AWS/GCP billing, MinIO storage)

#### BM-2: Time Savings
- **Manual Writing Time**: ~40 hours per ebook
- **Automated Generation Time**: ~15 minutes per ebook
- **Time Savings**: ~99.4% reduction (39.75 hours saved)

**Measurement**: User surveys, time tracking

#### BM-3: Scalability
- **Max Concurrent Generations**: 3 (Phase 1), 10 (Phase 3)
- **Monthly Generation Capacity**:
  - Phase 1: ~600 ebooks (3 concurrent × 15 min × 24 hrs × 30 days)
  - Phase 3: ~2,000 ebooks (10 concurrent × 15 min × 24 hrs × 30 days)

**Measurement**: Load testing

---

## 12. Risk Assessment

### 12.1 Technical Risks

#### Risk 1: LLM Model Quality
**Probability**: Medium
**Impact**: High
**Description**: Open-source CPU models (Llama 3.1 8B, Mistral 7B) may produce lower quality content compared to paid APIs (GPT-4o, Claude 3.5 Sonnet)

**Mitigation**:
- Fallback mechanism: If local model fails/timeout, use paid API (if configured)
- User choice: Allow users to select models (local vs. API)
- Quality monitoring: Track readability scores, user feedback
- Prompt engineering: Optimize prompts for open-source models

**Contingency**:
- If quality consistently <60% readability, default to paid APIs
- Provide clear warning to users about quality trade-offs

---

#### Risk 2: CPU Performance Bottlenecks
**Probability**: High
**Impact**: Medium
**Description**: CPU-based inference (Llama, SDXL) may be slow, causing generation timeouts

**Mitigation**:
- Optimize models: Use quantized versions (4-bit, 8-bit)
- Limit concurrency: Max 3 concurrent generations initially
- Implement queue: Queue tasks when system busy
- Progress feedback: Show accurate ETAs to users

**Contingency**:
- If average generation time >20 minutes, require GPU for production
- Offer GPU hosting option (AWS EC2 with GPU)

---

#### Risk 3: Fact Validation Accuracy
**Probability**: Medium
**Impact**: High
**Description**: Automated fact-checking may miss errors or flag correct claims, reducing trust

**Mitigation**:
- Multi-pass verification: 7-pass critic agent
- Confidence scoring: Require 2+ independent sources
- Human review: Flag low-confidence claims for manual review
- User feedback: Allow users to report fact errors

**Contingency**:
- If fact accuracy <90%, add mandatory human review step
- Provide disclaimer: "Content may require verification"

---

#### Risk 4: Google Drive API Limitations
**Probability**: Low
**Impact**: High
**Description**: Google Drive API has rate limits (e.g., 10,000 requests/day), may block automated uploads

**Mitigation**:
- Rate limiting: Throttle uploads to stay within limits
- Retry logic: Exponential backoff on rate limit errors
- Alternative storage: MinIO as primary, Google Drive as secondary
- User authentication: Use OAuth to leverage user quotas

**Contingency**:
- If Google Drive blocks uploads, disable temporarily, use MinIO only
- Provide clear error message to users

---

### 12.2 Security Risks

#### Risk 5: API Key Exposure
**Probability**: Low
**Impact**: Critical
**Description**: OpenAI/Anthropic API keys may be exposed in logs, frontend code, or database

**Mitigation**:
- Environment variables: Store keys in `.env` file (never in code)
- Server-side only: Never expose API keys to frontend
- Logging: Redact API keys from logs
- Encryption: Encrypt keys in database (if stored)

**Contingency**:
- If keys leaked, rotate immediately
- Monitor API usage for unusual patterns

---

#### Risk 6: Unauthorized Access
**Probability**: Low
**Impact**: High
**Description**: Attackers may gain access to admin dashboard, user data, or generation history

**Mitigation**:
- Strong authentication: Bcrypt with cost factor 12
- JWT validation: Verify tokens on every request
- Role-based access: Enforce admin-only endpoints
- Rate limiting: Prevent brute force attacks

**Contingency**:
- If breach detected, force password reset for all users
- Audit logs: Review all admin actions

---

### 12.3 Usability Risks

#### Risk 7: Complexity of Configuration
**Probability**: High
**Impact**: Medium
**Description**: Users may be overwhelmed by configuration options (language, chapter structure, styling, etc.)

**Mitigation**:
- Smart defaults: Pre-select common options (English, 5+3+2 chapters)
- Tooltips: Add "?" icons with explanations
- Progressive disclosure: Hide advanced options behind "Advanced" toggle
- Templates: Provide pre-built templates for common use cases

**Contingency**:
- If user surveys show <70% satisfaction, simplify UI
- Add onboarding tutorial/walkthrough

---

#### Risk 8: Unrealistic Quality Expectations
**Probability**: Medium
**Impact**: Medium
**Description**: Users may expect human-writer quality, be disappointed by AI-generated content

**Mitigation**:
- Clear communication: Set expectations in marketing ("AI-generated, may require editing")
- Quality reports: Show quality metrics (readability, fact accuracy)
- Sample ebooks: Provide example ebooks before user generates
- Editing tools: Allow users to edit generated content before PDF export

**Contingency**:
- If refund requests >10%, review quality thresholds
- Add human editing service (paid add-on)

---

### 12.4 Business Risks

#### Risk 9: Competing Products
**Probability**: High
**Impact**: Medium
**Description**: Other AI ebook generators (e.g., Jasper, Copy.ai) may offer similar features

**Mitigation**:
- Differentiation: Emphasize unique features (fact validation, infographics, zero interaction)
- Open-source: Appeal to users who want privacy, no subscription fees
- Multi-language: Support languages competitors don't
- Quality: Focus on 95%+ fact accuracy vs. competitors' lack of validation

**Contingency**:
- If market share <5%, pivot to enterprise features (API, white-label)

---

#### Risk 10: Legal Issues
**Probability**: Low
**Impact**: High
**Description**: Copyright infringement, plagiarism, or libel in AI-generated content

**Mitigation**:
- Fact validation: Ensure claims are verified, cited
- Plagiarism check: Compare content against existing sources
- Disclaimer: Add copyright notice ("AI-generated, verify before publishing")
- User agreement: Require users to accept liability for published content

**Contingency**:
- If sued, investigate claim, remove infringing content
- Add legal review step for high-risk topics (medical, legal)

---

### 12.5 Risk Monitoring

**Weekly Risk Review**:
- Review error logs for new risks
- Monitor user feedback for complaints
- Track quality metrics for degradation

**Monthly Risk Assessment**:
- Re-evaluate probability and impact
- Update mitigation strategies
- Escalate critical risks to stakeholders

**Quarterly Risk Report**:
- Summary of all risks and mitigation status
- New risks identified
- Retired risks (resolved)

---

## Appendix

### A. Glossary

- **Basic Chapter**: Single-level content, linear flow, introductory concepts
- **One-Level Depth Chapter**: Main sections with 2-3 subsections each
- **Two-Level Depth Chapter**: Complex nested hierarchies with detailed analysis
- **Agent**: Specialized AI module performing specific task (e.g., Topic Analysis Agent)
- **Skill**: User-invocable command combining multiple agents (e.g., `/ebook-generate`)
- **Critic & Proofreading Agent**: 7-pass fact validation agent ensuring 95%+ accuracy
- **Infographic**: Visual summary of chapter contents (flowchart, mind map, etc.)
- **Ollama**: Local LLM serving engine (CPU-based)
- **SDXL Lightning**: Fast 4-step image generation model
- **MinIO**: S3-compatible object storage
- **Celery**: Distributed task queue for background processing
- **RTL**: Right-to-left language formatting (e.g., Arabic)

---

### B. References

1. **Architecture Documents**:
   - `rustling-dancing-book.md`: Complete system architecture
   - `simple.md`: Web application architecture

2. **Technologies**:
   - FastAPI: https://fastapi.tiangolo.com/
   - React: https://react.dev/
   - Ollama: https://ollama.ai/
   - Stable Diffusion XL: https://huggingface.co/stabilityai/sdxl-turbo
   - Celery: https://docs.celeryq.dev/
   - PostgreSQL: https://www.postgresql.org/docs/
   - Redis: https://redis.io/docs/
   - MinIO: https://min.io/docs/

3. **Standards**:
   - WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
   - OpenAPI Specification: https://swagger.io/specification/
   - JWT: https://jwt.io/

---

### C. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-15 | System | Initial PRD creation |

---

### D. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Tech Lead | | | |
| Security Lead | | | |

---

**END OF PRD**
