# Crop Care Crop — Backend (REST API v1)

FastAPI backend for **Crop Care Crop**, an AI-powered crop disease detection
and recommendation system (final-year project).

## Status of this milestone

| Feature | Status |
|---|---|
| `GET /api/v1/health` | ✅ Working |
| `POST /api/v1/predictions` (image upload) | ✅ Working — validates, stores image, returns prediction request id |
| `GET /api/v1/predictions/{id}` | ✅ Working — returns lifecycle status (`crop/disease/confidence` stay `null` until the model is connected) |
| `GET /api/v1/diseases/{name}` | ✅ Contract working — catalogue empty by design → `404 DISEASE_NOT_FOUND` |
| `POST /api/v1/recommendations` | ✅ Contract working — returns `501 NOT_IMPLEMENTED` (no invented science) |
| Real ML model | ⏳ `app/ml/predictor.py` is the integration seam |
| PostgreSQL | ⏳ `app/repositories/` is the integration seam |
| Swagger / ReDoc | ✅ `/docs` and `/redoc` |

**No fake predictions and no fake database data anywhere.**

## Run it

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
cp .env.example .env                 # Windows: copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Test it

```bash
pytest -v
```

## Architecture

```
routes (HTTP only) → services (business logic) → repositories (data access)
                        │                            in-memory today, SQLAlchemy later
                        ├── storage  (safe UUID-named image files)
                        └── ml       (predictor stub — real model plugs in here)
schemas  = public API contract
domain   = internal records/enums shared across layers
core     = config, logging, errors, middleware
```

### Error envelope (every failing request)

```json
{ "error": { "code": "INVALID_IMAGE", "message": "…", "details": null } }
```

| Code | HTTP | Meaning |
|---|---|---|
| `VALIDATION_ERROR` | 422 | Malformed request / path param / missing multipart field |
| `INVALID_IMAGE` | 415 | Not a supported image (content type or file signature) |
| `FILE_TOO_LARGE` | 413 | Exceeds `MAX_UPLOAD_SIZE_MB` |
| `PREDICTION_NOT_FOUND` | 404 | Unknown prediction id |
| `DISEASE_NOT_FOUND` | 404 | Unknown disease name |
| `NOT_IMPLEMENTED` | 501 | Recommendation engine not connected yet |
| `MODEL_NOT_AVAILABLE` | 503 | Predictor called before ML integration |
| `STORAGE_ERROR` | 500 | Disk failure (no paths leaked to clients) |
| `INTERNAL_ERROR` | 500 | Unexpected error (logged server-side) |

## Known limitations (by design, for this task)

- Prediction records live **in memory** (`InMemoryPredictionRepository`):
  they disappear on restart and are not shared between workers.
  The Database Integration task replaces this class only.
- Uploaded images are kept in `UPLOAD_DIR`; a cleanup/retention job is a
  later task.
- Records stay in `received` status until the ML worker is connected.

## Next tasks

1. **Database Integration** — implement `SqlPredictionRepository` / `SqlDiseaseRepository`, Alembic migrations, load a real disease catalogue.
2. **ML Integration** — implement `CropDiseasePredictor.predict()`, call `PredictionService.process_prediction()` from a background worker.
3. **Recommendation engine** — implement `RecommendationService.recommend()`.
4. **Chatbot** — LangChain + Llama 3 via Ollama.
