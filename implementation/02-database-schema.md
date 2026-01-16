# Database Schema (PostgreSQL)

## Core Entities

### users
- `id`: SERIAL PRIMARY KEY
- `username`: VARCHAR(50) UNIQUE
- `password_hash`: VARCHAR(255)
- `email`: VARCHAR(100) UNIQUE
- `role`: VARCHAR(20) (admin, user)
- `created_at`: TIMESTAMP

### ebook_generations
- `id`: SERIAL PRIMARY KEY
- `user_id`: INT (FK)
- `topic_sentence`: TEXT
- `config_json`: JSONB
- `status`: VARCHAR(20) (pending, processing, completed, failed)
- `progress`: INT (0-100)
- `current_agent`: VARCHAR(50)
- `pdf_link`: TEXT
- `gdrive_link`: TEXT
- `fact_accuracy_score`: FLOAT
- `readability_score`: FLOAT
- `started_at`: TIMESTAMP
- `completed_at`: TIMESTAMP

### fact_verifications
- `id`: SERIAL PRIMARY KEY
- `generation_id`: INT (FK)
- `claim_text`: TEXT
- `verified`: BOOLEAN
- `confidence_score`: FLOAT
- `source`: TEXT

### agent_logs
- `id`: SERIAL PRIMARY KEY
- `generation_id`: INT (FK)
- `agent_name`: VARCHAR(50)
- `status`: VARCHAR(20)
- `execution_time`: FLOAT
- `error_message`: TEXT

### chapters
- `id`: SERIAL PRIMARY KEY
- `generation_id`: INT (FK)
- `chapter_number`: INT
- `title`: VARCHAR(255)
- `depth_level`: INT (0, 1, 2)
- `content_markdown`: TEXT
- `word_count`: INT
- `status`: VARCHAR(20) (drafting, refined, verified)
- `infographic_id`: INT (FK to infographics table)
- `created_at`: TIMESTAMP

### infographics
- `id`: SERIAL PRIMARY KEY
- `generation_id`: INT (FK)
- `chapter_id`: INT (FK to chapters table)
- `chapter_number`: INT
- `minio_path`: TEXT
- `image_type`: VARCHAR(50) (chart, diagram, artistic)
- `metadata`: JSONB (Visual concepts, prompt used)
- `created_at`: TIMESTAMP
