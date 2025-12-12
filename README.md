# LLM Evaluation Pipeline - Execution Flow & Project Structure
## Using Groq Cloud LLM Models

---

## Project Overview

This document outlines the complete execution flow and project structure for building an LLM evaluation pipeline that assesses AI responses across three dimensions:
1. **Response Relevance & Completeness**
2. **Hallucination / Factual Accuracy**
3. **Latency & Costs**

The pipeline leverages **Groq Cloud LLM models** for efficient, low-latency evaluation operations.

---

## Project Structure

```
llm-evaluation-pipeline/
│
├── README.md                           # Main documentation
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore file
│
├── src/                                # Main source code
│   ├── __init__.py
│   ├── config.py                       # Configuration & constants
│   ├── logger.py                       # Logging setup
│   │
│   ├── data_loader/
│   │   ├── __init__.py
│   │   ├── json_loader.py              # Load chat & context JSONs
│   │   └── schema_validator.py         # Validate input schema
│   │
│   ├── feature_extraction/
│   │   ├── __init__.py
│   │   ├── extractor.py                # Extract features from inputs
│   │   └── preprocessing.py            # Clean & preprocess data
│   │
│   ├── evaluators/
│   │   ├── __init__.py
│   │   ├── base_evaluator.py           # Abstract evaluator class
│   │   ├── relevance_evaluator.py      # Relevance & completeness
│   │   ├── hallucination_evaluator.py  # Hallucination detection
│   │   └── latency_cost_evaluator.py   # Latency & cost metrics
│   │
│   ├── llm_service/
│   │   ├── __init__.py
│   │   ├── groq_client.py              # Groq API wrapper
│   │   ├── prompt_templates.py         # Evaluation prompts
│   │   └── cache_manager.py            # Caching for embeddings/calls
│   │
│   ├── aggregation/
│   │   ├── __init__.py
│   │   └── result_aggregator.py        # Combine metrics & scores
│   │
│   ├── output/
│   │   ├── __init__.py
│   │   ├── formatter.py                # Format results (JSON, etc.)
│   │   └── reporter.py                 # Generate reports
│   │
│   └── pipeline.py                     # Main pipeline orchestrator
│
├── samples/                            # Sample JSONs for testing
│   ├── sample_chat.json
│   └── sample_context.json
│
├── tests/                              # Unit tests
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_evaluators.py
│   └── test_pipeline.py
│
└── main.py                             # Entry point script
```

---

## Execution Flow

### Phase 1: Initialization & Setup

```
START
  │
  ├─→ Load Configuration
  │    ├─ API Keys (Groq)
  │    ├─ Model names & parameters
  │    ├─ Evaluation thresholds
  │    └─ Cache settings
  │
  ├─→ Initialize Logger
  │    └─ Console & file logging
  │
  ├─→ Initialize Groq Client
  │    ├─ Authenticate with Groq API
  │    └─ Verify connection
  │
  └─→ Initialize Cache Manager
       └─ In-memory cache for embeddings
```

**Key Actions:**
- Read `.env` file for `GROQ_API_KEY`
- Validate configuration
- Setup logger with timestamps
- Create Groq client singleton

---

### Phase 2: Data Loading & Validation

```
Load Inputs
  │
  ├─→ Load Chat JSON
  │    ├─ Read file path
  │    ├─ Parse JSON
  │    ├─ Validate schema
  │    │  ├─ Check conversation structure
  │    │  ├─ Verify user message exists
  │    │  └─ Verify AI response exists
  │    └─ Extract metadata
  │        ├─ Timestamps
  │        ├─ User ID
  │        ├─ Session ID
  │        └─ Model used
  │
  ├─→ Load Context Vectors JSON
  │    ├─ Read file path
  │    ├─ Parse JSON
  │    ├─ Validate schema
  │    │  ├─ Check retrieval format
  │    │  └─ Verify context chunks
  │    └─ Extract metadata
  │        ├─ Retrieved doc count
  │        ├─ Similarity scores
  │        └─ Source documents
  │
  └─→ Data Validation Summary
       ├─ Log validation results
       └─ Proceed or error handling
```

**Key Actions:**
- Parse JSON files safely (error handling)
- Validate required fields
- Extract user query, AI response, and context chunks
- Store metadata for cost calculation

---

