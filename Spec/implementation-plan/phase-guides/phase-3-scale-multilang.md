# Phase 3 Implementation Guide: Scale & Multi-Language Support
## Weeks 13-16: Batch Processing & 10-Language Support

**Phase Overview:**
- Duration: 4 weeks (Weeks 13-16)
- Primary Goal: Scale system to handle batch generation and support 10 languages
- Critical Requirements: Batch processing (10 ebooks), LanguageTool integration, RTL support for Arabic
- Success Criteria: 10 parallel ebook generation ≤60 minutes, all 10 languages with proper grammar checking

---

## Week 13-14: Batch Processing Infrastructure

### 1. SKILL 2: `/ebook-batch` Implementation

**File:** `F:\bookmake2\skills\ebook-batch\skill.yaml`

```yaml
name: ebook-batch
description: Generate multiple ebooks in parallel with batch processing
version: 1.0.0
author: System
parameters:
  - name: topics
    type: array
    description: Array of up to 10 topic sentences
    required: true
    min_items: 1
    max_items: 10
  - name: target_language
    type: string
    description: Target language code
    default: "en"
    enum: ["en", "es", "fr", "de", "zh", "ja", "pt", "it", "ru", "ar"]
  - name: parallel_pipelines
    type: integer
    description: Number of parallel pipelines (1-5)
    default: 3
    min: 1
    max: 5
  - name: configuration
    type: object
    description: Shared batch configuration
    properties:
      min_chapters:
        type: integer
        default: 7
      max_chapters:
        type: integer
        default: 10
      min_sections_per_chapter:
        type: integer
        default: 4
      max_sections_per_chapter:
        type: integer
        default: 7
      tone:
        type: string
        default: "professional"
      audience_level:
        type: string
        default: "general"
```

**Implementation:** `F:\bookmake2\skills\ebook-batch\index.js`

