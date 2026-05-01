# System Design: Credit Card Fraud Detection

## Requirements

### Functional
- **Real-time inference**: Receive a transaction payload from the point-of-sale (POS) system and return a synchronous block/allow decision.
- **Batch inference**: Score bulk transactions offline (e.g., for nightly reconciliation, auditing, or backfilling predictions).

### Non-Functional
| Requirement | Target |
|------------|--------|
| Scale | 10M–50M transactions/day |
| Latency | < 200ms ideal, < 500ms absolute upper bound |
| Availability | 99.99% minimum (Max 52 mins downtime/year) |
| Feature Freshness | Hybrid (Real-time streaming + Batch historical) |

---

## Estimation

| Metric | Calculation | Result |
|--------|------------|--------|
| **QPS** | `(50,000,000 / 86,400) * 3` (peak multiplier) | ~1,734 QPS peak |
| **Storage** | `50,000,000 * 1 KB / day` | ~50 GB/day (~18 TB/year) |
| **Bandwidth** | `1,734 QPS * 1 KB` | ~1.7 MB/s |

---

## High-Level Architecture

```text
[POS Client] 
     │ (1. Real-time request)
     ▼ 
[API Gateway] ──(2. Async Log)──> [Message Broker (Kafka)] ──> [Stream Engine (Flink)]
     │                                                                │
     ▼ (3. Route)                                                     │ (4. Update streaming features)
[Model Serving Service] ◄──(5. Fetch Features)──► [Online Feature Store (Redis)]
     │
     ▼ (6. Predict & return)
  [Decision]
     │
     ▼ (7. Log Prediction)
[Message Broker (Kafka)] ──> [Data Lake / Data Warehouse (S3/Snowflake)]
                                      │
                                      ├──► [Batch Inference Service]
                                      │
                                      ├──► [Batch Feature Pipeline (ZenML)] ──(Sync)──► [Online Feature Store]
                                      │
                                      └──► [Model Training Pipeline (ZenML)]
```

### Component Descriptions
- **API Gateway**: Entry point for POS requests. Handles authentication, rate limiting, and routes to the model serving service.
- **Model Serving Service**: Validates request, fetches user profile/historical features from Redis, predicts fraud using the deployed ML model, and responds to the gateway. Fails over gracefully.
- **Online Feature Store (Redis)**: Low-latency Key-Value store serving pre-calculated batch features and continuously updated streaming features.
- **Stream Engine (Flink)**: Consumes raw transaction events from Kafka, computes streaming features (e.g., "count of transactions in last 5 minutes"), and upserts to Redis.
- **Data Lake (S3/Snowflake)**: The source of truth for all historical transaction logs and prediction results, supporting model retraining.
- **Batch Pipelines (ZenML)**: Handles heavy lifting: nightly feature recalculations, model retraining, and evaluating model drift.

---

## Deep-Dive: Online Feature Store & Streaming Pipeline

**Data Model**: 
The Online Feature Store (Redis) stores key-value pairs where the key is the entity ID (e.g., `user_id` or `card_id`) and the value is a serialized blob of features (e.g., JSON or Protobuf).
- *Access Pattern*: Point reads by `card_id` during inference. Point writes by Flink and bulk writes by the nightly batch job.

**Algorithm/Approach**: 
To support hybrid features, we use a Lambda architecture approach for features:
1. ZenML Batch pipeline computes historical features (e.g., "30-day avg spend") and bulk-loads them to Redis nightly.
2. Flink processes Kafka streams to maintain stateful real-time features (e.g., "5-min transaction velocity").

**Scaling Strategy**: 
Redis handles 100k+ reads/second easily, so 1.7k QPS is trivial. We will use a managed Redis cluster (e.g., AWS ElastiCache) across multiple Availability Zones to handle read scaling and fault tolerance.

**Failure Handling**: 
If the streaming pipeline (Flink) goes down, Redis will simply serve slightly stale real-time features. This is an acceptable graceful degradation. We prioritize serving the inference request over feature freshness.

---

## Deep-Dive: Model Serving & Latency Optimization

**Interface**: 
REST API or gRPC. Receives `transaction_amount`, `merchant_id`, `card_id`. Returns `{"is_fraud": bool, "confidence": float}`.

**Algorithm/Approach**: 
The serving service runs a lightweight web framework (e.g., FastAPI) and loads the trained LightGBM or Logistic Regression model into memory. Upon receiving a request, it concurrently fetches the Redis features and executes the model prediction. 

**Latency Budget Breakdown**:
- 50ms: Network transit (POS to Gateway to Service)
- 15ms: Feature Store Fetch (Redis)
- 30ms: Model execution (LightGBM/LR)
- Total: ~95ms (well within the 200ms ideal budget).

**Failure Handling (99.99% Availability)**: 
If the Model Serving service fails or the model errors out, the system must **fail-open** or execute a **rules-based fallback**. Blocking a legitimate transaction due to system failure is unacceptable. 
- *Fallback Strategy*: If prediction takes >150ms, timeout and return "Allow" for transactions under $100, and trigger manual review for transactions over $100.

---

## Tradeoffs

| Decision | Chosen | Alternative | Reason | When Alternative is Better |
|----------|--------|-------------|--------|----------------------------|
| **Feature Store** | Centralized Redis | Client passes all features | POS client cannot reasonably calculate historical or streaming velocity features. | If features are solely based on the current transaction payload. |
| **Streaming Engine** | Flink + Kafka | Spark Streaming | Flink offers true event-driven stream processing with lower latency than Spark's micro-batches. | If the team already operates a heavy Spark ecosystem. |
| **Architecture** | Hybrid (Batch+Stream) | Pure Streaming (Kappa) | We already have ZenML batch pipelines built. Pure streaming is harder to backfill and debug. | When the infrastructure team is highly mature with stream processing. |
| **Failure Mode** | Fail-Open | Fail-Closed | Business priority is minimizing friction for legitimate customers; we accept a slight increase in fraud during an outage. | In systems like medical devices or high-security authentication. |

---

## Operational Concerns

### Monitoring
- **System Metrics**: Track the 4 Golden Signals (Latency, Traffic, Errors, Saturation) for the Model Serving API and Feature Store.
- **ML Metrics**: Monitor prediction distributions. If the average predicted fraud rate jumps from 1% to 15%, trigger an alert.
- **Drift Detection**: Use Evidently AI to compare the daily ingested data distributions against the baseline data used during training.

### Deployment
- **Strategy**: **Shadow Mode** deployment first. The model scores transactions in production but doesn't block them. We evaluate precision/recall offline.
- **Rollout**: Move to a **Canary Rollout** (block fraud for 5% of traffic), then gradually increase to 100%.

### Failure Modes & Degradation
- **Redis goes down**: The Model Serving service falls back to a rules-based system or serves predictions using only the transaction payload features (ignoring historical features).
- **Model Drift detected**: Alert sent to Slack. ZenML pipeline triggered manually to retrain the model on the latest data. 

### Cost Estimation
- Compute (EKS/ECS for Serving): ~$500/month
- Feature Store (Managed Redis): ~$200/month
- Stream Processing (Managed Kafka/Flink): ~$800/month
- Storage (S3, 18TB/yr): ~$400/month
- Total estimated infrastructure cost: ~$1,900/month.