### Phase 3: Feature Extraction & Preprocessing

```
Extract Features
  │
  ├─→ From Chat Conversation
  │    ├─ Current user message (query)
  │    ├─ AI response (answer)
  │    ├─ Conversation history (past turns)
  │    ├─ Conversation length
  │    └─ Response generation timestamp
  │
  ├─→ From Context Vectors
  │    ├─ Context chunk count
  │    ├─ Context chunk texts
  │    ├─ Retrieval scores
  │    ├─ Document metadata
  │    └─ Total context length (tokens)
  │
  ├─→ Preprocess Text Data
  │    ├─ Normalize whitespace
  │    ├─ Handle special characters
  │    ├─ Extract sentences from response
  │    ├─ Extract key phrases from query
  │    └─ Clean context chunks
  │
  └─→ Store Extracted Features
       └─ In feature object for evaluators
```

**Key Actions:**
- Extract and parse response text
- Split response into sentences/claims
- Normalize text for comparison
- Count tokens for cost estimation
- Create feature bundle for evaluators

---

### Phase 4: Evaluation - Dimension 1: Relevance & Completeness

```
Evaluate Relevance & Completeness
  │
  ├─→ Relevance Analysis
  │    │
  │    ├─→ Heuristic Checks
  │    │    ├─ Keyword overlap (query ↔ response)
  │    │    ├─ Intent matching
  │    │    ├─ Topic alignment
  │    │    └─ Off-topic detection
  │    │
  │    └─→ Semantic Analysis (via Groq LLM)
  │         ├─ Send prompt to Groq model
  │         │  "Rate how well this response addresses the query"
  │         ├─ Extract relevance score (0-1)
  │         ├─ Cache result
  │         └─ Log token usage
  │
  ├─→ Completeness Analysis
  │    │
  │    ├─→ Coverage Check
  │    │    ├─ Does response cover main question?
  │    │    ├─ Does it address sub-questions?
  │    │    ├─ Are edge cases mentioned?
  │    │    └─ Missing critical information?
  │    │
  │    └─→ LLM-based Completeness (via Groq)
  │         ├─ Send context to Groq model
  │         ├─ "Does this response fully answer the query?"
  │         ├─ Extract completeness score (0-1)
  │         ├─ Identify missing sections
  │         └─ Log token usage
  │
  └─→ Output Relevance & Completeness Metrics
       ├─ Relevance score (0-1)
       ├─ Completeness score (0-1)
       ├─ Combined score
       ├─ Confidence level
       └─ Detailed feedback
```

**Key Actions:**
- Calculate keyword overlap between query and response
- Use Groq's fast model (e.g., Mixtral) for relevance evaluation
- Parse LLM output to extract numeric scores
- Cache embeddings for identical queries
- Track token usage for this dimension

---

### Phase 5: Evaluation - Dimension 2: Hallucination / Factual Accuracy

```
Evaluate Hallucination & Factual Accuracy
  │
  ├─→ Extract Claims from Response
  │    ├─ Split response into sentences
  │    ├─ Identify factual claims
  │    ├─ Filter opinion/subjective statements
  │    └─ Create claim list with indices
  │
  ├─→ Ground Claims Against Context
  │    │
  │    ├─→ For Each Claim:
  │    │    │
  │    │    ├─→ Heuristic Check
  │    │    │    ├─ Keyword matching in context
  │    │    │    ├─ Semantic similarity check
  │    │    │    └─ Supported/Unsupported flag
  │    │    │
  │    │    └─→ LLM-based Factuality (via Groq)
  │    │         ├─ Send to Groq: claim + context
  │    │         ├─ Prompt: "Is this claim supported?"
  │    │         ├─ Parse response:
  │    │         │  ├─ Supported (grounded in context)
  │    │         │  ├─ Unsupported (not in context)
  │    │         │  └─ Contradicted (conflicts context)
  │    │         └─ Log result
  │    │
  │    └─→ Aggregate Claim Verification
  │         ├─ Count supported claims
  │         ├─ Count unsupported claims
  │         ├─ Count contradicted claims
  │         └─ Calculate hallucination ratio
  │
  ├─→ Detect Hallucination Patterns
  │    ├─ Fabricated statistics
  │    ├─ Non-existent sources
  │    ├─ Invented dates/names
  │    └─ Consistency with context
  │
  └─→ Output Hallucination & Accuracy Metrics
       ├─ Hallucination ratio (0-1, lower is better)
       ├─ Accuracy score (0-1, higher is better)
       ├─ List of problematic claims
       ├─ Confidence level
       ├─ Grounding effectiveness
       └─ Detailed feedback per claim
```

