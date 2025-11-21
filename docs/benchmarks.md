# Memorable Benchmarks

## Overview

This document describes benchmark results and methodology for evaluating Memorable's performance.

## Benchmark Suite

### 1. LOCOMO Benchmark

**Purpose**: Evaluate long-term conversation memory capabilities.

**Reference**: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
- arXiv:2504.19413 (April 2025)
- https://arxiv.org/abs/2504.19413

**Test Categories**:
- Single-hop questions
- Multi-hop questions
- Temporal questions
- Open-domain questions

**Results** (Target):
- Overall accuracy: >75% (target: 30%+ improvement over Mem0)
- Single-hop: >85%
- Multi-hop: >70%
- Temporal: >65%
- Open-domain: >60%

**Methodology**:
1. Load test conversations
2. Extract and store memories
3. Ask questions requiring memory retrieval
4. Measure accuracy of responses

### 2. Multi-hop Reasoning Benchmark

**Purpose**: Test graph-based relationship traversal.

**Test Cases**:
- Entity relationship following
- Multi-step reasoning
- Graph traversal accuracy

**Results** (Target):
- Accuracy: >90%
- Average path length: 2-3 hops

**Methodology**:
1. Setup knowledge graph with entities and relationships
2. Ask questions requiring multi-hop reasoning
3. Measure accuracy of graph traversal

### 3. Temporal Coherence Benchmark

**Purpose**: Test temporal memory tracking.

**Reference**: "Highly engaging events reveal semantic and temporal compression in online community discourse"
- PNAS Nexus (March 2025)

**Test Cases**:
- Time-stamped memory retrieval
- Temporal sequence following
- Coherence checking

**Results** (Target):
- Temporal accuracy: >85%
- Coherence score: >90%

**Methodology**:
1. Create time-stamped memories
2. Query memories by time range
3. Check temporal coherence
4. Measure accuracy

## Performance Metrics

### Latency

**Target**: <100ms retrieval latency

**Measurement**:
- Time from query to memory retrieval
- Average across 1000 queries

### Token Efficiency

**Target**: 50%+ token savings vs full-context

**Measurement**:
- Compare tokens used with Memorable vs full-context injection
- Measure on LOCOMO benchmark

### Scalability

**Target**: Handle 10,000+ memories efficiently

**Measurement**:
- Query latency vs memory count
- Storage efficiency

## Comparison with Other Systems

### vs Mem0

**Mem0 Results** (from paper):
- 26% improvement over OpenAI memory
- 91% latency reduction
- 90% token savings

**Memorable Target**:
- 30%+ improvement over Mem0
- <100ms retrieval latency
- 50%+ token savings

### vs Memori

**Comparison Points**:
- Integration ease (both use interceptors)
- Performance (Memorable adds graph support)
- Research validation (Memorable has benchmarks)

### vs Supermemory

**Comparison Points**:
- Graph architecture (both support graphs)
- Performance claims (Supermemory: 25× faster, unverified)
- Research validation (Memorable has benchmarks)

## Running Benchmarks

### LOCOMO Benchmark

```python
from memorable import MemoryEngine
from memorable.benchmarks.locomo import LOCOMOBenchmark

memory = MemoryEngine(database="sqlite:///benchmark.db")
memory.enable()

benchmark = LOCOMOBenchmark(memory)
results = await benchmark.run()
print(results)
```

### Multi-hop Benchmark

```python
from memorable.benchmarks.multihop import MultiHopBenchmark

benchmark = MultiHopBenchmark(memory)
results = await benchmark.run()
print(results)
```

### Temporal Benchmark

```python
from memorable.benchmarks.temporal import TemporalBenchmark

benchmark = TemporalBenchmark(memory)
results = await benchmark.run()
print(results)
```

## Results Publication

Benchmark results will be published in:
- Research paper (planned)
- GitHub repository
- Documentation updates

## References

- Mem0 Paper: https://arxiv.org/abs/2504.19413
- LOCOMO Benchmark: Reference implementation from Mem0
- MemOS Dataset: https://huggingface.co/datasets/MemTensor/MemOS_eval_result

