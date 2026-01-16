# Testing & Verification Strategy (Automated)

## 🧪 Automated Test Suites (Zero-Manual Intervention)

The system is designed to be verified through automated suites that agents can run autonomously.

### 1. Backend Service Tests (Pytest)
- **Unit Tests**: Mocks for all 13 agents to verify JSON input/output integrity.
- **Integration Tests**: 
  - `test_agent_orchestrator`: Verifies the state machine transitions.
  - `test_storage_sync`: Verifies MinIO and GDrive upload status via API mocks.
- **Command**: `docker-compose exec backend pytest`

### 2. Frontend E2E Tests (Playwright/Cypress)
- **Headless Mode**: All UI tests must run headlessly for agent compatibility.
- **Automated Scenarios**:
  - `test_zero_interaction_flow`: Submits a topic and polls until success.
  - `test_neo_brutalist_responsive`: Visual regression testing for layout breaks.
  - `test_rtl_rendering`: verifies text direction for 'ar' config codes.
- **Command**: `npm run test:e2e`

### 3. Visual Infrastructure Verification
- **PixelMatch/Snapshotting**: Automates the check for "vibrant colors" and "bold borders" by comparing against baseline design snapshots.

## 🚢 Local Automated Deployment
A `health_check.sh` script is provided to verify the local environment after deployment:
1. Pings FastAPI `/health`.
2. Verifies Redis connection.
3. Checks Ollama model availability (`ollama list`).
4. Verifies MinIO bucket existence.

## ⏱️ Automated Performance Benchmarks
- **Pipeline Latency**: Automated log analysis to verify:
  - Topic Analysis < 30s.
  - Infographic Generation < 3min per chapter.
  - Total Pipeline < 15min.