**Key Actions:**
- Parse response into atomic claims
- Use Groq for fast hallucination detection
- Cross-reference each claim against context vectors
- Create a grounding report
- Track hallucinated vs. grounded statements

---

### Phase 6: Evaluation - Dimension 3: Latency & Costs

```
Evaluate Latency & Costs
  │
  ├─→ Capture Timing Metrics
  │    ├─ Overall pipeline latency
  │    ├─ Data loading time
  │    ├─ Feature extraction time
  │    ├─ Relevance evaluation time
  │    ├─ Hallucination evaluation time
  │    ├─ Aggregation time
  │    └─ Output formatting time
  │
  ├─→ Original LLM Response Metrics (if available)
  │    ├─ Read from chat JSON
  │    │  ├─ Response generation time
  │    │  ├─ Token count (input)
  │    │  ├─ Token count (output)
  │    │  └─ Model used
  │    └─ Calculate cost of original response
  │         └─ (tokens × model rate)
  │
  ├─→ Evaluation Overhead Metrics
  │    ├─ Count API calls to Groq
  │    │  ├─ Relevance evaluation calls
  │    │  ├─ Hallucination evaluation calls
  │    │  └─ Total calls
  │    ├─ Count total tokens used
  │    │  ├─ Input tokens
  │    │  ├─ Output tokens
  │    │  └─ Total tokens
  │    ├─ Calculate evaluation cost
  │    │  └─ (tokens × Groq model rate)
  │    └─ Compare to original response cost
  │
  ├─→ Scalability Analysis
  │    ├─ If processing N conversations:
  │    │  ├─ Total time: pipeline_time × N
  │    │  ├─ Batch processing potential
  │    │  ├─ Parallel evaluation possible
  │    │  └─ Cache hit rate estimation
  │    └─ Identify bottlenecks
  │         ├─ Sequential vs. parallel ops
  │         ├─ LLM calls vs. compute
  │         └─ I/O vs. processing
  │
  └─→ Output Latency & Cost Metrics
       ├─ Pipeline latency (ms)
       ├─ Cost per evaluation ($)
       ├─ Cost vs. original response (ratio)
       ├─ Tokens per evaluation
       ├─ API calls made
       ├─ Scalability estimate (millions/day)
       └─ Optimization recommendations
```

**Key Actions:**
- Use Python `time.time()` to measure each phase
- Count API calls to Groq
- Track token consumption
- Estimate costs based on Groq pricing
- Identify optimization opportunities
- Calculate throughput for scale

---

### Phase 7: Aggregation & Scoring

```
Aggregate Results
  │
  ├─→ Compile All Dimension Scores
  │    ├─ Relevance score (0-1)
  │    ├─ Completeness score (0-1)
  │    ├─ Hallucination score (inverted, 0-1)
  │    ├─ Accuracy score (0-1)
  │    ├─ Latency score (normalized inverse)
  │    └─ Cost score (normalized inverse)
  │
  ├─→ Compute Weighted Combined Score
  │    ├─ Assign weights (configurable):
  │    │  ├─ Relevance: 25%
  │    │  ├─ Completeness: 25%
  │    │  ├─ Hallucination/Accuracy: 40%
  │    │  ├─ Latency: 5%
  │    │  └─ Cost: 5%
  │    ├─ Calculate weighted sum
  │    └─ Final overall score (0-1)
  │
  ├─→ Generate Reliability Classification
  │    ├─ Score ≥ 0.8: RELIABLE
  │    ├─ Score 0.6-0.8: MODERATE
  │    ├─ Score < 0.6: UNRELIABLE
  │    └─ Assign confidence level
  │
  ├─→ Create Detailed Report
  │    ├─ Dimension scores & feedback
  │    ├─ Problematic areas flagged
  │    ├─ Recommendations for improvement
  │    ├─ Performance metrics summary
  │    └─ Timestamp & metadata
  │
  └─→ Structure Final Result Object
       ├─ Query & response
       ├─ All dimension scores
       ├─ Overall score & reliability
       ├─ Detailed findings
       └─ Metadata
```

