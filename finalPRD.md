# PRODUCT REQUIREMENTS DOCUMENT (PRD)
## Automated PDF Ebook Creation System - Web Application

---

## DOCUMENT CONTROL

| Version | Date | Author | Status | Changes |
|---------|------|--------|--------|---------|
| 1.0 | 2026-01-15 | Product Team | Draft | Initial comprehensive PRD creation |

---

## APPROVALS

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Tech Lead | | | |
| Architect | | | |
| Security Lead | | | |

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Product Overview & Vision](#2-product-overview--vision)
3. [Project Objectives](#3-project-objectives)
4. [Target Audience & User Personas](#4-target-audience--user-personas)
5. [Functional Requirements](#5-functional-requirements)
6. [Technical Architecture](#6-technical-architecture)
7. [Agent Orchestration Strategy](#7-agent-orchestration-strategy)
8. [System Specifications](#8-system-specifications)
9. [User Interface Requirements](#9-user-interface-requirements)
10. [API Specifications](#10-api-specifications)
11. [Database Schema](#11-database-schema)
12. [Non-Functional Requirements](#12-non-functional-requirements)
13. [Implementation Roadmap](#13-implementation-roadmap)
14. [Success Metrics & KPIs](#14-success-metrics--kpis)
15. [Risk Assessment](#15-risk-assessment)
16. [Resource Requirements](#16-resource-requirements)
17. [Appendices](#17-appendices)

---

# 1. EXECUTIVE SUMMARY

## 1.1 Product Vision

The **Automated PDF Ebook Creation System** is a revolutionary, zero-manual-interaction platform that transforms simple topic sentences into publication-ready, professional PDF ebooks. By leveraging a multi-agent architecture with **13 specialized AI agents**, the system delivers comprehensive, fact-verified, visually enhanced ebooks with embedded infographics in **10-15 minutes**—a process that traditionally takes weeks.

## 1.2 Value Proposition

| Traditional Approach | Our Solution |
|---------------------|--------------|
| 4-8 weeks for ebook creation | 10-15 minutes automated generation |
| Manual research and writing | AI-powered parallel research swarm |
| No fact verification | 7-pass rigorous fact validation (95%+ accuracy) |
| Text-only content | **Mandatory infographic per chapter** |
| Single language output | 10 languages with proper grammar support |
| Manual formatting | Professional PDF with embedded graphics |
| Manual file storage | Automatic Google Drive + local storage |
| Expensive human writers | $0 with open-source CPU models |

## 1.3 Key Differentiators

1. **True Zero-Interaction Automation**: No checkpoints, approvals, or manual intervention required
2. **Mandatory Visual Enhancement**: Every chapter includes AI-generated infographic
3. **Rigorous Fact Validation**: 95%+ accuracy through 7-pass verification process
4. **Flexible Content Structure**: Basic, One-Level, and Two-Level chapter depth options
5. **Multi-Language Native Support**: 10 languages with RTL and proper grammar checking
6. **Dual Storage Architecture**: Google Drive + optional local folder with automated management
7. **Open-Source First**: CPU-optimized models with optional API fallbacks

## 1.4 Market Opportunity

- **Content Creator Market**: 4M+ active creators seeking scalable content production
- **Corporate Training**: $370B global market requiring rapid documentation
- **Self-Publishing**: 2M+ annual titles, growing 15% YoY
- **Educational Resources**: K-12 and higher education demand for customized materials

---

# 2. PRODUCT OVERVIEW & VISION

## 2.1 Product Description

A comprehensive web-based platform that enables users to generate professional PDF ebooks through a completely automated pipeline. Users provide minimal input (topic sentence + optional configuration), and the system orchestrates **13 specialized AI agents** to research, write, enhance, verify, and deliver publication-ready content.

## 2.2 Core Product Philosophy

**ZERO DEFAULTS - USER CHOICE ONLY**

The system operates on the principle that users must explicitly specify all critical parameters. No intelligent defaults are applied without user awareness, ensuring complete control over:
- Language selection
- Chapter structure and depth
- Content specifications
- Storage destinations
- Styling preferences

## 2.3 Vision Statement

> To democratize professional ebook creation by making it accessible, fast, and free for everyone, regardless of technical expertise or language, while maintaining the highest standards of quality and accuracy.

## 2.4 Product Scope

### In Scope:
- Single and batch ebook generation (up to 10 simultaneous)
- 10 language support with native grammar checking
- Multi-level chapter structure (Basic, One-Level, Two-Level)
- Mandatory infographic generation (one per chapter)
- Fact validation with confidence scoring
- Dual storage (Google Drive + local)
- Web-based user interface
- Configuration management and templates
- Generation history and reporting
- Admin dashboard with complete oversight

### Out of Scope (Phase 1):
- Physical book printing services
- eBook marketplace distribution (Amazon KDP, etc.)
- Interactive eBook formats (EPUB, MOBI)
- Real-time collaborative editing
- Video/audio content generation
- Print-on-demand integration

---

# 3. PROJECT OBJECTIVES

## 3.1 Primary Objectives (Must Achieve)

| ID | Objective | Description | Success Criteria |
|----|-----------|-------------|------------------|
| **O1** | Zero-Interaction Pipeline | User provides topic only; system delivers PDF without additional input | No checkpoints or manual interventions required |
| **O2** | Factual Accuracy | Achieve 95%+ factual accuracy | Fact validation agent scores >=95% on verified claims |
| **O3** | Visual Enhancement | Generate one infographic per chapter | 100% of chapters include embedded visual summary |
| **O4** | Multi-Language Support | Support 10 languages with proper grammar | LanguageTool integration for all supported languages |
| **O5** | Performance Target | Complete generation in <=15 minutes | End-to-end pipeline completes within 15 minutes for 10-chapter ebook |
| **O6** | Batch Processing | Enable batch processing (3 parallel pipelines) | Generate 3 ebooks simultaneously without degradation |
| **O7** | Dual Storage | Provide dual storage with automated management | Google Drive + local folder with configurable options |

## 3.2 Secondary Objectives (Should Achieve)

| ID | Objective | Priority |
|----|-----------|----------|
| **S1** | Template library for common genres | Medium |
| **S2** | Version control for regenerations | Medium |
| **S3** | Advanced search and filtering | Medium |
| **S4** | Collaborative sharing features | Low |
| **S5** | Cost monitoring and budgeting | Low |

---

# 4. TARGET AUDIENCE & USER PERSONAS

## 4.1 Primary User Personas

### Persona 1: Content Creator / Author
| Attribute | Description |
|-----------|-------------|
| **Name** | Sarah Chen |
| **Role** | Full-time content creator, 150K subscribers |
| **Goals** | Scale content production, maintain quality |
| **Pain Points** | Writing bottleneck, research time, fact-checking |
| **Technical Proficiency** | Medium |
| **Use Case** | Generate lead magnet ebooks from video topics |
| **Languages** | English, Spanish |
| **Expected Usage** | 10+ ebooks per month |

### Persona 2: Corporate Trainer
| Attribute | Description |
|-----------|-------------|
| **Name** | Marcus Williams |
| **Role** | L&D Manager at Fortune 500 company |
| **Goals** | Rapid training material creation, consistency |
| **Pain Points** | Subject matter experts unavailable, formatting delays |
| **Technical Proficiency** | Medium-High |
| **Use Case** | Create training manuals from policy documents |
| **Languages** | English only |
| **Expected Usage** | 5+ ebooks per month |

### Persona 3: Academic Researcher
| Attribute | Description |
|-----------|-------------|
| **Name** | Dr. Elena Rodriguez |
| **Role** | University professor, published author |
| **Goals** | Translate research to accessible content |
| **Pain Points** | Technical writing, citation management |
| **Technical Proficiency** | High |
| **Use Case** | Create supplementary textbooks from course material |
| **Languages** | English, Spanish |
| **Expected Usage** | 2-3 ebooks per semester |

### Persona 4: Digital Marketer
| Attribute | Description |
|-----------|-------------|
| **Name** | Jake Thompson |
| **Role** | Digital marketing agency owner |
| **Goals** | Client lead magnets, content marketing assets |
| **Pain Points** | Client deadlines, volume requirements |
| **Technical Proficiency** | Medium |
| **Use Case** | Batch generate industry reports for multiple clients |
| **Languages** | English |
| **Expected Usage** | 20+ ebooks per month |

### Persona 5: Admin User
| Attribute | Description |
|-----------|-------------|
| **Name** | Alex Rivera |
| **Role** | System Administrator |
| **Goals** | Monitor system health, manage users, troubleshoot issues |
| **Pain Points** | Lack of visibility into generations |
| **Technical Proficiency** | High |
| **Languages** | English |
| **Expected Usage** | Daily monitoring, monthly reports |

---

# 5. FUNCTIONAL REQUIREMENTS

## 5.1 User-Invocable Skills (9 Skills)

### FR-1: Primary Ebook Generation (`/ebook-generate`)
**Priority**: P0 (Critical) | **Agent Flow**: All 13 Agents

**Description**: Generate single ebook with zero manual interaction

**User Workflow**:
```
Input Topic → Configure Options → Generate → Monitor Progress → Download PDF
```

**Acceptance Criteria**:
- Accept topic sentence (3-500 characters)
- Load or validate configuration JSON
- Execute all 13 agents sequentially/parallel
- Generate PDF with embedded infographics
- Upload to Google Drive (primary) + local folder (optional)
- Return download links and fact verification report
- Display real-time progress (current agent, percentage, ETA)
- Complete generation in 10-15 minutes

---

### FR-2: Batch Ebook Generation (`/ebook-batch`)
**Priority**: P1 (High) | **Agent Flow**: 3 parallel pipelines

**Description**: Generate multiple ebooks simultaneously

**Acceptance Criteria**:
- Accept up to 10 topic sentences
- Run 3 pipelines in parallel (configurable)
- Display progress per pipeline independently
- Aggregate results with summary report
- Complete 3 ebooks in 15-20 minutes
- Complete 10 ebooks in 50-60 minutes

---

### FR-3: Configuration Creation (`/ebook-config-create`)
**Priority**: P0 (Critical) | **Agent Flow**: Agent 1 only

**Description**: Create or update ebook-config.json

**Interactive Prompts**:
1. Language selection (10 options as radio buttons)
2. Chapter structure configuration:
   - Basic Chapters (0-20)
   - One-Level Depth Chapters (0-15)
   - Two-Level Depth Chapters (0-10)
3. Content specifications:
   - Words per chapter (1000-10000)
   - Include exercises (Yes/No)
   - Include case studies (Yes/No)
   - Tone (Professional/Casual/Academic)
   - Infographic style (Modern/Minimalist/Professional/Creative/Technical)
4. Storage options:
   - Google Drive (Yes/No)
   - Local folder path
   - Create local copy (Yes/No)
5. Styling (optional):
   - Font family
   - Heading font
   - Primary/Secondary colors
   - Page size
   - Margins

**Acceptance Criteria**:
- All required fields validated before saving
- Export/import configuration as JSON
- Validation error messages with guidance

---

### FR-4: Template-Based Generation (`/ebook-template`)
**Priority**: P2 (Medium) | **Agent Flow**: All 13 Agents

**Description**: Generate ebook from custom template

**Acceptance Criteria**:
- Accept template file path (JSON format)
- Validate template parameters
- Execute pipeline enforcing template specifications
- Deliver PDF matching template structure

---

### FR-5: Quality Report (`/ebook-quality-report`)
**Priority**: P2 (Medium) | **Agent Flow**: Agents 8, 9

**Description**: Generate comprehensive quality and fact verification report

**Input**: File path (markdown, docx, txt, pdf)

**Agents Involved**:
- Agent 8: Quality Enhancement (analysis mode)
- Agent 9: Critic & Proofreading (full verification)

**Output PDF Report Contains**:
- Readability scores (Flesch Reading Ease, etc.)
- Grammar issues identified
- Fact verification results:
  - Claims verified/corrected/flagged
  - Factual accuracy score (0-100%)
  - Confidence scores per claim
- Improvement suggestions

---

### FR-6: Content Expansion (`/ebook-expand`)
**Priority**: P2 (Medium) | **Agent Flow**: All 13 Agents

**Description**: Expand existing content into full ebook

**Acceptance Criteria**:
- Accept existing content file
- Analyze style, tone, language
- Extract key themes
- Generate additional chapters
- Generate infographics for all chapters
- Run full quality and fact-checking pipeline
- Deliver complete ebook PDF

---

### FR-7: Storage Setup (`/ebook-storage-setup`)
**Priority**: P0 (Critical) | **Agent Flow**: Agent 13

**Description**: Configure storage (Google Drive + Local)

**Google Drive Setup**:
1. Check for existing credentials
2. Guide user through Google Cloud project creation
3. Enable Drive API
4. Create OAuth credentials
5. Test authentication
6. Create base folder structure

**Local Folder Setup**:
1. Prompt for local folder path
2. Test write permissions
3. Create folder structure
4. Update config with local path

---

### FR-8: Statistics Dashboard (`/ebook-stats`)
**Priority**: P1 (High) | **Agent Flow**: Query only

**Description**: Display generation statistics

**Dashboard Metrics**:
- Total ebooks created
- Average generation time
- Most popular topics
- Quality score trends
- Fact accuracy trends
- Storage usage (Google Drive, local)
- Agent performance metrics
- Language distribution

---

### FR-9: Infographic Generation (`/ebook-infographic-only`)
**Priority**: P1 (High) | **Agent Flow**: Agent 6 only

**Description**: Generate infographics for existing chapters

**Acceptance Criteria**:
- Accept folder path with chapter files or single file
- Analyze each chapter's content structure
- Extract key concepts (5-7 per chapter)
- Determine visualization type:
  - Flowchart (processes)
  - Mind map (concepts)
  - Timeline (historical)
  - Comparison table (comparisons)
  - Hierarchy diagram (classifications)
- Generate infographic image using:
  - SDXL Lightning (4-step CPU-optimized)
  - Mermaid.js / Graphviz (diagrams)
  - Matplotlib / Plotly (charts)
- Save as `chapter_[N]_infographic.png`
- Deliver folder with all infographic images

---

## 5.2 Specialized Agents (13 Agents)

### Agent 1: Configuration Loader
**Priority**: P0 | **Timeout**: 30 seconds

**Function**: Load, validate, and parse user configuration

**Input**:
- `ebook-config.json` file path (optional)
- Web UI configuration (if JSON not present)

**Processing**:
- Validate language code (must be in supported list)
- Validate chapter counts:
  - Basic: 0-20
  - One-Level: 0-15
  - Two-Level: 0-10
- Calculate total chapters (must be ≥1)
- Validate storage paths
- Validate styling parameters
- Apply NO defaults (user must specify all required fields)

**Output**: Validated configuration object with applied parameters

---

### Agent 2: Topic Analysis
**Priority**: P0 | **Timeout**: 60 seconds

**Function**: Deep analysis of input topic sentence

**Input**:
- Topic sentence
- Configuration object

**Processing**:
- Identify target audience
- Classify domain/subject area
- Determine complexity level
- Extract key themes and subtopics
- Language-specific analysis

**Tools**: WebSearch, Memory, Configuration

**Output**: Structured topic brief with:
- Audience description
- Domain classification
- Complexity level
- Tone recommendations
- Key themes list

---

### Agent 3: Content Strategy
**Priority**: P0 | **Timeout**: 90 seconds

**Function**: Design comprehensive table of contents

**Input**:
- Topic brief
- Chapter structure configuration

**Processing**:
- Allocate chapters to Basic/One-Level/Two-Level per configuration
- Create chapter-by-chapter outline with depth specifications
- Define content depth for each section
- Establish logical flow and progression
- Set learning objectives per chapter
- Apply language-specific structuring (RTL for Arabic)

**Output**: Detailed outline with:
- Chapter titles
- Depth levels
- Word counts per chapter
- Section hierarchies

---

### Agent 4: Research Swarm (3 Parallel Agents)
**Priority**: P0 | **Timeout**: 180 seconds (3 agents parallel)

**Function**: Parallel research on different aspects

**Input**: Topic brief

**Processing** (all 3 agents run simultaneously):

| Sub-Agent | Focus | Output |
|-----------|-------|--------|
| **Agent A** | Latest trends, statistics, data (2024-2025) | Trend database |
| **Agent B** | Expert sources, case studies, real-world examples | Source database |
| **Agent C** | Competitor analysis, market gaps, unique angles | Market analysis |

**Tools**: WebSearch, Academic databases, Statistical databases

**Output**: Curated research database with:
- Aggregated and deduplicated results
- Proper citations
- Source credibility scores

---

### Agent 5: Chapter Generation Swarm
**Priority**: P0 | **Timeout**: 600 seconds (N parallel agents)

**Function**: Generate all chapters in parallel

**Input**:
- Research database
- Content outline
- Configuration

**Processing** (all chapters generated simultaneously):

| Chapter Type | Structure | Word Count | Parallel Agents |
|--------------|-----------|------------|-----------------|
| **Basic** | Linear flow | 3000-4000 | N agents (one per chapter) |
| **One-Level** | Main + 2-3 subsections | 4000-5000 | N agents (one per chapter) |
| **Two-Level** | Complex nested hierarchies | 5000-7000 | N agents (one per chapter) |

**Content Requirements**:
- Include examples, case studies
- Include practical exercises (if configured)
- Language-specific content generation
- Maintain consistent tone across all chapters

**Tools**: Memory, WebSearch, Configuration

**Output**: Complete chapter drafts with consistent tone

---

### Agent 6: Infographic Generation
**Priority**: P0 | **Timeout**: 300 seconds (N parallel agents)

**Function**: Generate one infographic per chapter (MANDATORY)

**Input**: Chapter content

**Processing** (one agent per chapter, parallel):

1. Analyze chapter structure
2. Extract 5-7 key concepts
3. Determine visualization type:
   - Flowchart (processes)
   - Mind map (concepts)
   - Timeline (historical)
   - Comparison table (comparisons)
   - Hierarchy diagram (classifications)
4. Generate image using:
   - SDXL Lightning (4-step CPU-optimized) for artistic visuals
   - Mermaid.js / Graphviz for structured diagrams
   - Matplotlib / Plotly for data charts
5. Apply styling from configuration
6. Save as high-resolution PNG (150 DPI, 1200px width)

**Output**: High-resolution infographic image file per chapter

**Acceptance Criteria**:
- Every chapter has exactly one infographic
- Image quality meets specifications
- Styling matches configuration

---

### Agent 7: Visual Design
**Priority**: P1 | **Timeout**: 60 seconds

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

### Agent 8: Quality Enhancement
**Priority**: P0 | **Timeout**: 120 seconds

**Function**: Multi-stage content improvement

**Input**: Chapter drafts

**Processing**:
- Grammar correction using LanguageTool (multi-language)
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

### Agent 9: Critic & Proofreading
**Priority**: P0 | **Timeout**: 300 seconds

**Function**: Rigorous fact validation and correction

**Input**: Polished content

**Processing** (7-Pass Verification):

| Pass | Function |
|------|----------|
| **Pass 1** | Identify all factual claims |
| **Pass 2** | Verify each claim against trusted sources |
| **Pass 3** | Cross-reference claims within document |
| **Pass 4** | Check for logical contradictions |
| **Pass 5** | Validate statistics and data |
| **Pass 6** | Assess source credibility |
| **Pass 7** | Language-specific accuracy checks |

**Verification Scope**:
- Statistics & numerical data
- Dates & timelines
- Quotes & citations
- Scientific claims
- Technical statements
- Geographical information
- Names & titles
- Cultural context

**Correction Strategy**:
- High Confidence Errors (>90%): Auto-correct immediately
- Medium Confidence (70-90%): Flag for review with alternatives
- Low Confidence (<70%): Highlight for review
- Unverifiable Claims: Remove or qualify with uncertainty language

**Tools**: WebSearch, Academic databases, Statistical databases, News archives

**Output**: Fact-corrected content + verification report with confidence scores

**Quality Gate**: Minimum 95% factual accuracy required

---

### Agent 10: SEO and Metadata
**Priority**: P1 | **Timeout**: 60 seconds

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

### Agent 11: Layout and Formatting
**Priority**: P0 | **Timeout**: 120 seconds

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

### Agent 12: PDF Generation
**Priority**: P0 | **Timeout**: 120 seconds

**Function**: Convert to professional PDF

**Input**: Formatted document

**Processing**:
- Convert to PDF using WeasyPrint/ReportLab
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

### Agent 13: Storage Integration
**Priority**: P0 | **Timeout**: 60 seconds

**Function**: Dual storage system (Google Drive + Local)

**Input**: PDF file, metadata, infographics

**Processing**:

**Google Drive Storage** (Default):
- Authenticate with Google Drive API
- Create folder structure:
  - Main: "Auto-Generated Ebooks"
  - Subfolder: [Topic Name]
  - Files: PDF, Infographics folder, Metadata, Reports
- Upload with proper naming
- Generate shareable link
- Log all uploads

**Local Storage** (Optional):
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

## 5.3 Enhanced Features (8 Gaps)

### FR-23: Email Notifications
**Priority**: P2

**Acceptance Criteria**:
- Send email when generation completes
- Send email when generation fails
- User preferences for notifications
- Daily summary option
- Weekly quality report option

---

### FR-24: Rate Limiting
**Priority**: P2

**Acceptance Criteria**:
- 5 generations per hour per user
- Higher limits for admin (100/hour)
- Display usage limits in UI
- Alert when limit approached
- Queue option when limit exceeded

---

### FR-25: Automated Backups
**Priority**: P1

**Acceptance Criteria**:
- Daily PostgreSQL backup at 2 AM
- Upload backups to MinIO
- MinIO versioning enabled
- Admin UI for backup management
- Retain 7 daily backups

---

### FR-26: Version Control for Regenerations
**Priority**: P2

**Acceptance Criteria**:
- Auto-increment version number on regeneration
- Link versions to parent generation
- UI to view all versions of same topic
- Compare versions feature
- "Generate Version 3" button

---

### FR-27: Cost Monitoring & Budgets
**Priority**: P2

**Acceptance Criteria**:
- Monthly budget per user
- Real-time cost tracking
- Alert at configurable threshold (default: 80%)
- Cost breakdown by provider
- Projected month-end cost
- Budget adjustment UI

---

### FR-28: Advanced Search & Filtering
**Priority**: P1

**Acceptance Criteria**:
- Full-text search across topics and content
- Multiple filters (status, language, date, quality scores, counts)
- Sort options (date, relevance, quality)
- Export results (CSV, JSON, PDF)

---

### FR-29: Collaborative Features
**Priority**: P2

**Acceptance Criteria**:
- Share ebooks via email or link
- Permission levels (View, View & Comment, Edit)
- Expiry options (Never, 7 days, 30 days, Custom)
- Comments per chapter
- Active shares management (revoke)

---

### FR-30: Template Library
**Priority**: P2

**Acceptance Criteria**:
- Public templates for common genres
- Template preview
- Save to user's library
- Create custom template
- Usage tracking
- Categories for filtering

---

# 6. TECHNICAL ARCHITECTURE

## 6.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Web Browser (React + TypeScript)                                        │
│  - Generate Ebook Page                                                   │
│  - Batch Generate Page                                                   │
│  - Configuration Manager                                                 │
│  - Ebook History                                                         │
│  - Admin Dashboard                                                       │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ HTTPS/WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  FastAPI                                                                 │
│  - Authentication (JWT)                                                 │
│  - Rate Limiting                                                         │
│  - Request Routing                                                       │
│  - Response Caching                                                      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  AGENT LAYER │    │ TASK QUEUE   │    │  DATA LAYER  │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ Agent 1-13   │    │  Celery +    │    │ PostgreSQL   │
│ Parallel     │    │  Redis       │    │ MinIO        │
│ Execution    │    │              │    │ Redis        │
└──────────────┘    └──────────────┘    └──────────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
              ┌─────────┐      ┌──────────┐
              │ Ollama  │      │External  │
              │ LLMs    │      │ APIs     │
              └─────────┘      └──────────┘
```

## 6.2 Technology Stack

### 6.2.1 Frontend

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| Framework | React | 18+ | Component-based, large ecosystem |
| Language | TypeScript | 5.3+ | Type safety, better DX |
| Styling | Tailwind CSS | 3.4+ | Utility-first, fast development |
| State Management | Zustand / React Query | Latest | Predictable state updates |
| Routing | React Router | 6.21+ | Declarative routing |
| HTTP Client | Axios | 1.6+ | Promise-based, interceptors |
| Real-time | Socket.IO Client | 4.5+ | WebSocket support |
| Build Tool | Vite | 5.0+ | Fast HMR, optimized builds |
| Testing | Jest + React Testing Library | Latest | Component testing |

### 6.2.2 Backend

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| Framework | FastAPI | 0.109+ | Async, type hints, auto-docs |
| Language | Python | 3.11+ | AI/ML ecosystem |
| Task Queue | Celery | 5.3+ | Distributed processing |
| Cache/Broker | Redis | 7+ | Fast, in-memory |
| Authentication | JWT + python-jose | Latest | Industry standard |
| API Docs | OpenAPI/Swagger | Built-in | Auto-generated |

### 6.2.3 AI/ML Models (CPU-Based)

**Text Generation**:
| Technology | Models | Purpose |
|------------|--------|---------|
| Ollama (local) | Llama 3.1 8B, Mistral 7B, Qwen2.5 7B, Gemma 2 9B | Primary LLM (free) |
| OpenAI API | GPT-4o | Fallback (paid) |
| Anthropic API | Claude 3.5 Sonnet | Fallback (paid) |

**Infographic Generation**:
| Technology | Purpose |
|------------|---------|
| Stable Diffusion XL Lightning | Artistic visuals (4-step) |
| Mermaid.js | Structured diagrams |
| Graphviz | Graph diagrams |
| Matplotlib | Scientific charts |
| Plotly | Interactive charts |
| DALL-E 3 | Fallback (paid) |

**Grammar & Quality**:
| Technology | Purpose |
|------------|---------|
| LanguageTool | Multi-language grammar |
| Textstat | Readability metrics |

### 6.2.4 Data Storage

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Primary DB | PostgreSQL | 15+ | User data, generations |
| Cache | Redis | 7+ | Sessions, rate limiting |
| Object Storage | MinIO | Latest | S3-compatible storage |
| External Storage | Google Drive API | v3 | User-facing storage |

### 6.2.5 PDF Generation

| Component | Technology | Purpose |
|-----------|------------|---------|
| Library | WeasyPrint | HTML/CSS to PDF |
| Fallback | ReportLab | Programmatic PDF |
| Templates | Jinja2 | Flexible templating |

### 6.2.6 Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| Containerization | Docker | Consistency |
| Orchestration | Docker Compose | Development deployment |
| Reverse Proxy | Nginx | Load balancing, SSL |
| Monitoring | Prometheus + Grafana | Metrics, alerts |

## 6.3 Component Responsibilities

### Frontend (React)
- User interface for all 6 pages
- Real-time status updates via WebSocket
- Form validation and submission
- PDF viewing and download
- Admin dashboard with monitoring

### Backend API (FastAPI)
- RESTful API endpoints
- Authentication & authorization
- Request validation
- Agent orchestration
- Celery task management
- Database operations

### Celery Worker
- Execute long-running generation tasks
- Parallel agent execution
- Progress updates to Redis
- Error handling and retry logic

### PostgreSQL
- User data
- Generation records
- Fact verification logs
- Agent execution logs
- API usage tracking
- Infographic metadata

### Redis
- Celery task queue
- Real-time progress cache
- Session storage
- Rate limiting

### MinIO
- PDF file storage
- Infographic image storage
- Metadata files
- Backup storage

### Ollama
- LLM model serving (Llama, Mistral, Qwen, Gemma)
- CPU-optimized inference
- Model caching

---

# 7. AGENT ORCHESTRATION STRATEGY

## 7.1 Sequential vs Parallel Execution

### Sequential Agents (must complete in order):

```
[1] Configuration Loader
    ↓
[2] Topic Analysis
    ↓
[3] Content Strategy
    ↓
[10] SEO & Metadata (after content ready)
    ↓
[11] Layout & Formatting
    ↓
[12] PDF Generation
    ↓
[13] Storage Integration
```

### Parallel Agents (can run simultaneously):

```
[4] Research Swarm ──┬─→ Agent A: Trends & Stats
    ├───→ Agent B: Sources & Examples
    └───→ Agent C: Market Analysis

[5] Chapter Generation ──┬─→ Basic Chapter Agent 1
    ├───→ Basic Chapter Agent 2
    ├───→ ... (all chapters parallel)
    └───→ Two-Level Chapter Agent N

[6] Infographic Generation ──┬─→ Chapter 1 Infographic
    ├───→ Chapter 2 Infographic
    └───→ Chapter N Infographic

[7] Visual Design (parallel with Quality Enhancement)

[8] Quality Enhancement + [9] Critic & Proofreading (parallel execution)
```

## 7.2 Complete Execution Flow

```
User Input (Topic + Config)
    ↓
╔═══════════════════════════════════════════════════════════════╗
║                    SEQUENTIAL PHASE 1                          ║
╠═══════════════════════════════════════════════════════════════╣
║ [1] Configuration Loader (30s)                                 ║
║     ↓                                                          ║
║ [2] Topic Analysis (60s)                                       ║
║     ↓                                                          ║
║ [3] Content Strategy (90s)                                     ║
╚═══════════════════════════════════════════════════════════════╝
    ↓
╔═══════════════════════════════════════════════════════════════╗
║                    PARALLEL PHASE 1                            ║
╠═══════════════════════════════════════════════════════════════╣
║ [4] Research Swarm (180s)                                     ║
║     ├─→ Agent A: Trends & Stats                               ║
║     ├─→ Agent B: Sources & Examples                           ║
║     └─→ Agent C: Market Analysis                              ║
║     ↓ (Aggregate Results)                                      ║
╚═══════════════════════════════════════════════════════════════╝
    ↓
╔═══════════════════════════════════════════════════════════════╗
║                    PARALLEL PHASE 2                            ║
╠═══════════════════════════════════════════════════════════════╣
║ [5] Chapter Generation (300-600s)                             ║
║     ├─→ Basic Chapter Agent 1                                 ║
║     ├─→ Basic Chapter Agent 2                                 ║
║     ├─→ One-Level Chapter Agent 1                             ║
║     ├─→ ... (all chapters parallel)                           ║
║     └─→ Two-Level Chapter Agent N                             ║
║     ↓ (All Chapters Complete)                                  ║
╚═══════════════════════════════════════════════════════════════╝
    ↓
╔═══════════════════════════════════════════════════════════════╗
║                    PARALLEL PHASE 3                            ║
╠═══════════════════════════════════════════════════════════════╣
║ [6] Infographic Generation (180-300s)                         ║
║     ├─→ Chapter 1 Infographic                                 ║
║     ├─→ Chapter 2 Infographic                                 ║
║     ├─→ ... (one per chapter, parallel)                       ║
║     └─→ Chapter N Infographic                                 ║
║     ↓ (All Infographics Complete)                              ║
╚═══════════════════════════════════════════════════════════════╝
    ↓
╔═══════════════════════════════════════════════════════════════╗
║                    PARALLEL PHASE 4                            ║
╠═══════════════════════════════════════════════════════════════╣
║ [7] Visual Design (60s) ┐                                     ║
║                        ├──> [Both Parallel]                   ║
║ [8] Quality Enhancement (120s) ┘                              ║
║     ↓                                                          ║
║ [9] Critic & Proofreading (300s) - Multi-pass verification    ║
╚═══════════════════════════════════════════════════════════════╝
    ↓
╔═══════════════════════════════════════════════════════════════╗
║                    SEQUENTIAL PHASE 2                          ║
╠═══════════════════════════════════════════════════════════════╣
║ [10] SEO & Metadata (60s)                                     ║
║     ↓                                                          ║
║ [11] Layout & Formatting (120s)                               ║
║     ↓                                                          ║
║ [12] PDF Generation (120s)                                    ║
║     ↓                                                          ║
║ [13] Storage Integration (60s)                                ║
╚═══════════════════════════════════════════════════════════════╝
    ↓
Output: PDF + Links + Reports
Total Time: 10-15 minutes
```

## 7.3 Error Handling Strategy

### Per-Agent Error Handling:

| Error Type | Strategy |
|------------|----------|
| Timeout | Retry 3x with exponential backoff (1s, 2s, 4s) |
| Model Failure | Fallback to alternative model (Ollama → OpenAI) |
| API Rate Limit | Queue request, retry after delay |
| Network Error | Retry 3x, then mark failed |

### Pipeline-Level Error Handling:

| Scenario | Action |
|----------|--------|
| Critical Agent Failure | Rollback partial results, notify user |
| Non-Critical Agent Failure | Continue with degraded output, log warning |
| Complete Pipeline Failure | Save error log, offer retry option |
| Partial Success | Save partial results, allow resume |

### Graceful Degradation:

| Component | Fallback |
|-----------|----------|
| Infographic Generation | Continue with text-only PDF |
| External Research | Use cached/available sources |
| Google Drive Upload | Save to MinIO/local only |
| Grammar Check | Continue without grammar correction |

---

# 8. SYSTEM SPECIFICATIONS

## 8.1 Agent Specifications

| Agent | Name | Timeout | Input | Output | Parallel |
|-------|------|---------|-------|--------|----------|
| 1 | Configuration Loader | 30s | Config file | Validated config | No |
| 2 | Topic Analysis | 60s | Topic, config | Topic brief | No |
| 3 | Content Strategy | 90s | Topic brief | Chapter outline | No |
| 4 | Research Swarm | 180s | Outline | Research database | Yes (3) |
| 5 | Chapter Generation | 600s | Research | All chapters | Yes (N) |
| 6 | Infographic Generation | 300s | Chapters | Images | Yes (N) |
| 7 | Visual Design | 60s | All content | Design system | Yes (with 8) |
| 8 | Quality Enhancement | 120s | Content | Polished content | Yes (with 7) |
| 9 | Critic & Proofreading | 300s | Content | Fact-corrected content | No (multi-pass) |
| 10 | SEO & Metadata | 60s | Content | Marketing package | No |
| 11 | Layout & Formatting | 120s | Content | Formatted doc | No |
| 12 | PDF Generation | 120s | Formatted doc | PDF file | No |
| 13 | Storage Integration | 60s | PDF, files | Storage links | No |

## 8.2 Skill Specifications

| Skill | Purpose | Input | Output | Duration | Agent Flow |
|-------|---------|-------|--------|----------|------------|
| `/ebook-generate` | Single ebook | Topic, config | PDF, links | 10-15 min | All 13 |
| `/ebook-batch` | Multiple ebooks | Up to 10 topics | Multiple PDFs | 15-60 min | 3 parallel pipelines |
| `/ebook-config-create` | Create config | Interactive | Config file | 2-3 min | Agent 1 |
| `/ebook-template` | Template-based | Topic, template | PDF | 10-15 min | All 13 |
| `/ebook-quality-report` | Analyze content | File path | Report PDF | 2-3 min | Agents 8, 9 |
| `/ebook-expand` | Expand content | Existing file | Full PDF | 10-15 min | All 13 |
| `/ebook-storage-setup` | Configure storage | Interactive | Setup complete | 5 min | Agent 13 |
| `/ebook-stats` | Display statistics | N/A | Dashboard | <1s | Query only |
| `/ebook-infographic-only` | Generate infographics | Chapter files | Images | 2-3 min | Agent 6 |

## 8.3 Hardware Requirements

### Minimum Requirements (Development)

| Resource | Specification |
|----------|---------------|
| CPU | 4 cores, 2.0 GHz |
| RAM | 16 GB |
| Storage | 50 GB SSD |
| OS | Windows 10/11, macOS 12+, or Linux (Ubuntu 22.04+) |
| Docker | 20.10+ |

### Recommended Requirements (Production)

| Resource | Specification |
|----------|---------------|
| CPU | 8+ cores, 3.0 GHz |
| RAM | 32 GB |
| Storage | 200 GB SSD |
| OS | Linux (Ubuntu 22.04 LTS) |
| Docker | 24.0+ |
| Network | Stable internet connection |

---

# 9. USER INTERFACE REQUIREMENTS

## 9.1 Design Principles

1. **Simplicity First**: Minimal input required for maximum output
2. **Progressive Disclosure**: Advanced options hidden by default
3. **Real-time Feedback**: Progress visible throughout generation
4. **Clear Validation**: Immediate feedback on invalid inputs
5. **Responsive Design**: Works on desktop, tablet, mobile

## 9.2 Page Structure

### Page 1: Generate Ebook (/generate)

**Required Sections**:

1. **Topic Input** (Required)
   - Large text input (minimum 3 words, maximum 500 characters)
   - Character counter
   - Example topics for inspiration

2. **Language Selection** (Required)
   - Radio buttons for 10 supported languages
   - Validation: Must select one language

3. **Chapter Structure** (Required)
   - Number inputs + sliders for:
     * Basic Chapters (0-20)
     * One-Level Depth Chapters (0-15)
     * Two-Level Depth Chapters (0-10)
   - Real-time total calculation
   - Validation: Minimum 1 chapter required

4. **Content Specifications** (Required)
   - Words Per Chapter (1000-10000)
   - Include Exercises: Yes/No
   - Include Case Studies: Yes/No
   - Tone: Professional/Casual/Academic
   - Infographic Style: Modern/Minimalist/Professional/Creative/Technical

5. **Storage Options** (Required)
   - Primary Storage: Google Drive / Local Folder
   - Local Folder Path (conditional)
   - Also Create Local Copy: Yes/No

6. **Styling** (Optional)
   - Checkbox: Use Professional Defaults
   - If unchecked, show advanced options

7. **Generate Button**
   - Shows estimated time
   - Shows total chapters
   - Shows estimated word count

8. **Real-Time Progress** (During Generation)
   - Overall progress bar (0-100%)
   - Current agent display (1-13)
   - Estimated time remaining
   - Agent status list with indicators
   - Live log output
   - Cancel button

### Page 2: Batch Generate (/batch)

- Multiple topic inputs (up to 10)
- Configuration sharing or individual customization
- Parallel execution setting
- Per-pipeline progress tracking

### Page 3: Configuration Manager (/config)

- Saved configurations list
- Create, edit, delete actions
- Import/export functionality

### Page 4: Ebook History (/history)

- Generations list with details
- Filtering and searching
- Actions per generation

### Page 5: Ebook Details (/ebook/:id)

**Tabs**:
- Overview (configuration and statistics)
- Agents (all 13 agents detailed)
- Quality Metrics
- Fact Verification
- Infographics
- Metadata
- Logs

### Page 6: Admin Dashboard (/admin)

**Tabs**:
1. **Overview**: System statistics
2. **All Generations**: Table with all generations, GDrive links
3. **System Monitoring**: CPU, memory, Docker, Celery
4. **Configuration**: View/edit app-config.json
5. **Users**: User management

---

# 10. API SPECIFICATIONS

## 10.1 Authentication API

### POST /api/auth/login
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

## 10.2 Generation API

### POST /api/generation/start
**Description**: Start a new ebook generation

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

### GET /api/generation/:id/status
**Description**: Get real-time status of a generation

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
  "agent_status": [
    {
      "agent_number": 1,
      "agent_name": "Configuration Loader",
      "status": "completed",
      "execution_time_seconds": 18
    }
  ]
}
```

## 10.3 Admin API

### GET /api/admin/stats
**Description**: Get system statistics (admin only)

**Response** (200 OK):
```json
{
  "overview": {
    "total_generations": 1247,
    "generations_today": 23,
    "success_rate": 98.7,
    "average_generation_time_seconds": 765
  },
  "storage": {
    "google_drive_used_gb": 2.3,
    "minio_used_gb": 1.8
  },
  "active": {
    "active_generations": 3,
    "queued_tasks": 7
  }
}
```

## 10.4 WebSocket Events

### Event: generation_progress
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

### Event: generation_complete
**Description**: Generation completed successfully

**Payload**:
```json
{
  "generation_id": 123,
  "status": "completed",
  "output": {
    "pdf_link": "https://minio.example.com/ebooks/ai_healthcare_v1.0.pdf",
    "gdrive_link": "https://drive.google.com/file/d/abc123/view"
  },
  "quality_metrics": {
    "readability_score": 72,
    "fact_accuracy_score": 96
  }
}
```

---

# 11. DATABASE SCHEMA

## 11.1 Core Tables

### users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP NULLABLE
);
```

### ebook_generations
```sql
CREATE TABLE ebook_generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic_sentence TEXT NOT NULL,
    config_json JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    current_agent VARCHAR(50) NULLABLE,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP NULLABLE,
    pdf_path TEXT NULLABLE,
    pdf_minio_path TEXT NULLABLE,
    gdrive_link TEXT NULLABLE,
    local_path TEXT NULLABLE,
    total_chapters INTEGER NULLABLE,
    total_words INTEGER NULLABLE,
    total_infographics INTEGER NULLABLE,
    generation_time_seconds INTEGER NULLABLE,
    readability_score FLOAT NULLABLE,
    grammar_score FLOAT NULLABLE,
    fact_accuracy_score FLOAT NULLABLE,
    error_message TEXT NULLABLE,
    retry_count INTEGER DEFAULT 0,
    version_number INTEGER DEFAULT 1,
    parent_generation_id INTEGER REFERENCES ebook_generations(id)
);
```

### fact_verifications
```sql
CREATE TABLE fact_verifications (
    id SERIAL PRIMARY KEY,
    generation_id INTEGER REFERENCES ebook_generations(id) ON DELETE CASCADE,
    claim_text TEXT NOT NULL,
    verified BOOLEAN NOT NULL,
    confidence_score FLOAT NOT NULL,
    correction_before TEXT NULLABLE,
    correction_after TEXT NULLABLE,
    verification_source TEXT NULLABLE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### agent_logs
```sql
CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    generation_id INTEGER REFERENCES ebook_generations(id) ON DELETE CASCADE,
    agent_name VARCHAR(50) NOT NULL,
    agent_number INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    input_data JSONB NULLABLE,
    output_data JSONB NULLABLE,
    execution_time_seconds FLOAT NULLABLE,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP NULLABLE,
    error_message TEXT NULLABLE
);
```

### infographics
```sql
CREATE TABLE infographics (
    id SERIAL PRIMARY KEY,
    generation_id INTEGER REFERENCES ebook_generations(id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    image_path TEXT NULLABLE,
    minio_path TEXT NULLABLE,
    visualization_type VARCHAR(50) NULLABLE,
    generation_method VARCHAR(50) NULLABLE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 11.2 JSON Configuration Schema

```json
{
    "type": "object",
    "required": ["language", "chapter_structure", "content_specs"],
    "properties": {
        "language": {
            "type": "string",
            "enum": ["en", "es", "fr", "de", "zh", "ja", "pt", "it", "ru", "ar"]
        },
        "chapter_structure": {
            "type": "object",
            "properties": {
                "basic_chapters": {"type": "integer", "minimum": 0, "maximum": 20},
                "one_level_depth_chapters": {"type": "integer", "minimum": 0, "maximum": 15},
                "two_level_depth_chapters": {"type": "integer", "minimum": 0, "maximum": 10}
            }
        },
        "storage_options": {
            "type": "object",
            "properties": {
                "google_drive": {"type": "boolean"},
                "local_folder": {"type": "string"},
                "create_local_copy": {"type": "boolean"}
            }
        },
        "styling": {
            "type": "object",
            "properties": {
                "font_family": {"type": "string"},
                "heading_font": {"type": "string"},
                "primary_color": {"type": "string"},
                "secondary_color": {"type": "string"},
                "page_size": {"type": "string"},
                "margins": {"type": "string"}
            }
        },
        "content_specs": {
            "type": "object",
            "properties": {
                "words_per_chapter": {"type": "integer", "minimum": 1000, "maximum": 10000},
                "include_exercises": {"type": "boolean"},
                "include_case_studies": {"type": "boolean"},
                "infographic_style": {"type": "string", "enum": ["modern", "minimalist", "professional", "creative", "technical"]},
                "tone": {"type": "string", "enum": ["professional", "casual", "academic"]}
            }
        }
    }
}
```

---

# 12. NON-FUNCTIONAL REQUIREMENTS

## 12.1 Performance Requirements

| Requirement | Specification | Priority |
|-------------|----------------|----------|
| **NFR-P-001** | Single ebook generation <=15 minutes | Critical |
| **NFR-P-002** | Topic analysis <=30 seconds | Critical |
| **NFR-P-003** | Research swarm <=2 minutes | Critical |
| **NFR-P-004** | Chapter generation <=5 minutes | Critical |
| **NFR-P-005** | Infographic generation <=3 minutes | Critical |
| **NFR-P-006** | PDF generation <=1 minute | Critical |
| **NFR-P-007** | Web page load time <=2 seconds | High |
| **NFR-P-008** | API response time <=500ms | High |
| **NFR-P-009** | Support 50 concurrent generations | Medium |
| **NFR-P-010** | Batch generation (3 ebooks) <=20 minutes | High |

## 12.2 Scalability Requirements

| Requirement | Specification | Priority |
|-------------|----------------|----------|
| **NFR-S-001** | Support 10,000 user accounts | High |
| **NFR-S-002** | Support 100,000 ebook generations/month | High |
| **NFR-S-003** | Horizontal scaling for web servers | High |
| **NFR-S-004** | Vertical scaling for AI processing | Medium |

## 12.3 Availability Requirements

| Requirement | Specification | Priority |
|-------------|----------------|----------|
| **NFR-A-001** | 99.5% uptime | Critical |
| **NFR-A-002** | Maximum 3.65 hours downtime/month | Critical |
| **NFR-A-003** | Graceful degradation during high load | High |
| **NFR-A-004** | Automated failover for critical services | High |
| **NFR-A-005** | Data backup daily with 30-day retention | Critical |

## 12.4 Security Requirements

| Requirement | Specification | Priority |
|-------------|----------------|----------|
| **NFR-SEC-001** | HTTPS only for all communications | Critical |
| **NFR-SEC-002** | User authentication with JWT | Critical |
| **NFR-SEC-003** | Role-based access control (user/admin) | Critical |
| **NFR-SEC-004** | Encrypted data at rest | Critical |
| **NFR-SEC-005** | API rate limiting (5/hour for users) | High |
| **NFR-SEC-006** | Input sanitization to prevent injection | Critical |
| **NFR-SEC-007** | GDPR compliance for EU users | Critical |

---

# 13. IMPLEMENTATION ROADMAP

## Phase 1: Core Pipeline with Zero Interaction (Weeks 1-8)

**Goal**: Working system that generates ebooks from topic sentence

**Sprint 1-2: Foundation**
- Project setup (Docker, database, base infrastructure)
- Authentication system
- Basic UI framework
- Configuration management

**Sprint 3-4: Agent Pipeline**
- Agent 1: Configuration Loader
- Agent 2: Topic Analysis
- Agent 3: Content Strategy
- Agent 4: Research Swarm
- Agent orchestration framework

**Sprint 5-6: Content Generation**
- Agent 5: Chapter Generation
- Agent 8: Quality Enhancement
- Agent 9: Critic & Proofreading
- Agent 10: SEO & Metadata

**Sprint 7-8: Output & Storage**
- Agent 11: Layout & Formatting
- Agent 12: PDF Generation
- Agent 13: Storage Integration
- End-to-end pipeline testing

**Deliverables**:
- Working zero-interaction ebook generation
- Web UI for single generation
- Google Drive integration
- Basic configuration management

## Phase 2: Infographic Generation & Web UI (Weeks 9-12)

**Goal**: Every chapter starts with professional infographic

**Sprint 9-10: Image Generation**
- Agent 6: Infographic Generation
- SDXL Lightning / Mermaid integration
- Image embedding in PDF

**Sprint 11-12: Visual Enhancement**
- Agent 7: Visual Design
- Styling application
- UI enhancements

**Deliverables**:
- One infographic per chapter
- Multiple visualization types
- Styling from configuration

## Phase 3: Scale & Multi-Language (Weeks 13-16)

**Sprint 13-14: Batch Processing**
- Skill 2: `/ebook-batch`
- Parallel pipeline execution
- Queue management

**Sprint 15-16: Multi-Language**
- Language-specific generation
- LanguageTool integration
- RTL support (Arabic)

**Deliverables**:
- Batch generation (3 parallel)
- 10 language support

## Phase 4: Advanced Features (Weeks 17-20)

**Sprint 17-18: Enhanced Features**
- Template library
- Advanced search
- Version control
- Email notifications

**Sprint 19-20: Production Readiness**
- Rate limiting
- Automated backups
- Cost monitoring
- Admin dashboard

## Phase 5: Production Hardening (Weeks 21-22)

- Security audit
- Load testing
- Documentation
- Deployment

---

# 14. SUCCESS METRICS & KPIS

## 14.1 Product Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| User registration rate | 1000 users in first 3 months | Signups / time |
| Generation completion rate | >98% | Completed / Started |
| Average generation time | <15 minutes | Duration tracking |
| User satisfaction (NPS) | >50 | Post-generation survey |
| Return user rate | >40% | Users with 2+ generations |

## 14.2 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Factual accuracy | >95% | Agent 9 verification |
| Readability score | >60 | Flesch Reading Ease |
| Grammar accuracy | 100% | Agent 8 verification |
| PDF generation success | 100% | File validity checks |
| Infographic generation | 100% (1 per chapter) | Count verification |

## 14.3 Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| System uptime | >99.5% | Monitoring |
| API response time (p95) | <500ms | APM |
| Database query time (p95) | <100ms | Database monitoring |
| Error rate | <2% | Error tracking |
| Queue processing time | <5 minutes | Celery monitoring |

---

# 15. RISK ASSESSMENT

## 15.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM API rate limits | Medium | High | Local models as fallback |
| PDF generation failures | Low | High | Comprehensive error handling |
| Database performance | Low | Medium | Query optimization, indexing |
| Google Drive API changes | Low | Medium | Version pinning, monitoring |
| Image generation cost | Medium | Medium | Usage limits, local models |

## 15.2 Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scaling challenges | Medium | High | Horizontal architecture |
| Data loss | Low | Critical | Daily backups, replication |
| Security breach | Low | Critical | Security audits |
| Service downtime | Medium | High | Redundancy, failover |

## 15.3 Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| User adoption lower than expected | Medium | High | Free tier, marketing |
| Competing products | High | Medium | Differentiation |
| Content quality concerns | Medium | High | Fact validation |
| Regulatory changes | Low | Medium | Legal review |

---

# 16. RESOURCE REQUIREMENTS

## 16.1 Team Structure

| Role | FTE | Responsibilities |
|------|-----|------------------|
| Product Manager | 1 | Requirements, roadmap |
| Tech Lead | 1 | Architecture, decisions |
| Backend Developer | 2-3 | API, agents, database |
| Frontend Developer | 1-2 | UI/UX implementation |
| AI/ML Engineer | 1 | Agent development |
| DevOps Engineer | 1 | Infrastructure, deployment |
| QA Engineer | 1 | Testing strategy |
| UX Designer | 0.5 | UI/UX design |

## 16.2 Infrastructure Requirements

### Production Environment

| Resource | Quantity | Specification |
|----------|----------|---------------|
| Application servers | 2+ | 8 CPU, 32GB RAM |
| Database server | 1 + 1 replica | 16 CPU, 64GB RAM, 500GB SSD |
| Redis cache | 1 | 8 CPU, 16GB RAM |
| Object storage | 1 | MinIO, 1TB+ |
| Load balancer | 1 | Nginx/HAProxy |

---

# 17. APPENDICES

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Basic Chapter** | Single-level content with linear flow, 3000-4000 words |
| **One-Level Chapter** | Content with 2-3 subsections, 4000-5000 words |
| **Two-Level Chapter** | Content with complex nested hierarchies, 5000-7000 words |
| **Agent** | Specialized AI module performing specific task in pipeline |
| **Skill** | User-invocable command triggering one or more agents |
| **Swarm** | Multiple agents working in parallel on same task |
| **Configuration** | JSON file specifying generation parameters |
| **Template** | Reusable configuration for common use cases |
| **Fact Verification** | 7-pass process validating factual claims |
| **RTL** | Right-to-left text direction (Arabic) |

## Appendix B: Supported Languages

| Code | Language | Grammar Support | RTL |
|------|----------|-----------------|-----|
| en | English | Yes | No |
| es | Spanish | Yes | No |
| fr | French | Yes | No |
| de | German | Yes | No |
| zh | Chinese | Yes | No |
| ja | Japanese | Yes | No |
| pt | Portuguese | Yes | No |
| it | Italian | Yes | No |
| ru | Russian | Yes | No |
| ar | Arabic | Yes | Yes |

## Appendix C: Error Codes

| Code | Description | User Action |
|------|-------------|-------------|
| E001 | Invalid configuration | Check configuration parameters |
| E002 | Topic too short | Provide longer topic (3+ words) |
| E003 | No chapters specified | Set at least one chapter type > 0 |
| E004 | Language not supported | Choose from supported languages |
| E005 | Generation timeout | Try again or contact support |
| E006 | PDF generation failed | Check configuration, try again |
| E007 | Storage upload failed | Check credentials, try again |
| E008 | Rate limit exceeded | Wait before next generation |
| E009 | Authentication failed | Check login credentials |
| E010 | Resource unavailable | Try again later |

## Appendix D: API Endpoints Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/refresh` | Refresh token |

### Generations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generations` | Start new generation |
| GET | `/api/generations` | List user generations |
| GET | `/api/generations/{id}` | Get generation details |
| GET | `/api/generations/{id}/status` | Get generation status |
| DELETE | `/api/generations/{id}` | Delete generation |
| POST | `/api/generations/{id}/cancel` | Cancel in-progress generation |
| GET | `/api/generations/{id}/download` | Download PDF |
| POST | `/api/generations/batch` | Start batch generation |

### Configurations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/configurations` | List user configurations |
| POST | `/api/configurations` | Create configuration |
| GET | `/api/configurations/{id}` | Get configuration details |
| PUT | `/api/configurations/{id}` | Update configuration |
| DELETE | `/api/configurations/{id}` | Delete configuration |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/stats` | System statistics |
| GET | `/api/admin/generations` | All generations |
| GET | `/api/admin/users` | User list |
| GET | `/api/admin/monitoring` | System monitoring data |

---

**END OF PRODUCT REQUIREMENTS DOCUMENT**

*This document is the source of truth for the Automated PDF Ebook Creation System project. All development decisions should reference this PRD to ensure alignment with product requirements.*
