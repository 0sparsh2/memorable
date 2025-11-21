# Memorable Benchmarks

This directory contains benchmark implementations for evaluating Memorable's performance.

## Benchmarks

### 1. LOCOMO Benchmark

Long-term Conversation Memory benchmark based on Mem0's research.

**Reference**: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
- arXiv:2504.19413 (April 2025)
- https://arxiv.org/abs/2504.19413

**Test Categories**:
- Single-hop questions
- Multi-hop questions
- Temporal questions
- Open-domain questions

**Usage**:
```python
from memorable import MemoryEngine
from memorable.benchmarks.locomo import LOCOMOBenchmark

memory = MemoryEngine(database="sqlite:///benchmark.db")
memory.enable()

benchmark = LOCOMOBenchmark(memory)
results = await benchmark.run()
print(results)
```

### 2. Multi-hop Reasoning Benchmark

Tests graph-based relationship traversal and multi-hop reasoning.

**Usage**:
```python
from memorable.benchmarks.multihop import MultiHopBenchmark

benchmark = MultiHopBenchmark(memory)
results = await benchmark.run()
print(results)
```

### 3. Temporal Coherence Benchmark

Tests temporal memory tracking and coherence.

**Usage**:
```python
from memorable.benchmarks.temporal import TemporalBenchmark

benchmark = TemporalBenchmark(memory)
results = await benchmark.run()
print(results)
```

### 4. System Comparison

Compares Memorable with Memori, Mem0, and Supermemory.

**Usage**:
```python
from memorable.benchmarks.comparison import SystemComparison

comparison = SystemComparison(memory)
results = await comparison.run_comparison()
print(results)
```

## Running Benchmarks

```bash
# Run all benchmarks
make benchmark

# Run specific benchmark
pytest benchmarks/locomo/ -v
pytest benchmarks/multihop/ -v
pytest benchmarks/temporal/ -v
pytest benchmarks/comparison/ -v
```

## Expected Results

### LOCOMO (Target)
- Overall accuracy: >75%
- Single-hop: >85%
- Multi-hop: >70%
- Temporal: >65%
- Open-domain: >60%

### Performance (Target)
- Retrieval latency: <100ms
- Token savings: 50%+ vs full-context
- Setup time: <1s

## References

- Mem0 Paper: https://arxiv.org/abs/2504.19413
- Mem0 GitHub: https://github.com/mem0ai/mem0
- Memori GitHub: https://github.com/GibsonAI/Memori
- Supermemory GitHub: https://github.com/supermemoryai/supermemory