**Key Actions:**
- Normalize all scores to 0-1 range
- Apply weighted scoring
- Determine reliability label
- Generate actionable feedback
- Prepare for output

---

### Phase 8: Output & Reporting

```
Format & Output Results
  │
  ├─→ Prepare Output Data
  │    ├─ Serialize to JSON
  │    └─ Create structured result dict
  │
  ├─→ Output to Multiple Formats
  │    │
  │    ├─→ JSON Output
  │    │    ├─ Write to file (result.json)
  │    │    ├─ Pretty print
  │    │    └─ Include all metrics
  │    │
  │    ├─→ Console Output
  │    │    ├─ Print summary table
  │    │    ├─ Highlight key findings
  │    │    └─ Show reliability status
  │    │
  │    └─→ Log Output
  │         ├─ Write to log file
  │         ├─ Include timestamps
  │         └─ Track all evaluations
  │
  ├─→ Generate Report
  │    ├─ Human-readable summary
  │    ├─ Dimension-by-dimension breakdown
  │    ├─ Issues & recommendations
  │    └─ Performance benchmarks
  │
  └─→ Return Results
       └─ To caller or storage
```

**Key Actions:**
- Convert results to JSON
- Print formatted summary
- Log all details
- Generate readable report
- Handle output to file/stdout

---

### Phase 9: Cleanup & Monitoring

```
Finalization
  │
  ├─→ Log Summary Statistics
  │    ├─ Total execution time
  │    ├─ Total tokens used
  │    ├─ Total cost
  │    ├─ Scores achieved
  │    └─ Reliability classification
  │
  ├─→ Cache Management
  │    ├─ Update in-memory cache
  │    ├─ Optionally persist cache
  │    └─ Log cache hit rate
  │
  ├─→ Resource Cleanup
  │    ├─ Close file handles
  │    ├─ Release memory if needed
  │    └─ Close logger
  │
  └─→ END
```

**Key Actions:**
- Log final summary
- Save cache for future runs
- Cleanup resources
- Close gracefully

---

## Complete Execution Timeline

```
INPUT: chat.json + context.json
  │
  ├─ PHASE 1: Initialize (100ms)
  │
  ├─ PHASE 2: Load & Validate (50ms)
  │
  ├─ PHASE 3: Extract Features (75ms)
  │
  ├─ PHASE 4: Evaluate Relevance (500ms - Groq API call)
  │
  ├─ PHASE 5: Evaluate Hallucination (800ms - Multiple Groq calls)
  │
  ├─ PHASE 6: Calculate Latency & Cost (25ms)
  │
  ├─ PHASE 7: Aggregate Results (50ms)
  │
  ├─ PHASE 8: Format & Output (50ms)
  │
  ├─ PHASE 9: Cleanup (25ms)
  │
  └─ OUTPUT: evaluation_result.json (Total: ~1675ms ≈ 1.7 seconds)
```

---

## Key Design Decisions with Groq

### Why Groq?

1. **Ultra-Low Latency**: Groq models are optimized for speed, critical for real-time evaluation
2. **Cost-Effective**: Pay-as-you-go pricing with competitive rates
3. **Multiple Models**: Mix of fast inference models (Mixtral, LLaMA) for different tasks
4. **API Simplicity**: Straightforward REST API for easy integration

### Groq Model Selection

- **Relevance Evaluation**: `llama-3.3-70b-versatile` (balanced speed & quality)
- **Hallucination Detection**: `llama-3.3-70b-versatile` (claims need careful analysis)
- **Quick Classifications**: `llama2-70b-4096` (when available, for speed)

### Optimization Strategies

1. **Batching**: Group similar evaluations to reduce API calls
2. **Caching**: Store embeddings and results to avoid redundant calls
3. **Sampling**: For scale, evaluate 10% of conversations in detail
4. **Async Processing**: Parallel evaluation of claims
5. **Prompt Optimization**: Minimal, focused prompts to reduce token usage

---

## Scalability for Millions of Daily Conversations

### Current Design (Single Conversation)

- Latency: ~1.7 seconds per evaluation
- Cost: ~$0.02 per evaluation (estimate)

### Scaling to Millions/Day

