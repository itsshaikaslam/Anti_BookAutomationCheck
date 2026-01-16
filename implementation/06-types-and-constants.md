# Types & Constants

## Core Types (TypeScript)
```typescript
export enum GenerationStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export type LanguageCode = 'en' | 'es' | 'fr' | 'de' | 'zh' | 'ja' | 'pt' | 'it' | 'ru' | 'ar';

export interface EbookConfig {
  language: LanguageCode;
  chapterStructure: {
    basic: number;
    oneLevel: number;
    twoLevel: number;
  };
  contentSpecs: {
    wordsPerChapter: number;
    tone: 'professional' | 'casual' | 'academic';
    infographicStyle: 'modern' | 'minimalist' | 'creative';
  };
}
```

## Backend Constants (Python)
```python
AGENT_TIMEOUTS = {
    # Sequential Phase 1
    "ConfigurationLoader": 30,
    "TopicAnalysis": 60,
    "ContentStrategy": 90,
    
    # Parallel Phase 1 (Research)
    "ResearchSwarm": 180,
    
    # Parallel Phase 2 (Content)
    "ChapterGeneration": 600,
    
    # Parallel Phase 3 (Visuals)
    "InfographicGeneration": 300,
    "VisualDesign": 60,
    
    # Refinement
    "QualityEnhancement": 120,
    "CriticProofreading": 300,
    
    # Sequential Phase 2 (Publication)
    "SEOMetadata": 60,
    "LayoutFormatting": 120,
    "PDFGeneration": 120,
    "StorageIntegration": 60,
}

# Source of Truth Paths
PROMPTS_DIR = "prompts/"
TEMPLATES_DIR = "templates/pdf/"
MODEL_FALLBACK_ORDER = ["llama3.1", "mistral", "gpt-4o"]

SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "zh", "ja", "pt", "it", "ru", "ar"]
DEFAULT_WORD_COUNT = 3500
MAX_BATCH_SIZE = 10
```