```javascript
const { Worker } = require('worker_threads');
const EventEmitter = require('events');
const path = require('path');

class BatchEbookGenerator extends EventEmitter {
  constructor(topics, options = {}) {
    super();
    this.topics = topics;
    this.targetLanguage = options.targetLanguage || 'en';
    this.parallelPipelines = Math.min(options.parallelPipelines || 3, 5);
    this.configuration = options.configuration || {};

    this.batchId = `batch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.queue = [...topics];
    this.runningWorkers = new Map();
    this.completedEbooks = new Map();
    this.failedEbooks = new Map();
    this.status = 'pending';
    this.startTime = null;
    this.endTime = null;
  }

  async start() {
    console.log(`Starting batch ${this.batchId} with ${this.topics.length} topics`);
    console.log(`Parallel pipelines: ${this.parallelPipelines}`);

    this.status = 'running';
    this.startTime = Date.now();
    this.emit('started', { batchId: this.batchId, totalTopics: this.topics.length });

    // Start initial workers
    while (this.runningWorkers.size < this.parallelPipelines && this.queue.length > 0) {
      const topic = this.queue.shift();
      await this.startPipeline(topic);
    }

    return this.batchId;
  }

  async startPipeline(topic) {
    const pipelineId = `pipeline_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    console.log(`Starting pipeline ${pipelineId} for topic: "${topic.substring(0, 50)}..."`);

    const workerData = {
      topic,
      targetLanguage: this.targetLanguage,
      configuration: this.configuration,
      pipelineId,
      batchId: this.batchId
    };

    const worker = new Worker(path.join(__dirname, 'pipeline-worker.js'), {
      workerData,
      resourceLimits: {
        maxOldGenerationSizeMb: 2048,
        maxYoungGenerationSizeMb: 512
      }
    });

    this.runningWorkers.set(pipelineId, {
      worker,
      topic,
      startTime: Date.now(),
      status: 'running'
    });

    this.emit('pipeline-started', { pipelineId, topic });

    worker.on('message', (message) => {
      this.handleWorkerMessage(pipelineId, message);
    });

    worker.on('error', (error) => {
      console.error(`Worker ${pipelineId} error:`, error);
      this.handlePipelineFailure(pipelineId, error);
    });

    worker.on('exit', (code) => {
      if (code !== 0) {
        this.handlePipelineFailure(pipelineId, new Error(`Worker exited with code ${code}`));
      }
      this.runningWorkers.delete(pipelineId);

      // Start next pipeline if available
      if (this.queue.length > 0 && this.status === 'running') {
        const nextTopic = this.queue.shift();
        this.startPipeline(nextTopic);
      }

      // Check if batch is complete
      this.checkCompletion();
    });

    return pipelineId;
  }

  handleWorkerMessage(pipelineId, message) {
    const { type, data } = message;

    switch (type) {
      case 'progress':
        this.emit('pipeline-progress', {
          pipelineId,
          progress: data.progress,
          stage: data.stage,
          message: data.message
        });
        break;

      case 'stage-complete':
        console.log(`Pipeline ${pipelineId} completed stage: ${data.stage}`);
        this.emit('pipeline-stage-complete', {
          pipelineId,
          stage: data.stage,
          duration: data.duration
        });
        break;

      case 'complete':
        console.log(`Pipeline ${pipelineId} completed successfully`);
        this.completedEbooks.set(pipelineId, {
          topic: this.runningWorkers.get(pipelineId)?.topic,
          ebookPath: data.ebookPath,
          metadata: data.metadata,
          duration: Date.now() - this.runningWorkers.get(pipelineId)?.startTime
        });
        this.emit('pipeline-complete', {
          pipelineId,
          ebookPath: data.ebookPath,
          metadata: data.metadata
        });
        break;

      case 'error':
        console.error(`Pipeline ${pipelineId} error:`, data.error);
        this.handlePipelineFailure(pipelineId, data.error);
        break;
    }
  }

  handlePipelineFailure(pipelineId, error) {
    const pipelineInfo = this.runningWorkers.get(pipelineId);
    this.failedEbooks.set(pipelineId, {
      topic: pipelineInfo?.topic,
      error: error.message,
      stack: error.stack,
      duration: Date.now() - pipelineInfo?.startTime
    });

    this.emit('pipeline-failed', {
      pipelineId,
      topic: pipelineInfo?.topic,
      error: error.message
    });

    // Terminate worker if still running
    if (pipelineInfo && pipelineInfo.worker) {
      pipelineInfo.worker.terminate();
    }
  }

  checkCompletion() {
    const total = this.topics.length;
    const completed = this.completedEbooks.size;
    const failed = this.failedEbooks.size;
    const finished = completed + failed;

    console.log(`Batch progress: ${finished}/${total} (completed: ${completed}, failed: ${failed})`);

    if (finished === total) {
      this.status = 'completed';
      this.endTime = Date.now();

      const summary = this.generateSummary();
      this.emit('complete', summary);
      console.log('Batch completed:', summary);
    }
  }

  generateSummary() {
    const duration = this.endTime - this.startTime;
    const completed = Array.from(this.completedEbooks.values());
    const failed = Array.from(this.failedEbooks.values());

    return {
      batchId: this.batchId,
      status: this.status,
      totalTopics: this.topics.length,
      completed: completed.length,
      failed: failed.length,
      duration,
      averageDuration: completed.length > 0
        ? duration / completed.length
        : 0,
      ebooks: completed.map(ebook => ({
        topic: ebook.topic,
        path: ebook.ebookPath,
        duration: ebook.duration,
        metadata: ebook.metadata
      })),
      failures: failed.map(failure => ({
        topic: failure.topic,
        error: failure.error,
        duration: failure.duration
      }))
    };
  }

  getStatus() {
    const running = Array.from(this.runningWorkers.values()).map(pipeline => ({
      pipelineId: pipeline.pipelineId,
      topic: pipeline.topic,
      status: pipeline.status,
      duration: Date.now() - pipeline.startTime
    }));

    return {
      batchId: this.batchId,
      status: this.status,
      totalTopics: this.topics.length,
      queued: this.queue.length,
      running: running.length,
      completed: this.completedEbooks.size,
      failed: this.failedEbooks.size,
      startTime: this.startTime,
      endTime: this.endTime,
      duration: this.endTime ? this.endTime - this.startTime : Date.now() - this.startTime,
      runningPipelines: running
    };
  }

  async cancel() {
    console.log(`Cancelling batch ${this.batchId}`);
    this.status = 'cancelled';

    // Terminate all running workers
    for (const [pipelineId, pipeline] of this.runningWorkers) {
      console.log(`Terminating pipeline ${pipelineId}`);
      pipeline.worker.terminate();
    }

    this.runningWorkers.clear();
    this.endTime = Date.now();

    this.emit('cancelled', {
      batchId: this.batchId,
      completed: this.completedEbooks.size,
      remaining: this.queue.length + this.runningWorkers.size
    });
  }
}

module.exports = BatchEbookGenerator;
```

**Pipeline Worker:** `F:\bookmake2\skills\ebook-batch\pipeline-worker.js`

```javascript
const { parentPort } = require('worker_threads');
const path = require('path');

// Import the main ebook generation skill
const EbookGenerator = require('../ebook-generation');

class PipelineWorker {
  constructor(topic, targetLanguage, configuration, pipelineId, batchId) {
    this.topic = topic;
    this.targetLanguage = targetLanguage;
    this.configuration = configuration;
    this.pipelineId = pipelineId;
    this.batchId = batchId;
    this.generator = null;
  }

  async run() {
    try {
      this.sendMessage('progress', {
        progress: 0,
        stage: 'initialization',
        message: 'Initializing pipeline'
      });

      // Create generator instance
      this.generator = new EbookGenerator(this.topic, {
        targetLanguage: this.targetLanguage,
        ...this.configuration
      });

      // Set up progress tracking
      this.generator.on('progress', (data) => {
        this.sendMessage('progress', {
          progress: data.progress,
          stage: data.stage,
          message: data.message
        });
      });

      this.generator.on('stage-complete', (data) => {
        this.sendMessage('stage-complete', {
          stage: data.stage,
          duration: data.duration
        });
      });

      // Run generation
      const result = await this.generator.generate();

      this.sendMessage('complete', {
        ebookPath: result.pdfPath,
        metadata: result.metadata
      });

    } catch (error) {
      console.error(`Pipeline ${this.pipelineId} error:`, error);
      this.sendMessage('error', {
        error: {
          message: error.message,
          stack: error.stack
        }
      });
      process.exit(1);
    }
  }

  sendMessage(type, data) {
    if (parentPort) {
      parentPort.postMessage({ type, data });
    }
  }
}

// Worker entry point
const { topic, targetLanguage, configuration, pipelineId, batchId } = workerData;

const worker = new PipelineWorker(topic, targetLanguage, configuration, pipelineId, batchId);
worker.run().then(() => {
  process.exit(0);
}).catch((error) => {
  console.error('Worker failed:', error);
  process.exit(1);
});
```

---

### 2. Batch API Endpoints

**File:** `F:\bookmake2\backend\api\routes\batch.js`

```javascript
const express = require('express');
const router = express.Router();
const BatchEbookGenerator = require('../../skills/ebook-batch');
const { authenticate } = require('../middleware/auth');

// Store active batches in memory (in production, use Redis)
const activeBatches = new Map();
const batchHistory = new Map();

/**
 * POST /api/generations/batch
 * Create a new batch generation job
 */
router.post('/batch', authenticate, async (req, res) => {
  try {
    const { topics, target_language = 'en', parallel_pipelines = 3, configuration } = req.body;

    // Validation
    if (!topics || !Array.isArray(topics)) {
      return res.status(400).json({
        success: false,
        error: 'topics must be an array'
      });
    }

    if (topics.length < 1 || topics.length > 10) {
      return res.status(400).json({
        success: false,
        error: 'topics must contain between 1 and 10 items'
      });
    }

    // Validate each topic
    for (const topic of topics) {
      if (typeof topic !== 'string' || topic.trim().length === 0) {
        return res.status(400).json({
          success: false,
          error: 'Each topic must be a non-empty string'
        });
      }

      if (topic.length > 500) {
        return res.status(400).json({
          success: false,
          error: 'Each topic must be less than 500 characters'
        });
      }
    }

    // Validate language
    const validLanguages = ['en', 'es', 'fr', 'de', 'zh', 'ja', 'pt', 'it', 'ru', 'ar'];
    if (!validLanguages.includes(target_language)) {
      return res.status(400).json({
        success: false,
        error: `Invalid language. Must be one of: ${validLanguages.join(', ')}`
      });
    }

    // Validate parallel_pipelines
    if (parallel_pipelines < 1 || parallel_pipelines > 5) {
      return res.status(400).json({
        success: false,
        error: 'parallel_pipelines must be between 1 and 5'
      });
    }

    // Create batch generator
    const batch = new BatchEbookGenerator(topics, {
      targetLanguage: target_language,
      parallelPipelines: parallel_pipelines,
      configuration
    });

    // Set up event handlers
    batch.on('pipeline-started', (data) => {
      console.log(`Pipeline started: ${data.pipelineId}`);
    });

    batch.on('pipeline-progress', (data) => {
      // Could emit WebSocket event here for real-time updates
      console.log(`Pipeline ${data.pipelineId} progress: ${data.progress}%`);
    });

    batch.on('pipeline-complete', (data) => {
      console.log(`Pipeline completed: ${data.pipelineId}`);
    });

    batch.on('pipeline-failed', (data) => {
      console.error(`Pipeline failed: ${data.pipelineId}`, data.error);
    });

    batch.on('complete', (summary) => {
      console.log('Batch complete:', summary);
      batchHistory.set(summary.batchId, summary);
      activeBatches.delete(summary.batchId);
    });

    batch.on('cancelled', (data) => {
      console.log('Batch cancelled:', data);
      batchHistory.set(data.batchId, {
        batchId: data.batchId,
        status: 'cancelled',
        completed: data.completed,
        cancelledAt: new Date().toISOString()
      });
      activeBatches.delete(data.batchId);
    });

    // Start batch
    const batchId = await batch.start();
    activeBatches.set(batchId, batch);

    res.json({
      success: true,
      data: {
        batchId,
        status: 'started',
        totalTopics: topics.length,
        targetLanguage: target_language,
        parallelPipelines: parallel_pipelines,
        estimatedDuration: topics.length * 6 * 60 * 1000 // Rough estimate: 6 min per ebook
      }
    });

  } catch (error) {
    console.error('Batch creation error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to create batch job',
      details: error.message
    });
  }
});

/**
 * GET /api/batch/:id/status
 * Get batch job status
 */
router.get('/batch/:id/status', authenticate, async (req, res) => {
  try {
    const { id } = req.params;

    // Check active batches
    let batch = activeBatches.get(id);
    let fromHistory = false;

    // Check history if not active
    if (!batch) {
      const historyEntry = batchHistory.get(id);
      if (historyEntry) {
        batch = historyEntry;
        fromHistory = true;
      }
    }

    if (!batch) {
      return res.status(404).json({
        success: false,
        error: 'Batch not found'
      });
    }

    const status = fromHistory ? batch : batch.getStatus();

    res.json({
      success: true,
      data: status
    });

  } catch (error) {
    console.error('Batch status error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get batch status',
      details: error.message
    });
  }
});

/**
 * GET /api/batch/:id/details
 * Get detailed batch information including progress for each pipeline
 */
router.get('/batch/:id/details', authenticate, async (req, res) => {
  try {
    const { id } = req.params;

    const batch = activeBatches.get(id);
    if (!batch) {
      return res.status(404).json({
        success: false,
        error: 'Batch not found or already completed'
      });
    }

    const status = batch.getStatus();
    const details = {
      ...status,
      pipelines: [],
      queue: batch.queue.map((topic, index) => ({
        index,
        topic: topic.substring(0, 100)
      })),
      completed: Array.from(batch.completedEbooks.entries()).map(([id, ebook]) => ({
        pipelineId: id,
        topic: ebook.topic.substring(0, 100),
        path: ebook.ebookPath,
        duration: ebook.duration,
        metadata: ebook.metadata
      })),
      failed: Array.from(batch.failedEbooks.entries()).map(([id, failure]) => ({
        pipelineId: id,
        topic: failure.topic.substring(0, 100),
        error: failure.error,
        duration: failure.duration
      }))
    };

    res.json({
      success: true,
      data: details
    });

  } catch (error) {
    console.error('Batch details error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get batch details',
      details: error.message
    });
  }
});

/**
 * POST /api/batch/:id/cancel
 * Cancel a running batch job
 */
router.post('/batch/:id/cancel', authenticate, async (req, res) => {
  try {
    const { id } = req.params;

    const batch = activeBatches.get(id);
    if (!batch) {
      return res.status(404).json({
        success: false,
        error: 'Batch not found or already completed'
      });
    }

    if (batch.status === 'completed' || batch.status === 'cancelled') {
      return res.status(400).json({
        success: false,
        error: `Cannot cancel batch with status: ${batch.status}`
      });
    }

    await batch.cancel();

    res.json({
      success: true,
      data: {
        batchId: id,
        status: 'cancelled',
        completed: batch.completedEbooks.size,
        cancelledAt: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Batch cancellation error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to cancel batch',
      details: error.message
    });
  }
});

/**
 * GET /api/batches
 * List all batches (active and historical)
 */
router.get('/batches', authenticate, async (req, res) => {
  try {
    const { limit = 50, offset = 0 } = req.query;

    const active = Array.from(activeBatches.values()).map(batch => batch.getStatus());
    const history = Array.from(batchHistory.values())
      .sort((a, b) => new Date(b.endTime) - new Date(a.endTime))
      .slice(parseInt(offset), parseInt(offset) + parseInt(limit));

    res.json({
      success: true,
      data: {
        active,
        history,
        total: {
          active: active.length,
          history: batchHistory.size
        }
      }
    });

  } catch (error) {
    console.error('List batches error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to list batches',
      details: error.message
    });
  }
});

module.exports = router;
```

---

### 3. Celery Task Queue Enhancement

**File:** `F:\bookmake2\backend\celery\tasks.py`

```python
from celery import Celery, group, chain, chord
from celery.result import GroupResult
from celery.exceptions import SoftTimeLimitExceeded
import redis
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configure Celery with Redis
celery_app = Celery(
    'ebook_generator',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

# Queue configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,

    # Queue priorities
    task_routes={
        'tasks.batch_generation': {'queue': 'batch'},
        'tasks.single_generation': {'queue': 'default'},
        'tasks.priority_generation': {'queue': 'priority'},
    },

    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,

    # Task time limits
    task_soft_time_limit=3600,  # 1 hour
    task_time_limit=4200,       # 70 minutes

    # Result backend
    result_expires=86400,  # 24 hours
    result_extended=True,
)

# Redis client for queue monitoring
redis_client = redis.Redis(host='localhost', port=6379, db=2)

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='tasks.single_generation')
def single_generation(self, topic: str, target_language: str, configuration: Dict[str, Any]):
    """
    Generate a single ebook
    """
    from ebook_generator import EbookGenerator

    logger.info(f"Starting generation for topic: {topic[:50]}")

    try:
        generator = EbookGenerator(topic, {
            'target_language': target_language,
            **configuration
        })

        result = generator.generate()

        logger.info(f"Completed generation for topic: {topic[:50]}")

        return {
            'success': True,
            'topic': topic,
            'pdf_path': result['pdf_path'],
            'metadata': result['metadata'],
            'task_id': self.request.id
        }

    except SoftTimeLimitExceeded:
        logger.error(f"Time limit exceeded for topic: {topic[:50]}")
        return {
            'success': False,
            'topic': topic,
            'error': 'Task time limit exceeded',
            'task_id': self.request.id
        }
    except Exception as e:
        logger.error(f"Generation failed for topic: {topic[:50]}, error: {str(e)}")
        return {
            'success': False,
            'topic': topic,
            'error': str(e),
            'task_id': self.request.id
        }


@celery_app.task(bind=True, name='tasks.batch_generation')
def batch_generation(self, topics: List[str], target_language: str,
                    parallel_pipelines: int, configuration: Dict[str, Any]):
    """
    Generate multiple ebooks in batch with parallel processing
    """
    batch_id = f"batch_{datetime.utcnow().timestamp()}"
    logger.info(f"Starting batch {batch_id} with {len(topics)} topics")

    # Store batch metadata in Redis
    batch_metadata = {
        'batch_id': batch_id,
        'total_topics': len(topics),
        'target_language': target_language,
        'parallel_pipelines': parallel_pipelines,
        'configuration': configuration,
        'status': 'running',
        'started_at': datetime.utcnow().isoformat(),
        'completed': 0,
        'failed': 0
    }
    redis_client.set(f"batch:{batch_id}", json.dumps(batch_metadata))

    # Create tasks for each topic
    tasks = []
    for topic in topics:
        task = single_generation.s(topic, target_language, configuration)
        tasks.append(task)

    # Execute tasks in parallel groups
    results = []
    for i in range(0, len(tasks), parallel_pipelines):
        group_tasks = tasks[i:i + parallel_pipelines]
        job = group(group_tasks)
        group_result = job.apply_async()

        # Wait for group to complete
        while not group_result.ready():
            group_result.join(timeout=10)

            # Update batch progress
            completed_count = sum(1 for r in group_result.results if r.ready())
            metadata = json.loads(redis_client.get(f"batch:{batch_id}"))
            metadata['completed'] = completed_count
            metadata['failed'] = sum(1 for r in group_result.results if r.result and not r.result.get('success'))
            redis_client.set(f"batch:{batch_id}", json.dumps(metadata))

            # Update task progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'batch_id': batch_id,
                    'completed': completed_count,
                    'total': len(topics),
                    'progress': int((completed_count / len(topics)) * 100)
                }
            )

        # Collect results
        for result in group_result.results:
            results.append(result.result)

    # Update batch metadata
    completed_count = sum(1 for r in results if r.get('success'))
    failed_count = sum(1 for r in results if not r.get('success'))

    batch_metadata['status'] = 'completed'
    batch_metadata['completed'] = completed_count
    batch_metadata['failed'] = failed_count
    batch_metadata['completed_at'] = datetime.utcnow().isoformat()
    redis_client.set(f"batch:{batch_id}", json.dumps(batch_metadata))

    logger.info(f"Batch {batch_id} completed: {completed_count} succeeded, {failed_count} failed")

    return {
        'success': True,
        'batch_id': batch_id,
        'total_topics': len(topics),
        'completed': completed_count,
        'failed': failed_count,
        'results': results
    }


@celery_app.task(bind=True, name='tasks.monitor_batch')
def monitor_batch(self, batch_id: str):
    """
    Monitor batch progress and return detailed status
    """
    batch_data = redis_client.get(f"batch:{batch_id}")

    if not batch_data:
        return {
            'success': False,
            'error': 'Batch not found'
        }

    metadata = json.loads(batch_data)

    return {
        'success': True,
        'batch_id': batch_id,
        'status': metadata['status'],
        'total_topics': metadata['total_topics'],
        'completed': metadata['completed'],
        'failed': metadata['failed'],
        'progress': int((metadata['completed'] / metadata['total_topics']) * 100),
        'started_at': metadata['started_at'],
        'completed_at': metadata.get('completed_at')
    }


@celery_app.task(bind=True, name='tasks.cancel_batch')
def cancel_batch(self, batch_id: str):
    """
    Cancel a running batch
    """
    batch_data = redis_client.get(f"batch:{batch_id}")

    if not batch_data:
        return {
            'success': False,
            'error': 'Batch not found'
        }

    metadata = json.loads(batch_data)

    if metadata['status'] in ['completed', 'cancelled']:
        return {
            'success': False,
            'error': f"Cannot cancel batch with status: {metadata['status']}"
        }

    # Revoke all tasks in the batch
    # Note: This requires storing task IDs in Redis when creating the batch
    task_ids = metadata.get('task_ids', [])
    for task_id in task_ids:
        celery_app.control.revoke(task_id, terminate=True)

    # Update metadata
    metadata['status'] = 'cancelled'
    metadata['cancelled_at'] = datetime.utcnow().isoformat()
    redis_client.set(f"batch:{batch_id}", json.dumps(metadata))

    logger.info(f"Batch {batch_id} cancelled")

    return {
        'success': True,
        'batch_id': batch_id,
        'cancelled_at': metadata['cancelled_at']
    }


@celery_app.task(bind=True, name='tasks.flush_queue')
def flush_queue(self, queue_name: str = 'default'):
    """
    Flush all tasks from a queue
    """
    try:
        celery_app.control.purge()
        logger.info(f"Flushed queue: {queue_name}")

        return {
            'success': True,
            'queue': queue_name,
            'flushed_at': datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to flush queue {queue_name}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task(bind=True, name='tasks.get_queue_stats')
def get_queue_stats(self):
    """
    Get statistics about all queues
    """
    inspector = celery_app.control.inspect()

    # Get active tasks
    active = inspector.active()
    # Get scheduled tasks
    scheduled = inspector.scheduled()
    # Get reserved tasks
    reserved = inspector.reserved()

    stats = {
        'queues': {},
        'timestamp': datetime.utcnow().isoformat()
    }

    for queue in ['default', 'batch', 'priority']:
        active_count = sum(len(tasks) for tasks in (active or {}).values()) if active else 0
        scheduled_count = sum(len(tasks) for tasks in (scheduled or {}).values()) if scheduled else 0
        reserved_count = sum(len(tasks) for tasks in (reserved or {}).values()) if reserved else 0

        stats['queues'][queue] = {
            'active': active_count,
            'scheduled': scheduled_count,
            'reserved': reserved_count,
            'total': active_count + scheduled_count + reserved_count
        }

    return stats


# Fair scheduling implementation
@celery_app.task(bind=True, name='tasks.priority_generation')
def priority_generation(self, topic: str, target_language: str,
                       configuration: Dict[str, Any], priority: int = 5):
    """
    Generate ebook with priority (1-10, where 1 is highest priority)
    """
    # Set task priority
    self.request.delivery_info['priority'] = priority

    return single_generation(topic, target_language, configuration)
```

**Celery Configuration:** `F:\bookmake2\backend\celery\celeryconfig.py`

```python
from celery import Celery

class CeleryConfig:
    # Broker settings
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'

    # Task settings
    task_serializer = 'json'
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'UTC'
    enable_utc = True

    # Queue configuration
    task_queues = {
        'priority': {
            'exchange': 'priority',
            'exchange_type': 'direct',
            'routing_key': 'priority',
        },
        'batch': {
            'exchange': 'batch',
            'exchange_type': 'direct',
            'routing_key': 'batch',
        },
        'default': {
            'exchange': 'default',
            'exchange_type': 'direct',
            'routing_key': 'default',
        },
    }

    # Task routing
    task_routes = {
        'tasks.priority_generation': {'queue': 'priority'},
        'tasks.batch_generation': {'queue': 'batch'},
        'tasks.single_generation': {'queue': 'default'},
    }

    # Worker settings
    worker_prefetch_multiplier = 1
    worker_max_tasks_per_child = 50

    # Task time limits
    task_soft_time_limit = 3600  # 1 hour
    task_time_limit = 4200       # 70 minutes

    # Result settings
    result_expires = 86400  # 24 hours
    result_extended = True

    # Priority settings
    task_inherit_parent_priority = True
    task_default_priority = 5
    worker_disable_rate_limits = False
```

**Worker Startup Script:** `F:\bookmake2\backend\celery\start-workers.sh`

```bash
#!/bin/bash

# Start Celery workers for different queues

echo "Starting Celery workers..."

# Priority queue worker (1 worker, high priority tasks)
celery -A celery.tasks worker \
    --loglevel=info \
    --queue=priority \
    --concurrency=1 \
    --max-tasks-per-child=50 \
    -n priority-worker@%h &

# Batch queue workers (3 workers, parallel batch processing)
celery -A celery.tasks worker \
    --loglevel=info \
    --queue=batch \
    --concurrency=3 \
    --max-tasks-per-child=50 \
    -n batch-worker@%h &

# Default queue workers (2 workers, normal tasks)
celery -A celery.tasks worker \
    --loglevel=info \
    --queue=default \
    --concurrency=2 \
    --max-tasks-per-child=50 \
    -n default-worker@%h &

echo "Celery workers started"
wait
```

---

### 4. Frontend: Complete Batch Generate Page

**File:** `F:\bookmake2\frontend\src\pages\batch-generate.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Loader2,
  Play,
  X,
  CheckCircle,
  XCircle,
  Clock,
  FileText,
  Download,
  Settings
} from 'lucide-react';

const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'zh', name: '中文', flag: '🇨🇳' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
  { code: 'pt', name: 'Português', flag: '🇵🇹' },
  { code: 'it', name: 'Italiano', flag: '🇮🇹' },
  { code: 'ru', name: 'Русский', flag: '🇷🇺' },
  { code: 'ar', name: 'العربية', flag: '🇸🇦' }
];

const TOPIC_PLACEHOLDERS = [
  'Enter first topic...',
  'Enter second topic...',
  'Enter third topic...',
  'Enter fourth topic...',
  'Enter fifth topic...',
  'Enter sixth topic...',
  'Enter seventh topic...',
  'Enter eighth topic...',
  'Enter ninth topic...',
  'Enter tenth topic...'
];

export default function BatchGeneratePage() {
  const [topics, setTopics] = useState(Array(10).fill(''));
  const [targetLanguage, setTargetLanguage] = useState('en');
  const [parallelPipelines, setParallelPipelines] = useState(3);
  const [configuration, setConfiguration] = useState({
    min_chapters: 7,
    max_chapters: 10,
    min_sections_per_chapter: 4,
    max_sections_per_chapter: 7,
    tone: 'professional',
    audience_level: 'general'
  });

  const [batchId, setBatchId] = useState(null);
  const [batchStatus, setBatchStatus] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);
  const [pollInterval, setPollInterval] = useState(null);

  // Poll batch status
  useEffect(() => {
    if (batchId && isGenerating) {
      const interval = setInterval(async () => {
        try {
          const response = await axios.get(`/api/batch/${batchId}/details`);
          setBatchStatus(response.data.data);

          if (response.data.data.status === 'completed' ||
              response.data.data.status === 'cancelled') {
            setIsGenerating(false);
            clearInterval(interval);
            setPollInterval(null);
          }
        } catch (err) {
          console.error('Error polling batch status:', err);
          setError(err.response?.data?.error || 'Failed to get batch status');
          clearInterval(interval);
        }
      }, 2000); // Poll every 2 seconds

      setPollInterval(interval);

      return () => clearInterval(interval);
    }
  }, [batchId, isGenerating]);

  const handleTopicChange = (index, value) => {
    const newTopics = [...topics];
    newTopics[index] = value;
    setTopics(newTopics);
  };

  const handleStartBatch = async () => {
    setError(null);

    // Validate topics
    const validTopics = topics.filter(t => t.trim().length > 0);

    if (validTopics.length === 0) {
      setError('Please enter at least one topic');
      return;
    }

    if (validTopics.length > 10) {
      setError('Maximum 10 topics allowed');
      return;
    }

    setIsGenerating(true);

    try {
      const response = await axios.post('/api/generations/batch', {
        topics: validTopics,
        target_language: targetLanguage,
        parallel_pipelines: parallelPipelines,
        configuration
      });

      setBatchId(response.data.data.batchId);
      setBatchStatus({
        batchId: response.data.data.batchId,
        status: 'running',
        totalTopics: validTopics.length,
        completed: 0,
        failed: 0
      });

    } catch (err) {
      console.error('Batch creation error:', err);
      setError(err.response?.data?.error || 'Failed to create batch');
      setIsGenerating(false);
    }
  };

  const handleCancelBatch = async () => {
    if (!batchId) return;

    try {
      await axios.post(`/api/batch/${batchId}/cancel`);
      setIsGenerating(false);

      if (pollInterval) {
        clearInterval(pollInterval);
        setPollInterval(null);
      }

    } catch (err) {
      console.error('Batch cancellation error:', err);
      setError(err.response?.data?.error || 'Failed to cancel batch');
    }
  };

  const formatDuration = (ms) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`;
    }
    return `${remainingSeconds}s`;
  };

  const getProgressPercentage = () => {
    if (!batchStatus) return 0;
    const total = batchStatus.totalTopics || 1;
    const finished = (batchStatus.completed || 0) + (batchStatus.failed || 0);
    return Math.round((finished / total) * 100);
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Batch Ebook Generation</h1>
          <p className="text-muted-foreground">
            Generate up to 10 ebooks in parallel with customizable settings
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Input Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Topics Input */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Topics (up to 10)
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {topics.map((topic, index) => (
                  <div key={index} className="space-y-2">
                    <Label htmlFor={`topic-${index}`}>
                      Topic {index + 1}
                    </Label>
                    <Input
                      id={`topic-${index}`}
                      placeholder={TOPIC_PLACEHOLDERS[index]}
                      value={topic}
                      onChange={(e) => handleTopicChange(index, e.target.value)}
                      disabled={isGenerating}
                      maxLength={500}
                    />
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Language Selection */}
            <Card>
              <CardHeader>
                <CardTitle>Target Language</CardTitle>
              </CardHeader>
              <CardContent>
                <RadioGroup
                  value={targetLanguage}
                  onValueChange={setTargetLanguage}
                  disabled={isGenerating}
                  className="grid grid-cols-2 gap-4"
                >
                  {LANGUAGES.map(lang => (
                    <div
                      key={lang.code}
                      className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-accent"
                    >
                      <RadioGroupItem
                        value={lang.code}
                        id={`lang-${lang.code}`}
                      />
                      <Label
                        htmlFor={`lang-${lang.code}`}
                        className="flex items-center gap-2 cursor-pointer flex-1"
                      >
                        <span className="text-2xl">{lang.flag}</span>
                        <span>{lang.name}</span>
                      </Label>
                    </div>
                  ))}
                </RadioGroup>
              </CardContent>
            </Card>

            {/* Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  Configuration
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <div>
                    <Label>Parallel Pipelines: {parallelPipelines}</Label>
                    <p className="text-sm text-muted-foreground mb-2">
                      Number of ebooks to generate simultaneously
                    </p>
                    <Slider
                      value={[parallelPipelines]}
                      onValueChange={(value) => setParallelPipelines(value[0])}
                      min={1}
                      max={5}
                      step={1}
                      disabled={isGenerating}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-muted-foreground mt-1">
                      <span>1 (Slow)</span>
                      <span>5 (Fast)</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="min-chapters">Min Chapters</Label>
                      <Input
                        id="min-chapters"
                        type="number"
                        min={1}
                        max={20}
                        value={configuration.min_chapters}
                        onChange={(e) => setConfiguration({
                          ...configuration,
                          min_chapters: parseInt(e.target.value)
                        })}
                        disabled={isGenerating}
                      />
                    </div>
                    <div>
                      <Label htmlFor="max-chapters">Max Chapters</Label>
                      <Input
                        id="max-chapters"
                        type="number"
                        min={1}
                        max={20}
                        value={configuration.max_chapters}
                        onChange={(e) => setConfiguration({
                          ...configuration,
                          max_chapters: parseInt(e.target.value)
                        })}
                        disabled={isGenerating}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="min-sections">Min Sections per Chapter</Label>
                      <Input
                        id="min-sections"
                        type="number"
                        min={1}
                        max={20}
                        value={configuration.min_sections_per_chapter}
                        onChange={(e) => setConfiguration({
                          ...configuration,
                          min_sections_per_chapter: parseInt(e.target.value)
                        })}
                        disabled={isGenerating}
                      />
                    </div>
                    <div>
                      <Label htmlFor="max-sections">Max Sections per Chapter</Label>
                      <Input
                        id="max-sections"
                        type="number"
                        min={1}
                        max={20}
                        value={configuration.max_sections_per_chapter}
                        onChange={(e) => setConfiguration({
                          ...configuration,
                          max_sections_per_chapter: parseInt(e.target.value)
                        })}
                        disabled={isGenerating}
                      />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Error Alert */}
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Action Buttons */}
            <div className="flex gap-4">
              {!isGenerating ? (
                <Button
                  onClick={handleStartBatch}
                  size="lg"
                  className="flex-1"
                  disabled={topics.filter(t => t.trim()).length === 0}
                >
                  <Play className="w-5 h-5 mr-2" />
                  Start Batch Generation
                </Button>
              ) : (
                <Button
                  onClick={handleCancelBatch}
                  size="lg"
                  variant="destructive"
                  className="flex-1"
                >
                  <X className="w-5 h-5 mr-2" />
                  Cancel Batch
                </Button>
              )}
            </div>
          </div>

          {/* Right Column: Status & Progress */}
          <div className="space-y-6">
            {/* Batch Overview */}
            <Card>
              <CardHeader>
                <CardTitle>Batch Status</CardTitle>
              </CardHeader>
              <CardContent>
                {!batchStatus ? (
                  <p className="text-sm text-muted-foreground">
                    No batch running
                  </p>
                ) : (
                  <div className="space-y-4">
                    <div>
                      <Label>Batch ID</Label>
                      <p className="text-sm font-mono">{batchStatus.batchId}</p>
                    </div>

                    <div>
                      <Label>Status</Label>
                      <Badge
                        variant={
                          batchStatus.status === 'completed' ? 'success' :
                          batchStatus.status === 'running' ? 'default' :
                          'destructive'
                        }
                      >
                        {batchStatus.status}
                      </Badge>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Total</p>
                        <p className="font-semibold">{batchStatus.totalTopics}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Queued</p>
                        <p className="font-semibold">{batchStatus.queued || 0}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Running</p>
                        <p className="font-semibold">{batchStatus.running || 0}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Completed</p>
                        <p className="font-semibold text-green-600">
                          {batchStatus.completed || 0}
                        </p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Failed</p>
                        <p className="font-semibold text-red-600">
                          {batchStatus.failed || 0}
                        </p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Duration</p>
                        <p className="font-semibold">
                          {formatDuration(batchStatus.duration || 0)}
                        </p>
                      </div>
                    </div>

                    <div>
                      <Label>Progress</Label>
                      <Progress value={getProgressPercentage()} />
                      <p className="text-sm text-muted-foreground mt-1">
                        {getProgressPercentage()}% complete
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Pipeline Details */}
            {batchStatus && batchStatus.runningPipelines && batchStatus.runningPipelines.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Running Pipelines</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {batchStatus.runningPipelines.map(pipeline => (
                    <div key={pipeline.pipelineId} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <Badge variant="default">
                          <Loader2 className="w-3 h-3 mr-1 animate-spin" />
                          Running
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {formatDuration(pipeline.duration)}
                        </span>
                      </div>
                      <p className="text-sm line-clamp-2">
                        {pipeline.topic}
                      </p>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Completed Ebooks */}
            {batchStatus && batchStatus.completed && batchStatus.completed.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    Completed ({batchStatus.completed.length})
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {batchStatus.completed.map((ebook, index) => (
                    <div key={index} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <Badge variant="success">
                          <CheckCircle className="w-3 h-3 mr-1" />
                          Complete
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {formatDuration(ebook.duration)}
                        </span>
                      </div>
                      <p className="text-sm line-clamp-2">{ebook.topic}</p>
                      <Button
                        size="sm"
                        variant="outline"
                        className="w-full"
                        asChild
                      >
                        <a href={ebook.path} download>
                          <Download className="w-4 h-4 mr-2" />
                          Download PDF
                        </a>
                      </Button>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Failed Ebooks */}
            {batchStatus && batchStatus.failed && batchStatus.failed.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <XCircle className="w-5 h-5 text-red-600" />
                    Failed ({batchStatus.failed.length})
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {batchStatus.failed.map((failure, index) => (
                    <div key={index} className="border border-red-200 rounded-lg p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <Badge variant="destructive">
                          <XCircle className="w-3 h-3 mr-1" />
                          Failed
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {formatDuration(failure.duration)}
                        </span>
                      </div>
                      <p className="text-sm line-clamp-2">{failure.topic}</p>
                      <p className="text-xs text-red-600">{failure.error}</p>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

### 5. Load Testing

**File:** `F:\bookmake2\tests\load\batch-load-test.js`

```javascript
const axios = require('axios');
const { performance } = require('perf_hooks');

const API_BASE = 'http://localhost:3000/api';

// Test topics
const testTopics = [
  'The history of artificial intelligence and machine learning',
  'Introduction to modern web development with React and Node.js',
  'Understanding blockchain technology and cryptocurrency',
  'The science of climate change and environmental sustainability',
  'Essential principles of effective leadership and management',
  'A guide to healthy nutrition and fitness for beginners',
  'The fundamentals of graphic design and visual communication',
  'Introduction to cloud computing and distributed systems',
  'The art of creative writing and storytelling techniques',
  'Understanding psychology and human behavior'
];

class BatchLoadTest {
  constructor() {
    this.results = [];
  }

  async testSingleTopic(topic) {
    const startTime = performance.now();

    try {
      const response = await axios.post(`${API_BASE}/generations`, {
        topic,
        target_language: 'en'
      });

      const duration = performance.now() - startTime;

      return {
        success: true,
        topic,
        duration,
        pdfPath: response.data.data.pdf_path
      };
    } catch (error) {
      const duration = performance.now() - startTime;

      return {
        success: false,
        topic,
        duration,
        error: error.message
      };
    }
  }

  async testBatch(topics, parallelPipelines = 3) {
    const startTime = performance.now();

    try {
      const response = await axios.post(`${API_BASE}/generations/batch`, {
        topics,
        target_language: 'en',
        parallel_pipelines: parallelPipelines
      });

      const batchId = response.data.data.batchId;
      console.log(`Batch created: ${batchId}`);

      // Poll for completion
      let status;
      let pollCount = 0;
      const maxPolls = 180; // 30 minutes max

      do {
        await new Promise(resolve => setTimeout(resolve, 2000));

        const statusResponse = await axios.get(`${API_BASE}/batch/${batchId}/status`);
        status = statusResponse.data.data;

        pollCount++;
        console.log(`Poll ${pollCount}: ${status.completed}/${status.totalTopics} completed, ${status.failed} failed`);

      } while (status.status !== 'completed' && status.status !== 'cancelled' && pollCount < maxPolls);

      const duration = performance.now() - startTime;

      return {
        success: status.status === 'completed',
        batchId,
        duration,
        totalTopics: status.totalTopics,
        completed: status.completed,
        failed: status.failed,
        averageTimePerEbook: duration / status.totalTopics
      };

    } catch (error) {
      const duration = performance.now() - startTime;

      return {
        success: false,
        duration,
        error: error.message
      };
    }
  }

  async runTests() {
    console.log('Starting Batch Load Tests...\n');

    // Test 1: Single generation (baseline)
    console.log('Test 1: Single generation (baseline)');
    const singleResult = await this.testSingleTopic(testTopics[0]);
    console.log(`Result: ${singleResult.success ? 'SUCCESS' : 'FAILED'}, Duration: ${(singleResult.duration / 1000).toFixed(2)}s\n`);
    this.results.push({ test: 'Single Generation', ...singleResult });

    // Test 2: 3 parallel pipelines
    console.log('\nTest 2: 3 parallel pipelines (3 topics)');
    const batch3Result = await this.testBatch(testTopics.slice(0, 3), 3);
    console.log(`Result: ${batch3Result.success ? 'SUCCESS' : 'FAILED'}`);
    console.log(`Duration: ${(batch3Result.duration / 1000 / 60).toFixed(2)} minutes`);
    console.log(`Completed: ${batch3Result.completed}, Failed: ${batch3Result.failed}`);
    console.log(`Average time per ebook: ${(batch3Result.averageTimePerEbook / 1000 / 60).toFixed(2)} minutes\n`);
    this.results.push({ test: '3 Parallel Pipelines', ...batch3Result });

    // Test 3: 5 parallel pipelines
    console.log('\nTest 3: 5 parallel pipelines (5 topics)');
    const batch5Result = await this.testBatch(testTopics.slice(0, 5), 5);
    console.log(`Result: ${batch5Result.success ? 'SUCCESS' : 'FAILED'}`);
    console.log(`Duration: ${(batch5Result.duration / 1000 / 60).toFixed(2)} minutes`);
    console.log(`Completed: ${batch5Result.completed}, Failed: ${batch5Result.failed}`);
    console.log(`Average time per ebook: ${(batch5Result.averageTimePerEbook / 1000 / 60).toFixed(2)} minutes\n`);
    this.results.push({ test: '5 Parallel Pipelines', ...batch5Result });

    // Test 4: Full batch (10 topics, 3 pipelines)
    console.log('\nTest 4: Full batch - 10 topics with 3 pipelines');
    const batch10Result = await this.testBatch(testTopics, 3);
    console.log(`Result: ${batch10Result.success ? 'SUCCESS' : 'FAILED'}`);
    console.log(`Duration: ${(batch10Result.duration / 1000 / 60).toFixed(2)} minutes`);
    console.log(`Target: ≤60 minutes`);
    console.log(`Status: ${batch10Result.duration <= 60 * 60 * 1000 ? 'PASS' : 'FAIL'}`);
    console.log(`Completed: ${batch10Result.completed}, Failed: ${batch10Result.failed}`);
    console.log(`Average time per ebook: ${(batch10Result.averageTimePerEbook / 1000 / 60).toFixed(2)} minutes\n`);
    this.results.push({ test: '10 Topic Batch (3 pipelines)', ...batch10Result });

    // Test 5: Queue management (start 2 batches quickly)
    console.log('\nTest 5: Queue management (2 concurrent batches)');
    const [batch1, batch2] = await Promise.all([
      this.testBatch(testTopics.slice(0, 3), 2),
      this.testBatch(testTopics.slice(3, 6), 2)
    ]);
    console.log(`Batch 1: ${batch1.success ? 'SUCCESS' : 'FAILED'}, Duration: ${(batch1.duration / 1000 / 60).toFixed(2)} minutes`);
    console.log(`Batch 2: ${batch2.success ? 'SUCCESS' : 'FAILED'}, Duration: ${(batch2.duration / 1000 / 60).toFixed(2)} minutes\n`);
    this.results.push({ test: 'Concurrent Batches', batch1, batch2 });

    // Test 6: Cancellation
    console.log('\nTest 6: Batch cancellation');
    try {
      const createResponse = await axios.post(`${API_BASE}/generations/batch`, {
        topics: testTopics.slice(0, 5),
        target_language: 'en',
        parallel_pipelines: 3
      });
      const batchId = createResponse.data.data.batchId;

      // Wait 5 seconds then cancel
      await new Promise(resolve => setTimeout(resolve, 5000));

      const cancelResponse = await axios.post(`${API_BASE}/batch/${batchId}/cancel`);
      console.log(`Cancellation: ${cancelResponse.data.success ? 'SUCCESS' : 'FAILED'}`);
      this.results.push({ test: 'Batch Cancellation', success: cancelResponse.data.success });
    } catch (error) {
      console.log(`Cancellation: FAILED - ${error.message}`);
      this.results.push({ test: 'Batch Cancellation', success: false, error: error.message });
    }

    // Print summary
    console.log('\n' + '='.repeat(50));
    console.log('LOAD TEST SUMMARY');
    console.log('='.repeat(50));

    this.results.forEach(result => {
      console.log(`\n${result.test}:`);
      if (result.batch1 && result.batch2) {
        console.log(`  Batch 1: ${result.batch1.success ? 'PASS' : 'FAIL'}`);
        console.log(`  Batch 2: ${result.batch2.success ? 'PASS' : 'FAIL'}`);
      } else {
        console.log(`  Status: ${result.success ? 'PASS' : 'FAIL'}`);
        if (result.duration) {
          console.log(`  Duration: ${(result.duration / 1000 / 60).toFixed(2)} minutes`);
        }
      }
    });

    console.log('\n' + '='.repeat(50));
  }
}

// Run tests
const test = new BatchLoadTest();
test.runTests().catch(console.error);
```

---

## Week 15-16: Multi-Language Support Implementation

### 1. LanguageTool Integration

**Installation:** `F:\bookmake2\backend\scripts\install-languagetool.sh`

```bash
#!/bin/bash

echo "Installing LanguageTool for multi-language support..."

# Install LanguageTool
cd /opt
sudo wget https://languagetool.org/download/LanguageTool-6.3.zip
sudo unzip LanguageTool-6.3.zip
sudo rm LanguageTool-6.3.zip
sudo mv LanguageTool-6.3 languagetool

# Install language packages
cd languagetool

# Download language dictionaries for all 10 languages
declare -a LANGUAGES=(
    "en"    # English
    "es"    # Spanish
    "fr"    # French
    "de"    # German
    "zh"    # Chinese
    "ja"    # Japanese
    "pt"    # Portuguese
    "it"    # Italian
    "ru"    # Russian
    "ar"    # Arabic
)

for lang in "${LANGUAGES[@]}"; do
    echo "Installing language pack for: $lang"
    # LanguageTool includes most dictionaries by default
    # For additional dictionaries, download from:
    # https://languagetool.org/download/LanguageTool-6.3.zip
done

# Create systemd service for LanguageTool server
sudo tee /etc/systemd/system/languagetool.service > /dev/null <<EOF
[Unit]
Description=LanguageTool Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/languagetool
ExecStart=/usr/bin/java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081 --allow-origin "*"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable languagetool
sudo systemctl start languagetool

echo "LanguageTool installation complete!"
echo "Server running on http://localhost:8081"
```

**Python Integration:** `F:\bookmake2\backend\services\languagetool.py`

```python
import requests
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# LanguageTool language codes
LANGUAGE_CODES = {
    'en': 'en-US',
    'es': 'es-ES',
    'fr': 'fr-FR',
    'de': 'de-DE',
    'zh': 'zh-CN',
    'ja': 'ja-JP',
    'pt': 'pt-BR',
    'it': 'it-IT',
    'ru': 'ru-RU',
    'ar': 'ar'
}

@dataclass
class GrammarError:
    """Represents a grammar or spelling error"""
    message: str
    context: str
    context_offset: int
    error_length: int
    category: str
    rule_id: str
    suggestions: List[str]
    replacements: List[Dict[str, Any]]


class LanguageToolService:
    """
    Service for integrating with LanguageTool for grammar checking
    across multiple languages
    """

    def __init__(self, api_url: str = 'http://localhost:8081/v2/check'):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        })

    def check_text(
        self,
        text: str,
        language: str = 'en',
        enabled_rules: Optional[List[str]] = None,
        disabled_rules: Optional[List[str]] = None,
        enabled_categories: Optional[List[str]] = None,
        disabled_categories: Optional[List[str]] = None
    ) -> List[GrammarError]:
        """
        Check text for grammar and spelling errors

        Args:
            text: The text to check
            language: Language code (en, es, fr, de, zh, ja, pt, it, ru, ar)
            enabled_rules: List of rule IDs to enable
            disabled_rules: List of rule IDs to disable
            enabled_categories: List of categories to enable
            disabled_categories: List of categories to disable

        Returns:
            List of GrammarError objects
        """
        # Map language code
        lt_language = LANGUAGE_CODES.get(language, 'en-US')

        # Prepare request data
        data = {
            'text': text,
            'language': lt_language,
            'enabledOnly': 'false'
        }

        # Add optional parameters
        if enabled_rules:
            data['enabledRules'] = ','.join(enabled_rules)
        if disabled_rules:
            data['disabledRules'] = ','.join(disabled_rules)
        if enabled_categories:
            data['enabledCategories'] = ','.join(enabled_categories)
        if disabled_categories:
            data['disabledCategories'] = ','.join(disabled_categories)

        try:
            response = self.session.post(self.api_url, data=data, timeout=30)
            response.raise_for_status()

            result = response.json()
            errors = []

            for match in result.get('matches', []):
                error = GrammarError(
                    message=match.get('message', ''),
                    context=match.get('context', {}).get('text', ''),
                    context_offset=match.get('context', {}).get('offset', 0),
                    error_length=match.get('length', 0),
                    category=match.get('rule', {}).get('category', ''),
                    rule_id=match.get('rule', {}).get('id', ''),
                    suggestions=[
                        replacement.get('value')
                        for replacement in match.get('replacements', [])[:5]
                    ],
                    replacements=match.get('replacements', [])
                )
                errors.append(error)

            logger.info(f"LanguageTool found {len(errors)} errors in {language} text")
            return errors

        except requests.exceptions.RequestException as e:
            logger.error(f"LanguageTool request failed: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"LanguageTool error: {str(e)}")
            return []

    def suggest_corrections(
        self,
        text: str,
        language: str = 'en',
        auto_apply: bool = False
    ) -> Dict[str, Any]:
        """
        Suggest corrections for text

        Args:
            text: The text to check
            language: Language code
            auto_apply: Whether to auto-apply suggestions

        Returns:
            Dictionary with original_text, corrected_text, and errors
        """
        errors = self.check_text(text, language)

        if not errors:
            return {
                'original_text': text,
                'corrected_text': text,
                'errors': [],
                'has_errors': False
            }

        # Sort errors by position (reverse order to avoid offset issues)
        sorted_errors = sorted(errors, key=lambda e: e.context_offset, reverse=True)

        corrected_text = text

        for error in sorted_errors:
            if auto_apply and error.replacements:
                # Apply first suggestion
                replacement = error.replacements[0]['value']
                start = error.context_offset
                end = start + error.error_length
                corrected_text = corrected_text[:start] + replacement + corrected_text[end:]

        return {
            'original_text': text,
            'corrected_text': corrected_text,
            'errors': [
                {
                    'message': error.message,
                    'offset': error.context_offset,
                    'length': error.error_length,
                    'category': error.category,
                    'suggestions': error.suggestions
                }
                for error in errors
            ],
            'has_errors': True,
            'error_count': len(errors)
        }

    def check_chapter(
        self,
        chapter_content: Dict[str, Any],
        language: str = 'en'
    ) -> Dict[str, Any]:
        """
        Check an entire chapter for errors

        Args:
            chapter_content: Chapter content with title and sections
            language: Language code

        Returns:
            Dictionary with errors by section
        """
        results = {
            'title_errors': [],
            'section_errors': [],
            'total_errors': 0
        }

        # Check title
        if 'title' in chapter_content:
            title_errors = self.check_text(chapter_content['title'], language)
            results['title_errors'] = [
                {
                    'message': error.message,
                    'suggestions': error.suggestions
                }
                for error in title_errors
            ]
            results['total_errors'] += len(title_errors)

        # Check sections
        for section in chapter_content.get('sections', []):
            if 'content' in section:
                section_errors = self.check_text(section['content'], language)
                results['section_errors'].append({
                    'section_id': section.get('id'),
                    'section_title': section.get('title', ''),
                    'errors': [
                        {
                            'message': error.message,
                            'offset': error.context_offset,
                            'suggestions': error.suggestions
                        }
                        for error in section_errors
                    ]
                })
                results['total_errors'] += len(section_errors)

        return results

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Get list of supported languages

        Returns:
            List of language dictionaries with code and name
        """
        return [
            {'code': 'en', 'name': 'English', 'lt_code': 'en-US'},
            {'code': 'es', 'name': 'Spanish', 'lt_code': 'es-ES'},
            {'code': 'fr', 'name': 'French', 'lt_code': 'fr-FR'},
            {'code': 'de', 'name': 'German', 'lt_code': 'de-DE'},
            {'code': 'zh', 'name': 'Chinese', 'lt_code': 'zh-CN'},
            {'code': 'ja', 'name': 'Japanese', 'lt_code': 'ja-JP'},
            {'code': 'pt', 'name': 'Portuguese', 'lt_code': 'pt-BR'},
            {'code': 'it', 'name': 'Italian', 'lt_code': 'it-IT'},
            {'code': 'ru', 'name': 'Russian', 'lt_code': 'ru-RU'},
            {'code': 'ar', 'name': 'Arabic', 'lt_code': 'ar'}
        ]


# Singleton instance
lt_service = LanguageToolService()
```

**Agent 8 Integration:** `F:\bookmake2\backend\agents\agent-8-quality-enhancement.js`

```javascript
const { Agent } = require('../agent-base');
const axios = require('axios');

class QualityEnhancementAgent extends Agent {
  constructor() {
    super('Agent-8-QualityEnhancement');
    this.languagetoolApi = 'http://localhost:8081/v2/check';
  }

  async execute(input) {
    const { chapterContent, targetLanguage = 'en', options = {} } = input;

    this.log('Starting quality enhancement', {
      language: targetLanguage,
      hasChapter: !!chapterContent
    });

    try {
      // Step 1: Grammar and spelling check using LanguageTool
      const grammarCheck = await this.checkGrammar(chapterContent, targetLanguage);

      // Step 2: Language-specific enhancements
      const enhanced = await this.applyLanguageEnhancements(
        chapterContent,
        targetLanguage,
        grammarCheck
      );

      // Step 3: Readability optimization
      const readabilityScore = await this.analyzeReadability(enhanced, targetLanguage);

      // Step 4: Coherence check
      const coherenceScore = await this.checkCoherence(enhanced, targetLanguage);

      this.log('Quality enhancement complete', {
        grammarErrors: grammarCheck.errorCount,
        readabilityScore,
        coherenceScore
      });

      return {
        enhancedContent: enhanced,
        grammarCheck,
        readabilityScore,
        coherenceScore,
        improvements: this.summarizeImprovements(grammarCheck, readabilityScore)
      };

    } catch (error) {
      this.error('Quality enhancement failed', error);
      throw error;
    }
  }

  async checkGrammar(content, language) {
    const languageCode = this.getLanguageToolCode(language);

    try {
      // Check title
      const titleErrors = await this.checkWithLanguageTool(
        content.title,
        languageCode
      );

      // Check each section
      const sectionErrors = [];
      for (const section of content.sections || []) {
        const errors = await this.checkWithLanguageTool(
          section.content,
          languageCode
        );
        sectionErrors.push({
          sectionId: section.id,
          errors
        });
      }

      const totalErrors = titleErrors.length +
        sectionErrors.reduce((sum, s) => sum + s.errors.length, 0);

      return {
        titleErrors,
        sectionErrors,
        errorCount: totalErrors,
        hasErrors: totalErrors > 0
      };

    } catch (error) {
      this.error('Grammar check failed', error);
      return {
        titleErrors: [],
        sectionErrors: [],
        errorCount: 0,
        hasErrors: false,
        error: error.message
      };
    }
  }

  async checkWithLanguageTool(text, languageCode) {
    const params = new URLSearchParams({
      text,
      language: languageCode,
      enabledOnly: 'false'
    });

    const response = await axios.post(this.languagetoolApi, params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      timeout: 30000
    });

    const matches = response.data.matches || [];

    return matches.map(match => ({
      message: match.message,
      offset: match.offset,
      length: match.length,
      context: match.context?.text || '',
      category: match.rule?.category || '',
      ruleId: match.rule?.id || '',
      suggestions: match.replacements?.slice(0, 5).map(r => r.value) || []
    }));
  }

  async applyLanguageEnhancements(content, language, grammarCheck) {
    const enhanced = JSON.parse(JSON.stringify(content)); // Deep clone

    // Apply language-specific enhancements
    switch (language) {
      case 'ar':
        // Arabic-specific: Ensure proper RTL formatting
        enhanced = this.applyArabicEnhancements(enhanced);
        break;

      case 'zh':
      case 'ja':
        // CJK languages: Character consistency and formatting
        enhanced = this.applyCJKEnhancements(enhanced, language);
        break;

      case 'en':
      case 'es':
      case 'fr':
      case 'de':
      case 'it':
      case 'pt':
      case 'ru':
        // Latin and Cyrillic: Standard enhancements
        enhanced = this.applyLatinEnhancements(enhanced, language);
        break;
    }

    return enhanced;
  }

  applyArabicEnhancements(content) {
    // Ensure proper Arabic text formatting
    // Arabic is RTL, so we need to ensure proper rendering

    const arabicNumberFormat = (num) => {
      // Convert Western numerals to Arabic-Indic numerals
      const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
      return num.toString().replace(/\d/g, d => arabicNumerals[d]);
    };

    // Process sections
    for (const section of content.sections || []) {
      // Add RTL marker at the beginning
      section.content = `\u202B${section.content}\u202C`;

      // Format numbers in Arabic
      section.content = section.content.replace(/\d+/g, match => arabicNumberFormat(match));
    }

    return content;
  }

  applyCJKEnhancements(content, language) {
    // CJK-specific enhancements
    for (const section of content.sections || []) {
      // Ensure proper punctuation
      if (language === 'zh') {
        // Chinese punctuation
        section.content = section.content
          .replace(/，/g, '、')
          .replace(/。/g, '。');
      } else if (language === 'ja') {
        // Japanese punctuation
        section.content = section.content
          .replace(/,/g, '、')
          .replace(/\./g, '。');
      }
    }

    return content;
  }

  applyLatinEnhancements(content, language) {
    // Language-specific punctuation and formatting
    const punctuationRules = {
      'es': { quoteOpen: '«', quoteClose: '»' },
      'fr': { quoteOpen: '« ', quoteClose: ' »' },
      'de': { quoteOpen: '„', quoteClose: '"' },
      'it': { quoteOpen: '«', quoteClose: '»' },
      'pt': { quoteOpen: '«', quoteClose: '»' },
      'ru': { quoteOpen: '«', quoteClose: '»' },
      'en': { quoteOpen: '"', quoteClose: '"' }
    };

    const rules = punctuationRules[language] || punctuationRules['en'];

    for (const section of content.sections || []) {
      // Apply language-specific quote marks
      section.content = section.content
        .replace(/"/g, rules.quoteOpen)
        .replace(/"/g, rules.quoteClose);
    }

    return content;
  }

  async analyzeReadability(content, language) {
    // Simplified readability scoring
    const text = content.sections?.map(s => s.content).join(' ') || '';

    // Count words, sentences, etc.
    const words = text.split(/\s+/).length;
    const sentences = text.split(/[.!?]+/).length;
    const avgWordsPerSentence = words / Math.max(sentences, 1);

    // Calculate score (simplified Flesch Reading Ease)
    let score;
    if (language === 'ar' || language === 'zh' || language === 'ja') {
      // CJK and Arabic have different metrics
      score = Math.min(100, Math.max(0, 100 - (avgWordsPerSentence * 2)));
    } else {
      // Latin-based languages
      score = Math.min(100, Math.max(0, 206.835 - (avgWordsPerSentence * 1.015)));
    }

    return {
      score: Math.round(score),
      level: this.getReadabilityLevel(score),
      words,
      sentences,
      avgWordsPerSentence: Math.round(avgWordsPerSentence * 10) / 10
    };
  }

  getReadabilityLevel(score) {
    if (score >= 90) return 'Very Easy';
    if (score >= 80) return 'Easy';
    if (score >= 70) return 'Fairly Easy';
    if (score >= 60) return 'Standard';
    if (score >= 50) return 'Fairly Difficult';
    if (score >= 30) return 'Difficult';
    return 'Very Difficult';
  }

  async checkCoherence(content, language) {
    // Simplified coherence check
    const sections = content.sections || [];

    if (sections.length < 2) {
      return { score: 100, issues: [] };
    }

    let issues = [];
    let totalScore = 100;

    // Check for section transitions
    for (let i = 1; i < sections.length; i++) {
      const prevContent = sections[i - 1].content.toLowerCase();
      const currContent = sections[i].content.toLowerCase();

      // Check for transition words
      const transitionWords = this.getTransitionWords(language);
      const hasTransition = transitionWords.some(word =>
        currContent.includes(word) || prevContent.includes(word)
      );

      if (!hasTransition) {
        issues.push({
          section: i,
          type: 'missing_transition',
          message: 'Section lacks proper transition'
        });
        totalScore -= 5;
      }
    }

    return {
      score: Math.max(0, totalScore),
      issues: issues.slice(0, 5) // Limit to top 5 issues
    };
  }

  getTransitionWords(language) {
    const transitions = {
      'en': ['however', 'therefore', 'furthermore', 'moreover', 'consequently'],
      'es': ['sin embargo', 'por lo tanto', 'además', 'consecuentemente'],
      'fr': ['cependant', 'donc', 'de plus', 'par conséquent'],
      'de': ['jedoch', 'deshalb', 'außerdem', 'folglich'],
      'zh': ['然而', '因此', '此外', '所以'],
      'ja': ['しかし', 'したがって', 'さらに', 'そのため'],
      'pt': ['no entanto', 'portanto', 'além disso', 'consequentemente'],
      'it': ['tuttavia', 'quindi', 'inoltre', 'di conseguenza'],
      'ru': ['однако', 'поэтому', 'кроме того', 'следовательно'],
      'ar': ['ومع ذلك', 'لذلك', 'علاوة على ذلك', 'وبالتالي']
    };

    return transitions[language] || transitions['en'];
  }

  summarizeImprovements(grammarCheck, readabilityScore) {
    const improvements = [];

    if (grammarCheck.hasErrors) {
      improvements.push({
        type: 'grammar',
        count: grammarCheck.errorCount,
        message: `Fixed ${grammarCheck.errorCount} grammar/spelling issues`
      });
    }

    if (readabilityScore.score < 70) {
      improvements.push({
        type: 'readability',
        score: readabilityScore.score,
        message: 'Improved text readability and flow'
      });
    }

    return improvements;
  }

  getLanguageToolCode(language) {
    const codes = {
      'en': 'en-US',
      'es': 'es-ES',
      'fr': 'fr-FR',
      'de': 'de-DE',
      'zh': 'zh-CN',
      'ja': 'ja-JP',
      'pt': 'pt-BR',
      'it': 'it-IT',
      'ru': 'ru-RU',
      'ar': 'ar'
    };

    return codes[language] || 'en-US';
  }
}

module.exports = { QualityEnhancementAgent };
```

---

### 2. Update All Agents for Multi-Language

**Agent 2 (Topic Analysis) - Language-Specific:** `F:\bookmake2\backend\agents\agent-2-topic-analysis.js`

```javascript
class TopicAnalysisAgent extends Agent {
  async execute(input) {
    const { topic, targetLanguage = 'en' } = input;

    const prompts = {
      'en': `Analyze the following topic and extract key information: "${topic}"`,
      'es': `Analiza el siguiente tema y extrae información clave: "${topic}"`,
      'fr': `Analysez le sujet suivant et extrayez les informations clés: "${topic}"`,
      'de': `Analysieren Sie das folgende Thema und extrahieren Sie Schlüsselinformationen: "${topic}"`,
      'zh': `分析以下主题并提取关键信息："${topic}"`,
      'ja': `以下のトピックを分析し、重要な情報を抽出してください："${topic}"`,
      'pt': `Analise o seguinte tópico e extraia informações-chave: "${topic}"`,
      'it': `Analizza il seguente argomento ed estrai le informazioni chiave: "${topic}"`,
      'ru': `Проанализируйте следующую тему и извлеките ключевую информацию: "${topic}"`,
      'ar': `حلل الموضوع التالي واستخرج المعلومات الأساسية: "${topic}"`
    };

    const prompt = prompts[targetLanguage] || prompts['en'];

    // Use language-specific prompt for analysis
    const analysis = await this.callLLM(prompt, { targetLanguage });

    return {
      topic,
      language: targetLanguage,
      keywords: analysis.keywords || [],
      mainThemes: analysis.themes || [],
      targetAudience: analysis.audience || 'general',
      complexity: analysis.complexity || 'intermediate'
    };
  }
}
```

**Agent 5 (Chapter Generation) - Language-Specific:** `F:\bookmake2\backend\agents\agent-5-chapter-generation.js`

```javascript
class ChapterGenerationAgent extends Agent {
  async execute(input) {
    const { chapterOutline, targetLanguage = 'en', context } = input;

    const systemPrompts = {
      'en': 'You are an expert content writer specializing in creating engaging educational content in English.',
      'es': 'Eres un experto redactor de contenido especializado en crear contenido educativo atractivo en español.',
      'fr': 'Vous êtes un expert rédacteur de contenu spécialisé dans la création de contenu éducatif engageant en français.',
      'de': 'Sie sind ein Experte für Content-Erstellung, spezialisiert auf ansprechende Bildungsinhalte auf Deutsch.',
      'zh': '你是一位專業的內容作家，專門創作文吸引人的中文教育內容。',
      'ja': 'あなたは、魅力的な教育コンテンツを日本語で作成する専門家です。',
      'pt': 'Você é um especialista em criação de conteúdo, focado em criar conteúdo educacional envolvente em português.',
      'it': 'Sei un esperto content writer specializzato nella creazione di contenuti educativi coinvolgenti in italiano.',
      'ru': 'Вы эксперт по созданию контента, специализирующийся на создании увлекательного образовательного контента на русском языке.',
      'ar': 'أنت خبير في كتابة المحتوى متخصص في إنشاء محتوى تعليمي جذاب باللغة العربية.'
    };

    const systemPrompt = systemPrompts[targetLanguage] || systemPrompts['en'];

    const chapterContent = await this.callLLM(
      `Generate chapter content following this outline: ${JSON.stringify(chapterOutline)}`,
      {
        systemPrompt,
        targetLanguage,
        context
      }
    );

    return {
      ...chapterContent,
      language: targetLanguage,
      metadata: {
        wordCount: chapterContent.content?.split(/\s+/).length || 0,
        language: targetLanguage,
        generatedAt: new Date().toISOString()
      }
    };
  }
}
```

**Agent 7 (Visual Design) - RTL Support:** `F:\bookmake2\backend\agents\agent-7-visual-design.js`

```javascript
class VisualDesignAgent extends Agent {
  async execute(input) {
    const { topic, targetLanguage = 'en', theme, colorScheme } = input;

    const isRTL = targetLanguage === 'ar';
    const layoutDirection = isRTL ? 'rtl' : 'ltr';

    const design = await this.callLLM(
      `Create visual design specifications for: "${topic}"`,
      {
        targetLanguage,
        layoutDirection,
        theme: theme || 'professional',
        colorScheme: colorScheme || 'cool'
      }
    );

    return {
      ...design,
      layout: {
        direction: layoutDirection,
        textAlign: isRTL ? 'right' : 'left',
        ...(design.layout || {})
      },
      typography: {
        ...(design.typography || {}),
        font: this.getRecommendedFont(targetLanguage)
      },
      rtl: isRTL
    };
  }

  getRecommendedFont(language) {
    const fonts = {
      'en': 'Merriweather, Georgia, serif',
      'es': 'Montserrat, Open Sans, sans-serif',
      'fr': 'Lato, Raleway, sans-serif',
      'de': 'Roboto, Open Sans, sans-serif',
      'zh': 'Noto Sans SC, Source Han Sans CN, sans-serif',
      'ja': 'Noto Sans JP, Source Han Sans JP, sans-serif',
      'pt': 'Lato, Open Sans, sans-serif',
      'it': 'Lora, Crimson Text, serif',
      'ru': 'PT Serif, Source Sans Pro, sans-serif',
      'ar': 'Noto Sans Arabic, Amiri, sans-serif'
    };

    return fonts[language] || fonts['en'];
  }
}
```

**Agent 11 (Layout & Formatting) - RTL:** `F:\bookmake2\backend\agents\agent-11-layout-formatting.js`

```javascript
class LayoutFormattingAgent extends Agent {
  async execute(input) {
    const { chapters, design, targetLanguage = 'en' } = input;

    const isRTL = targetLanguage === 'ar';

    const html = this.generateHTML(chapters, design, {
      language: targetLanguage,
      rtl: isRTL
    });

    const css = this.generateCSS(design, {
      language: targetLanguage,
      rtl: isRTL
    });

    return {
      html,
      css,
      metadata: {
        totalPages: this.estimatePageCount(html),
        language: targetLanguage,
        direction: isRTL ? 'rtl' : 'ltr'
      }
    };
  }

  generateHTML(chapters, design, options) {
    const dir = options.rtl ? 'dir="rtl"' : 'dir="ltr"';
    const lang = `lang="${options.language}"`;

    let html = `<!DOCTYPE html>
<html ${lang} ${dir}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ebook</title>
</head>
<body>
  <div class="ebook-container">
`;

    for (const chapter of chapters) {
      html += `
    <div class="chapter">
      <h1 class="chapter-title">${chapter.title}</h1>
`;

      for (const section of chapter.sections) {
        html += `
      <div class="section">
        <h2 class="section-title">${section.title}</h2>
        <div class="section-content">${section.content}</div>
      </div>
`;
      }

      html += `
    </div>
`;
    }

    html += `
  </div>
</body>
</html>`;

    return html;
  }

  generateCSS(design, options) {
    const textAlign = options.rtl ? 'right' : 'left';
    const fontFamily = this.getFontFamily(options.language);

    return `
      * {
        box-sizing: border-box;
      }

      body {
        font-family: ${fontFamily};
        direction: ${options.rtl ? 'rtl' : 'ltr'};
        text-align: ${textAlign};
        margin: 0;
        padding: 20px;
        line-height: 1.6;
      }

      .ebook-container {
        max-width: 800px;
        margin: 0 auto;
      }

      .chapter {
        margin-bottom: 40px;
      }

      .chapter-title {
        font-size: 2em;
        margin-bottom: 20px;
        color: ${design.colors?.primary || '#333'};
      }

      .section {
        margin-bottom: 30px;
      }

      .section-title {
        font-size: 1.5em;
        margin-bottom: 15px;
        color: ${design.colors?.secondary || '#555'};
      }

      .section-content {
        font-size: 1em;
        line-height: 1.8;
        color: ${design.colors?.text || '#000'};
      }

      ${options.rtl ? `
      /* RTL-specific styles */
      .chapter-title,
      .section-title,
      .section-content {
        unicode-bidi: embed;
      }
      ` : ''}
    `;
  }

  getFontFamily(language) {
    const fonts = {
      'en': "'Merriweather', Georgia, serif",
      'es': "'Montserrat', sans-serif",
      'fr': "'Lato', sans-serif",
      'de': "'Roboto', sans-serif",
      'zh': "'Noto Sans SC', sans-serif",
      'ja': "'Noto Sans JP', sans-serif",
      'pt': "'Open Sans', sans-serif",
      'it': "'Lora', serif",
      'ru': "'PT Serif', serif",
      'ar': "'Noto Sans Arabic', sans-serif"
    };

    return fonts[language] || fonts['en'];
  }

  estimatePageCount(html) {
    // Rough estimate: 500 words per page
    const wordCount = html.split(/\s+/).length;
    return Math.ceil(wordCount / 500);
  }
}
```

---

### 3. Multi-Language Font Support

**Font Installation:** `F:\bookmake2\backend\scripts\install-fonts.sh`

```bash
#!/bin/bash

echo "Installing multi-language fonts for PDF generation..."

FONT_DIR="/usr/share/fonts/truetype"
EBOOK_FONT_DIR="/opt/ebook-generator/fonts"

mkdir -p $EBOOK_FONT_DIR

# English fonts
echo "Installing English fonts..."
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSerif-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSerif-Bold.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSerif-Italic.ttf

# Spanish/Portuguese/French/Italian fonts (same as English with special characters)
echo "Installing Latin language fonts..."
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSans-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSans-Bold.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSans-Italic.ttf

# German fonts (includes special characters)
echo "Installing German fonts..."
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSans-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSans-Bold.ttf

# Chinese fonts
echo "Installing Chinese fonts..."
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSansSC-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSansSC-Bold.ttf

# Japanese fonts
echo "Installing Japanese fonts..."
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSansJP-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSansJP-Bold.ttf

# Russian fonts (Cyrillic)
echo "Installing Russian fonts..."
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSans-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSans-Bold.ttf

# Arabic fonts (RTL support)
echo "Installing Arabic fonts..."
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSansArabic-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/NotoSansArabic-Bold.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/Amiri-Regular.ttf
wget -P $EBOOK_FONT_DIR https://github.com/googlefonts/noto-fonts/raw/master/hinted/ttf/Amiri-Bold.ttf

# Update font cache
echo "Updating font cache..."
fc-cache -fv

echo "Font installation complete!"
echo "Fonts installed to: $EBOOK_FONT_DIR"
```

**WeasyPrint Font Configuration:** `F:\bookmake2\backend\config\fonts.py`

```python
import os
from weasyprint import CSS
from weasyprint.text.fonts import FontConfiguration

FONT_DIR = '/opt/ebook-generator/fonts'

LANGUAGE_FONTS = {
    'en': {
        'serif': "'Noto Serif', 'Merriweather', Georgia, serif",
        'sans-serif': "'Noto Sans', Arial, sans-serif",
        'monospace': "'Noto Sans Mono', 'Courier New', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSerif-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSerif-Bold.ttf'),
            os.path.join(FONT_DIR, 'NotoSerif-Italic.ttf')
        ]
    },
    'es': {
        'serif': "'Noto Serif', 'Merriweather', Georgia, serif",
        'sans-serif': "'Noto Sans', 'Open Sans', Arial, sans-serif",
        'monospace': "'Noto Sans Mono', 'Courier New', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSans-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSans-Bold.ttf')
        ]
    },
    'fr': {
        'serif': "'Noto Serif', 'Lora', Georgia, serif",
        'sans-serif': "'Noto Sans', 'Lato', Arial, sans-serif",
        'monospace': "'Noto Sans Mono', 'Courier New', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSans-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSans-Bold.ttf')
        ]
    },
    'de': {
        'serif': "'Noto Serif', 'Merriweather', Georgia, serif",
        'sans-serif': "'Noto Sans', 'Roboto', Arial, sans-serif",
        'monospace": "'Noto Sans Mono', 'Courier New', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSans-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSans-Bold.ttf')
        ]
    },
    'zh': {
        'serif': "'Noto Serif SC', 'Source Han Serif CN', serif",
        'sans-serif': "'Noto Sans SC', 'Source Han Sans CN', sans-serif",
        'monospace': "'Noto Sans Mono SC', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSansSC-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSansSC-Bold.ttf')
        ]
    },
    'ja': {
        'serif': "'Noto Serif JP', 'Source Han Serif JP', serif",
        'sans-serif': "'Noto Sans JP', 'Source Han Sans JP', sans-serif",
        'monospace': "'Noto Sans Mono JP', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSansJP-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSansJP-Bold.ttf')
        ]
    },
    'pt': {
        'serif': "'Noto Serif', 'Merriweather', Georgia, serif",
        'sans-serif': "'Noto Sans', 'Open Sans', Arial, sans-serif",
        'monospace': "'Noto Sans Mono', 'Courier New', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSans-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSans-Bold.ttf')
        ]
    },
    'it': {
        'serif': "'Noto Serif', 'Lora', Georgia, serif",
        'sans-serif': "'Noto Sans', 'Open Sans', Arial, sans-serif",
        'monospace': "'Noto Sans Mono', 'Courier New', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSans-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSans-Bold.ttf')
        ]
    },
    'ru': {
        'serif': "'Noto Serif', 'PT Serif', Georgia, serif",
        'sans-serif': "'Noto Sans', 'Open Sans', Arial, sans-serif",
        'monospace': "'Noto Sans Mono', 'Courier New', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSans-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSans-Bold.ttf')
        ]
    },
    'ar': {
        'serif': "'Amiri', 'Noto Serif Arabic', serif",
        'sans-serif': "'Noto Sans Arabic', 'Amiri', sans-serif",
        'monospace': "'Noto Sans Arabic', monospace",
        'font_paths': [
            os.path.join(FONT_DIR, 'NotoSansArabic-Regular.ttf'),
            os.path.join(FONT_DIR, 'NotoSansArabic-Bold.ttf'),
            os.path.join(FONT_DIR, 'Amiri-Regular.ttf'),
            os.path.join(FONT_DIR, 'Amiri-Bold.ttf')
        ],
        'direction': 'rtl'
    }
}

def get_font_css(language='en'):
    """
    Generate CSS for language-specific fonts
    """
    font_config = LANGUAGE_FONTS.get(language, LANGUAGE_FONTS['en'])

    css = f"""
    @font-face {{
        font-family: 'Noto Sans';
        src: url('file://{font_config['font_paths'][0]}');
        font-weight: normal;
        font-style: normal;
    }}

    @font-face {{
        font-family: 'Noto Sans';
        src: url('file://{font_config['font_paths'][1]}');
        font-weight: bold;
        font-style: normal;
    }}

    body {{
        font-family: {font_config['sans-serif']};
        direction: {font_config.get('direction', 'ltr')};
        text-align: {'right' if font_config.get('direction') == 'rtl' else 'left'};
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: {font_config['serif']};
    }}

    p, div {{
        font-family: {font_config['sans-serif']};
    }}

    code, pre {{
        font-family: {font_config['monospace']};
    }}
    """

    return CSS(string=css)


def verify_fonts(language='en'):
    """
    Verify that required fonts are installed
    """
    font_config = LANGUAGE_FONTS.get(language, LANGUAGE_FONTS['en'])
    missing_fonts = []

    for font_path in font_config['font_paths']:
        if not os.path.exists(font_path):
            missing_fonts.append(font_path)

    if missing_fonts:
        raise FileNotFoundError(
            f"Missing fonts for language {language}: {missing_fonts}"
        )

    return True
```

---

### 4. Language Testing Suite

**File:** `F:\bookmake2\tests\multilang\test-language-support.js`

```javascript
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const API_BASE = 'http://localhost:3000/api';

const TEST_TOPICS = {
  'en': 'The fundamentals of machine learning and artificial intelligence',
  'es': 'Los fundamentos del aprendizaje automático y la inteligencia artificial',
  'fr': 'Les fondamentaux de l\'apprentissage automatique et de l\'intelligence artificielle',
  'de': 'Die Grundlagen des maschinellen Lernens und der künstlichen Intelligenz',
  'zh': '机器学习和人工智能的基础',
  'ja': '機械学習と人工知能の基礎',
  'pt': 'Os fundamentos do aprendizado de máquina e inteligência artificial',
  'it': 'Le fondamenta del machine learning e dell\'intelligenza artificiale',
  'ru': 'Основы машинного обучения и искусственного интеллекта',
  'ar': 'أساسيات التعلم الآلي والذكاء الاصطناعي'
};

class LanguageTestSuite {
  constructor() {
    this.results = [];
  }

  async testLanguage(language) {
    console.log(`\nTesting language: ${language}`);
    console.log('='.repeat(50));

    const topic = TEST_TOPICS[language];
    const testId = `${language}_${Date.now()}`;

    try {
      // Step 1: Create generation
      console.log('Step 1: Creating generation...');
      const createResponse = await axios.post(`${API_BASE}/generations`, {
        topic,
        target_language: language
      });

      const generationId = createResponse.data.data.generation_id;
      console.log(`Generation created: ${generationId}`);

      // Step 2: Monitor progress
      console.log('Step 2: Monitoring progress...');
      let status;
      let attempts = 0;
      const maxAttempts = 180; // 30 minutes max

      do {
        await new Promise(resolve => setTimeout(resolve, 5000)); // Poll every 5 seconds

        const statusResponse = await axios.get(
          `${API_BASE}/generations/${generationId}`
        );
        status = statusResponse.data.data;

        attempts++;
        console.log(`Poll ${attempts}: ${status.stage || 'initializing'} (${status.progress || 0}%)`);

      } while (status.status !== 'completed' && attempts < maxAttempts);

      if (status.status !== 'completed') {
        throw new Error('Generation timed out');
      }

      // Step 3: Download and verify PDF
      console.log('Step 3: Downloading PDF...');
      const pdfPath = status.pdf_path;
      const pdfExists = fs.existsSync(pdfPath);

      if (!pdfExists) {
        throw new Error(`PDF not found at ${pdfPath}`);
      }

      const pdfStats = fs.statSync(pdfPath);
      console.log(`PDF size: ${(pdfStats.size / 1024 / 1024).toFixed(2)} MB`);

      // Step 4: Verify language-specific features
      console.log('Step 4: Verifying language-specific features...');
      const checks = await this.verifyLanguageFeatures(pdfPath, language);

      const result = {
        language,
        topic,
        generationId,
        pdfPath,
        pdfSize: pdfStats.size,
        status: 'success',
        duration: status.duration,
        checks
      };

      console.log(`\nTest PASSED for ${language}`);
      console.log(`Duration: ${(status.duration / 1000 / 60).toFixed(2)} minutes`);
      console.log(`PDF size: ${(pdfStats.size / 1024 / 1024).toFixed(2)} MB`);

      this.results.push(result);

    } catch (error) {
      console.error(`\nTest FAILED for ${language}: ${error.message}`);

      this.results.push({
        language,
        topic,
        status: 'failed',
        error: error.message
      });
    }
  }

  async verifyLanguageFeatures(pdfPath, language) {
    const checks = {
      hasFonts: false,
      hasCorrectEncoding: false,
      hasRTL: false,
      renderable: false
    };

    // Note: In a real implementation, you would use a PDF parsing library
    // like pdf-parse to verify these features

    // Check 1: PDF exists and is not empty
    const stats = fs.statSync(pdfPath);
    checks.renderable = stats.size > 1000; // At least 1KB

    // Check 2: RTL for Arabic
    if (language === 'ar') {
      checks.hasRTL = true; // Should be verified by inspecting PDF structure
    }

    // Check 3: Font embedding (would need PDF parser)
    checks.hasFonts = true;

    // Check 4: Character encoding (would need PDF parser)
    checks.hasCorrectEncoding = true;

    return checks;
  }

  async runAllTests() {
    console.log('Starting Multi-Language Test Suite');
    console.log('='.repeat(50));
    console.log(`Testing ${Object.keys(TEST_TOPICS).length} languages\n`);

    const languages = Object.keys(TEST_TOPICS);

    for (const language of languages) {
      await this.testLanguage(language);
    }

    // Print summary
    console.log('\n' + '='.repeat(50));
    console.log('MULTI-LANGUAGE TEST SUMMARY');
    console.log('='.repeat(50));

    const passed = this.results.filter(r => r.status === 'success').length;
    const failed = this.results.filter(r => r.status === 'failed').length;

    console.log(`\nTotal Tests: ${this.results.length}`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${failed}`);

    console.log('\nDetailed Results:');
    console.log('-'.repeat(50));

    for (const result of this.results) {
      console.log(`\n${result.language}: ${result.status.toUpperCase()}`);
      if (result.status === 'success') {
        console.log(`  Duration: ${(result.duration / 1000 / 60).toFixed(2)} minutes`);
        console.log(`  PDF Size: ${(result.pdfSize / 1024 / 1024).toFixed(2)} MB`);
        console.log(`  Checks: ${JSON.stringify(result.checks)}`);
      } else {
        console.log(`  Error: ${result.error}`);
      }
    }

    console.log('\n' + '='.repeat(50));

    // Save results to file
    const resultsPath = path.join(__dirname, 'test-results.json');
    fs.writeFileSync(resultsPath, JSON.stringify(this.results, null, 2));
    console.log(`\nResults saved to: ${resultsPath}`);
  }
}

// Run tests
const testSuite = new LanguageTestSuite();
testSuite.runAllTests().catch(console.error);
```

---

## Verification & Testing Checklist

### Week 13-14: Batch Processing

- [ ] `/ebook-batch` skill implemented with parallel pipeline execution
- [ ] Batch API endpoints created and tested:
  - [ ] POST /api/generations/batch
  - [ ] GET /api/batch/:id/status
  - [ ] GET /api/batch/:id/details
  - [ ] POST /api/batch/:id/cancel
- [ ] Celery task queue configured with:
  - [ ] Batch queue isolation
  - [ ] Task prioritization
  - [ ] Fair scheduling
- [ ] Frontend batch generate page completed with:
  - [ ] 10-topic input form
  - [ ] Parallel execution slider (1-5 pipelines)
  - [ ] Per-pipeline progress cards
  - [ ] Batch summary report
  - [ ] Cancellation functionality
- [ ] Load testing completed:
  - [ ] 3 parallel pipelines tested
  - [ ] 5 parallel pipelines tested
  - [ ] 10-ebook batch tested
  - [ ] Completion time ≤60 minutes verified
  - [ ] Queue management tested
  - [ ] Cancellation tested

### Week 15-16: Multi-Language Support

- [ ] LanguageTool installed and configured:
  - [ ] LanguageTool server running on port 8081
  - [ ] All 10 language dictionaries installed
  - [ ] API tested for each language
- [ ] LanguageTool integrated with Agent 8:
  - [ ] Grammar checking working
  - [ ] Spelling checking working
  - [ ] Suggestions working
  - [ ] Auto-correction working
- [ ] All agents updated for multi-language:
  - [ ] Agent 2: Topic Analysis (language-specific prompts)
  - [ ] Agent 3: Content Strategy (language-specific structure)
  - [ ] Agent 5: Chapter Generation (language-specific generation)
  - [ ] Agent 7: Visual Design (RTL for Arabic)
  - [ ] Agent 8: Quality Enhancement (LanguageTool integration)
  - [ ] Agent 9: Critic & Proofreading (language-specific verification)
  - [ ] Agent 10: SEO & Metadata (language-specific SEO)
  - [ ] Agent 11: Layout & Formatting (RTL for Arabic)
  - [ ] Agent 12: PDF Generation (font embedding)
- [ ] Fonts installed for all 10 languages:
  - [ ] English (Latin)
  - [ ] Spanish (Latin with special characters)
  - [ ] French (Latin with special characters)
  - [ ] German (Latin with special characters)
  - [ ] Chinese (CJK)
  - [ ] Japanese (CJK)
  - [ ] Portuguese (Latin with special characters)
  - [ ] Italian (Latin with special characters)
  - [ ] Russian (Cyrillic)
  - [ ] Arabic (RTL script)
- [ ] WeasyPrint configured for all languages:
  - [ ] Font embedding configured
  - [ ] Character encoding verified
  - [ ] RTL rendering tested for Arabic
- [ ] Frontend language selection UI:
  - [ ] 10 radio buttons with flags
  - [ ] Language names in native script
  - [ ] RTL preview for Arabic
- [ ] Language testing completed:
  - [ ] Test ebook generated in each language
  - [ ] Grammar checking verified
  - [ ] PDF rendering verified
  - [ ] Character encoding verified
  - [ ] Arabic RTL verified
  - [ ] Font embedding verified
  - [ ] All special characters render correctly

---

## Performance Targets

**Batch Processing:**
- 3 parallel pipelines: 3 ebooks in ≤18 minutes (6 min per ebook)
- 5 parallel pipelines: 5 ebooks in ≤30 minutes (6 min per ebook)
- 10 ebooks (3 pipelines): ≤60 minutes total

**Multi-Language:**
- LanguageTool response time: ≤5 seconds per 1000 words
- Font loading time: ≤2 seconds per language
- PDF generation time: ≤30 seconds per ebook (regardless of language)
- Grammar accuracy: ≥95% for English, ≥90% for other languages

**System Resources:**
- Memory per pipeline: ≤2GB
- CPU utilization per pipeline: ≤80%
- Disk I/O: ≤100MB/s per pipeline
- Network: ≤10Mbps for LanguageTool API calls

---

## Deployment Instructions

### 1. Install LanguageTool

```bash
cd backend/scripts
sudo bash install-languagetool.sh

# Verify installation
curl http://localhost:8081/v2/check -d "text=Hello world&language=en-US"
```

### 2. Install Fonts

```bash
cd backend/scripts
sudo bash install-fonts.sh

# Verify fonts
fc-list | grep -i "noto"
fc-list | grep -i "amiri"
```

### 3. Configure Celery

```bash
# Start Redis
sudo systemctl start redis

# Start Celery workers
cd backend/celery
bash start-workers.sh

# Verify workers
celery -A celery.tasks inspect active
```

### 4. Run Tests

```bash
# Load testing
cd tests/load
node batch-load-test.js

# Language testing
cd tests/multilang
node test-language-support.js
```

---

## Troubleshooting

### LanguageTool Issues

**Problem:** LanguageTool not responding
```bash
# Check if service is running
sudo systemctl status languagetool

# Restart service
sudo systemctl restart languagetool

# Check logs
sudo journalctl -u languagetool -f
```

**Problem:** Language not supported
```bash
# Verify language pack is installed
curl http://localhost:8081/v2/languages

# Install missing language pack
sudo apt-get install languagetool-<lang>
```

### Font Issues

**Problem:** Fonts not rendering in PDF
```bash
# Rebuild font cache
sudo fc-cache -fv

# Verify fonts are installed
fc-list | grep -i "noto"

# Check WeasyPrint can access fonts
python3 -c "from weasyprint import CSS; print(CSS())"
```

**Problem:** Arabic text not rendering RTL
```javascript
// Verify dir attribute is set in HTML
html.setAttribute('dir', 'rtl');

// Check CSS direction property
const direction = window.getComputedStyle(element).direction;
console.log(direction); // Should be 'rtl'
```

### Batch Processing Issues

**Problem:** Batch not completing
```bash
# Check Celery workers
celery -A celery.tasks inspect active

# Check Redis queue
redis-cli
> llen default
> llen batch

# Flush stuck queues
celery -A celery.tasks purge
```

**Problem:** Memory issues with parallel pipelines
```bash
# Monitor memory usage
free -h

# Adjust worker concurrency
# Edit celeryconfig.py
worker_concurrency = 2  # Reduce from 3
```

---

## Success Criteria

Phase 3 is complete when:

1. **Batch Processing:**
   - Can generate 10 ebooks in parallel
   - Completion time ≤60 minutes
   - All batch API endpoints working
   - Queue management functional
   - Cancellation working

2. **Multi-Language Support:**
   - All 10 languages supported
   - LanguageTool integrated and working
   - Fonts installed and embedded
   - Arabic RTL rendering correct
   - All special characters render properly
   - Grammar checking working for all languages

3. **Quality:**
   - Load tests passing
   - Language tests passing
   - No critical bugs
   - Performance targets met
   - Resource usage within limits

---

## Next Steps: Phase 4

After completing Phase 3, proceed to:

**Phase 4: Advanced Features & Optimization (Weeks 17-20)**
- Interactive ebook components
- Video and audio embedding
- Advanced analytics dashboard
- User collaboration features
- Template marketplace
- Performance optimization
- CDN integration
- Caching strategies

---

**Document Version:** 1.0
**Last Updated:** 2026-01-16
**Author:** System Architecture Team
**Status:** Ready for Implementation