```
Daily Load: 1,000,000 conversations

Approach 1: Sampling (Most Cost-Effective)
├─ Evaluate only 10% (~100,000) in detail
├─ Daily cost: $2,000
├─ Latency: No impact on user
└─ Quality: Good statistical coverage

Approach 2: Lightweight Pipeline
├─ Phase 1: Heuristic checks only (50ms)
├─ Phase 2: LLM evaluation on high-stakes queries only (500ms)
├─ Daily cost: $1,000
└─ Latency: 50ms baseline, 500ms for detailed

Approach 3: Batched Processing
├─ Collect evaluations in batches of 100
├─ Process overnight/off-peak
├─ Reduce per-evaluation cost by 30%
└─ Not real-time but economical

Approach 4: Hybrid (Recommended)
├─ Real-time: Lightweight heuristics (50ms)
├─ Batch: Detailed Groq evaluation (async)
├─ Storage: Results in cache/DB for reference
└─ Daily cost: $800 + infrastructure
```

### Bottleneck Mitigation

```
Bottleneck: Groq API calls
Solution: Cache identical queries, batch similar evaluations

Bottleneck: Tokenization
Solution: Reuse embeddings, cache token counts

Bottleneck: Claim extraction
Solution: Use lightweight regex/NLP, not LLM

Bottleneck: Storage
Solution: Compress results, archive old evaluations
```

---

## Integration Points

### Input Integration

```
User Chat System
    ↓
Chat JSON → Pipeline
Context DB → JSON Export → Pipeline
    ↓
Evaluation Results
    ↓
Output to Dashboard/Monitoring System
```

### Output Integration

```
Evaluation Results
    ├─ Real-time Alert (if unreliable)
    ├─ Log to Monitoring System
    ├─ Store in Results DB
    ├─ Display in Dashboard
    └─ Notify Product Team if issues
```

---

## Configuration & Environment Variables

### `.env` File Variables

```
# Groq API Configuration
GROQ_API_KEY=gsk_xxxxxx
GROQ_MODEL_RELEVANCE=llama-3.3-70b-versatile
GROQ_MODEL_HALLUCINATION=llama-3.3-70b-versatile

# Evaluation Thresholds
RELEVANCE_THRESHOLD=0.7
COMPLETENESS_THRESHOLD=0.7
HALLUCINATION_THRESHOLD=0.2
OVERALL_THRESHOLD=0.7

# Optimization
ENABLE_CACHING=true
CACHE_SIZE=1000
BATCH_SIZE=10
SAMPLING_RATE=1.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=evaluation.log
```

---

## Success Metrics

```
Evaluation Pipeline Success = 
  (Accuracy × 0.3) + 
  (Speed × 0.3) + 
  (Cost-Effectiveness × 0.2) + 
  (Code Quality × 0.2)

Where:
- Accuracy: Correlation with human judgment
- Speed: Sub-2s per evaluation
- Cost: <$0.05 per evaluation
- Code Quality: PEP-8 compliance, tests, docs
```

---

## Real-World Example: Context Vectors JSON Structure

This is an actual example from Malpani Infertility Clinic's vector retrieval system:

```json
{
  "status": "success",
  "status_code": 200,
  "message": "Message sent successfully!",
  "data": {
    "vector_data": [
      {
        "id": 28960,
        "source_url": "https://www.drmalpani.com/hotels",
        "text": "Hotels Near Malpani Infertility Clinic... Happy Home Hotel offers single rooms for Rs 1400 and double rooms for Rs 2000. This is a 5 min walk away from the clinic...",
        "tokens": 403,
        "created_at": "2024-02-09T00:00:00.000Z"
      },
      {
        "id": 27025,
        "source_url": "https://www.drmalpani.com/hotels",
        "text": "Hotels Near Malpani Infertility Clinic... Your best choice would be Gopal Mansion. An airconditioned room with TV and bath is only Rs 800 per night...",
        "tokens": 542,
        "created_at": "2024-02-09T00:00:00.000Z"
      },
      {
        "id": 36724,
        "source_url": null,
        "text": "What is the Cost for IVF?\nA complete IVF cycle at our clinic costs about Rs 3,00,000 - and this is all-inclusive for all medical procedures. Medicines would cost about Rs 145000 more.",
        "tokens": 234,
        "created_at": "2024-09-11T00:00:00.000Z"
      }
    ],
    "sources": {
      "message_id": 361938,
      "vector_ids": [28960, 27025, 36724, ...],
      "vectors_info": [
        {
          "score": 0.5244379923082604,
          "vector_id": 28960,
          "tokens_count": 403
        },
        {
          "score": 0.5116742114729494,
          "vector_id": 27025,
          "tokens_count": 542
        },
        {
          "score": 0.27962456820157633,
          "vector_id": 36724,
          "tokens_count": 234
        }
      ],
      "vectors_used": [27025, 37548, 28960],
      "final_response": [
        "For Gopal Mansion, an air-conditioned room with TV and bath is Rs 800 per night.",
        "Happy Home Hotel offers single rooms for Rs 1400 and double rooms for Rs 2000."
      ]
    }
  }
}
```

### Key Observations from This Example

**Input Structure:**
- Status code & metadata
- Array of vector_data (retrieved context chunks)
- Each chunk has: id, source_url, text content, token count, timestamp

**Relevance Metrics in vectors_info:**
- `score`: Semantic similarity score (0-1, higher = more relevant)
- `tokens_count`: Length of context chunk
- Only top-scoring vectors are used in response

**Evaluation Opportunities:**
1. **Relevance Check**: Compare user query against vector scores
2. **Hallucination Check**: Verify LLM response against actual text content
3. **Cost Analysis**: Count vectors retrieved, total tokens, multiple vector_ids used

---

## Example Evaluation Scenario

### Query: "Where can I stay when visiting Malpani Clinic?"

**Context Vectors Retrieved:** 3 vectors (IDs: 28960, 27025, 36724)

**Hypothetical AI Response:**
> "When visiting Malpani Infertility Clinic, you have excellent accommodation options. Gopal Mansion offers the most affordable option at Rs 800 per night for an AC room. Happy Home Hotel is also nearby with rooms at Rs 1400-2000. The entire IVF treatment cycle costs approximately Rs 3 lakhs."

**Evaluation Breakdown:**

```
PHASE 4: Relevance & Completeness
├─ Query Coverage: ✓ Addresses "where to stay"
├─ Completeness: ✓ Multiple options provided
├─ Off-topic: ✓ Briefly mentions costs (borderline)
└─ Relevance Score: 0.85 (Good - directly answers query)

PHASE 5: Hallucination Detection
├─ Claim 1: "Gopal Mansion offers Rs 800/night AC room"
│   └─ Vector ID 27025: ✓ SUPPORTED (exact match in context)
├─ Claim 2: "Happy Home Hotel Rs 1400-2000"
│   └─ Vector ID 28960: ✓ SUPPORTED (exact match in context)
├─ Claim 3: "IVF cycle costs Rs 3 lakhs"
│   └─ Vector ID 36724: ✓ SUPPORTED (exact match in context)
└─ Hallucination Score: 0.0 (No hallucinations - all grounded)

PHASE 6: Latency & Costs
├─ Vectors Retrieved: 3
├─ Total Context Tokens: 403 + 542 + 234 = 1,179 tokens
├─ Groq API Calls: 2 (relevance + hallucination evaluation)
├─ Total Input Tokens: ~1,500 (context + prompts)
├─ Estimated Cost: $0.008 USD (using Groq Mixtral pricing)
└─ Latency: ~1,200ms (1.2 seconds)

PHASE 7: Aggregation
├─ Relevance Score: 0.85 (25% weight)
├─ Completeness Score: 0.80 (25% weight)
├─ Hallucination Score: 1.0 (40% weight - no hallucinations)
├─ Latency Score: 0.95 (normalized, 5% weight)
├─ Cost Score: 0.90 (normalized, 5% weight)
├─ Weighted Final Score: (0.85×0.25) + (0.80×0.25) + (1.0×0.40) + (0.95×0.05) + (0.90×0.05)
├─ Final Score: 0.9025 ≈ 0.90
└─ Reliability: RELIABLE ✓

PHASE 8: Output
{
  "query": "Where can I stay when visiting Malpani Clinic?",
  "ai_response": "When visiting Malpani...",
  "evaluation": {
    "relevance_score": 0.85,
    "completeness_score": 0.80,
    "hallucination_score": 0.0,
    "overall_score": 0.90,
    "reliability_status": "RELIABLE",
    "grounding_details": {
      "total_claims": 3,
      "supported_claims": 3,
      "unsupported_claims": 0,
      "contradicted_claims": 0
    },
    "context_metrics": {
      "vectors_retrieved": 3,
      "total_context_tokens": 1179,
      "average_retrieval_score": 0.52
    },
    "performance_metrics": {
      "pipeline_latency_ms": 1200,
      "api_calls_made": 2,
      "total_tokens_used": 1500,
      "estimated_cost_usd": 0.008
    }
  }
}
```

---

## Integration with Your Pipeline

### Data Loading Phase (Phase 2)

```python
# Your data_loader.py should handle:

def load_context_json(filepath):
    """Load context vectors JSON"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Extract relevant fields
    context = {
        'vectors': data['data']['vector_data'],
        'retrieval_scores': [v['score'] for v in data['data']['sources']['vectors_info']],
        'total_context_tokens': sum(v['tokens_count'] for v in data['data']['vector_data']),
        'sources_used': data['data']['sources']['vectors_used']
    }
    
    return context
```

### Feature Extraction Phase (Phase 3)

```python
# Your extractor.py should extract:

def extract_context_features(context_data):
    """Extract features from context vectors"""
    
    features = {
        'retrieval_count': len(context_data['vectors']),
        'context_chunks': [v['text'] for v in context_data['vectors']],
        'context_tokens': context_data['total_context_tokens'],
        'source_urls': [v['source_url'] for v in context_data['vectors']],
        'retrieval_scores': context_data['retrieval_scores'],
        'average_relevance': sum(context_data['retrieval_scores']) / len(context_data['retrieval_scores']),
        'timestamp_distribution': [v['created_at'] for v in context_data['vectors']]
    }
    
    return features
```

### Hallucination Evaluation (Phase 5)

```python
# Your hallucination_evaluator.py should:

def check_claim_grounding(claim, context_chunks, groq_client):
    """
    For each claim in the response, verify it's grounded in context
    
    Example:
    Claim: "Gopal Mansion offers Rs 800/night AC room"
    Context: Contains "An airconditioned room with TV and bath is only Rs 800 per night"
    Result: GROUNDED ✓
    """
    
    # Step 1: Heuristic keyword matching
    keywords = extract_keywords(claim)
    for context in context_chunks:
        if all(kw in context for kw in keywords):
            return {"grounded": True, "method": "keyword_match"}
    
    # Step 2: Semantic similarity check
    claim_embedding = get_embedding(claim)
    for idx, context in enumerate(context_chunks):
        context_embedding = get_embedding(context)
        similarity = cosine_similarity(claim_embedding, context_embedding)
        if similarity > 0.8:
            return {"grounded": True, "method": "semantic_match", "score": similarity}
    
    # Step 3: LLM-based verification (Groq)
    prompt = f"""
    Given this claim and context, is the claim supported?
    
    Claim: {claim}
    Context: {' '.join(context_chunks)}
    
    Answer: SUPPORTED / UNSUPPORTED / CONTRADICTED
    """
    
    result = groq_client.evaluate(prompt)
    return {"grounded": result != "UNSUPPORTED", "method": "llm_verify", "response": result}
```

---

## Next Steps

1. **Design Phase**: Finalize architecture with this flow
2. **Development Phase**: Build each component following phases
3. **Testing Phase**: Unit tests for each evaluator
4. **Integration Phase**: Connect to sample JSONs
5. **Optimization Phase**: Profile and optimize bottlenecks
6. **Documentation Phase**: Complete README with examples
7. **Submission Phase**: Push to public GitHub

---

## Quick Reference: Phase Dependencies

```
Phase 1 (Init) 
    ↓
Phase 2 (Load) 
    ↓
Phase 3 (Extract) 
    ↓ (Parallel from here)
├─ Phase 4 (Relevance)
├─ Phase 5 (Hallucination)
└─ Phase 6 (Latency/Cost)
    ↓ (Join back)
Phase 7 (Aggregate)
    ↓
Phase 8 (Output)
    ↓
Phase 9 (Cleanup)
```
---
This execution flow ensures a systematic, scalable approach to evaluating LLM responses while keeping costs and latency low using Groq's fast inference capabilities.

   1     python main.py --chat samples/sample-chat-conversation-01.json --context samples/sample_context_vectors-01.json --output output/response1.json
