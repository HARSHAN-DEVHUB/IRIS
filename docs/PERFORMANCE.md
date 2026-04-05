# ⚡ Performance Tuning Guide

Optimize IRIS for speed and efficiency on your hardware.

## Performance Benchmarks

### Operation Timings

| Operation | Time | Notes |
|-----------|------|-------|
| **Wake-word detection** | < 100ms | Real-time processing |
| **Speech-to-text** (5 sec) | 2-5s | Depends on Whisper model |
| **LLM inference** (Llama 2, CPU) | 3-10s | Depends on i7/i9 |
| **LLM inference** (GPT-4, API) | 1-3s | Cloud-based |
| **Command execution** | < 1s | App launching |
| **Text-to-speech** | < 2s | Audio generation |
| **Full pipeline** | 5-20s | Wake → Response → Action |

### Resource Usage

| Resource | Idle | Active | Peak |
|----------|------|--------|------|
| **CPU** | 2-5% | 40-60% | 80-100% |
| **RAM** | 200-300 MB | 800-1200 MB | 2-3 GB |
| **Disk I/O** | None | 50-100 MB/s | 100-200 MB/s |
| **Network** | 0 KB/s | 50-100 KB/s | 200-500 KB/s |

---

## Performance Optimization

### 1. CPU Optimization

#### Use Smaller LLM Model

```yaml
llm:
  model: "mistral"  # Smaller, faster than llama2
  # or
  model: "neural-chat"  # Optimized for speed
```

**Model Comparison**:
| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| Mistral | 7B | ⚡⚡⚡ Fast | ⭐⭐⭐ Good |
| Neural-Chat | 7B | ⚡⚡⚡ Fast | ⭐⭐⭐ Good |
| Llama 2 | 7B | ⚡⚡ Medium | ⭐⭐⭐ Good |
| Llama 2 | 13B | ⚡ Slow | ⭐⭐⭐⭐ Excellent |

#### Reduce Response Length

```yaml
llm:
  max_tokens: 256  # Shorter responses = faster
  # Instead of 512
```

#### Limit Worker Threads

```yaml
performance:
  num_workers: 2  # Reduce from 4 if CPU bottleneck
```

#### Use Cloud AI (Faster)

```bash
LLM_PROVIDER=openai  # Use GPT-4 instead of local
# Much faster (1-3s vs 5-10s)
# But requires API key and internet
```

---

### 2. RAM Optimization

#### Reduce Cache Size

```yaml
performance:
  cache_size: 50  # Reduced from 100
  # Fewer cached responses = less memory
```

#### Use GPU Instead of CPU

```yaml
llm:
  ollama:
    num_gpu: 1  # Enable GPU acceleration
```

This offloads to GPU, freeing system RAM:
- **CPU-only**: 1-2 GB RAM usage
- **GPU**: 500-800 MB RAM usage
- **Cloud**: 200-300 MB RAM usage

#### Reduce Vector Database Cache

```python
# In brain/memory_manager.py
MAX_CACHE_ITEMS = 50  # Reduced from 100
```

---

### 3. Disk I/O Optimization

#### Use SSD (Fastest)

```bash
# Check disk type
lsblk -d -o name,rota
# 0 = SSD (fast), 1 = HDD (slow)
```

If on HDD:
- Consider upgrading to SSD
- Or reduce logging

#### Reduce Logging Verbosity

```yaml
logging:
  level: "WARNING"  # Reduced from INFO
  # Fewer disk writes
```

#### Disable Backups (Development Only)

```yaml
storage:
  backup:
    enabled: false  # For development only!
```

---

### 4. Network Optimization

#### Use Local LLM

```bash
LLM_PROVIDER=ollama  # No network needed
# Instead of OpenAI which requires internet
```

#### Optimize API Calls

```python
# Cache API responses
@lru_cache(maxsize=128)
def get_user_data(user_id):
    return fetch_from_api(user_id)
```

#### Use Connection Pooling

```python
# Automatic with requests library
# Reuses connections instead of creating new ones
```

---

### 5. Audio Optimization

#### Reduce Sample Rate (if acceptable)

```yaml
audio:
  sample_rate: 8000  # Reduced from 16000
  # Lower quality but faster processing
  # 16000 recommended for accuracy
```

#### Increase Chunk Size (processing efficiency)

```yaml
audio:
  chunk_size: 2048  # Increased from 1024
  # Processes more data at once
  # Tradeoff: slightly higher latency
```

---

## Scenario-Based Optimization

### Scenario 1: Slow Machine (i3, 4 GB RAM)

```yaml
llm:
  provider: "openai"  # Use cloud, not local
  model: "gpt-3.5-turbo"
  temperature: 0.5
  max_tokens: 256

audio:
  sample_rate: 8000  # Lower quality
  chunk_size: 2048

performance:
  num_workers: 1
  cache_size: 20

logging:
  level: "WARNING"
```

**Result**: ~5-10 seconds response time

### Scenario 2: Medium Machine (i7, 16 GB RAM)

```yaml
llm:
  provider: "ollama"
  model: "mistral"
  temperature: 0.7
  max_tokens: 512

llm:
  ollama:
    num_gpu: 0  # CPU only

performance:
  num_workers: 4
  cache_size: 100
  enable_request_queue: true

logging:
  level: "INFO"
```

**Result**: ~8-12 seconds response time

### Scenario 3: High-End Machine (i9, 32 GB RAM, RTX 3080)

```yaml
llm:
  provider: "ollama"
  model: "llama2-13b"  # Larger model
  temperature: 0.8
  max_tokens: 1024

llm:
  ollama:
    num_gpu: 1  # GPU acceleration

performance:
  num_workers: 8
  cache_size: 500
  enable_request_queue: true
  enable_profiling: true

logging:
  level: "DEBUG"
```

**Result**: ~5-8 seconds response time

---

## Profiling & Monitoring

### Enable Profiling

```yaml
advanced:
  enable_profiling: true
```

### Monitor Performance

```bash
# CPU/Memory usage
top -p $(pgrep -f "python main.py")

# Disk usage
du -sh data/ logs/

# Network (if using cloud)
iftop  # Monitor network traffic
```

### Profile Code Execution

```bash
# Generate profile
python -m cProfile -o profile_stats.prof main.py

# View results
python -m pstats profile_stats.prof
# (then: sort cumtime, stats 10)
```

### Benchmark Operations

```python
import time

# Benchmark LLM response
start = time.time()
response = llm.generate("Hello")
elapsed = time.time() - start
print(f"LLM took {elapsed:.2f}s")
```

---

## Storage Optimization

### Database Optimization

```bash
# Optimize database
sqlite3 data/iris.db "VACUUM;"

# Check database size
ls -lh data/iris.db
```

### Clean Old Logs

```bash
# Remove logs older than 7 days
find logs/ -name "*.log.*" -mtime +7 -delete

# Archive old logs
tar -czf logs/archive_$(date +%Y%m%d).tar.gz logs/iris.log.*
```

### Archive Old Conversations

```python
import datetime
from brain.memory_manager import MemoryManager

memory = MemoryManager()

# Archive conversations older than 30 days
cutoff = datetime.datetime.now() - datetime.timedelta(days=30)
memory.archive_conversations_before(cutoff)
```

---

## Common Performance Issues

### Issue: High Memory Usage

**Diagnosis**:
```bash
ps aux | grep python  # Check RSS column
```

**Solutions**:
1. Reduce cache size
2. Use GPU instead of CPU
3. Use smaller LLM model
4. Reduce max_tokens

**Example Fix**:
```yaml
performance:
  cache_size: 50  # was 100
llm:
  max_tokens: 256  # was 512
llm:
  ollama:
    num_gpu: 1  # Enable GPU
```

### Issue: Slow Response Times

**Diagnosis**:
```bash
# Monitor CPU while asking IRIS a question
watch -n 0.5 "top -b -p $(pgrep -f 'python main.py')"
```

**Solutions**:
1. Use cloud AI (faster)
2. Use smaller model
3. Enable GPU acceleration
4. Reduce max_tokens

**Example Fix**:
```bash
LLM_PROVIDER=openai  # Use cloud
```

### Issue: 100% CPU Usage

**Diagnosis**:
```bash
top  # Identify Python process using CPU
```

**Solutions**:
1. Use cloud AI instead
2. Reduce num_workers
3. Enable GPU
4. Use smaller model

---

## Performance Monitoring Checklist

- [ ] Monitor baseline performance
- [ ] Profile critical paths
- [ ] Use appropriate LLM/model
- [ ] Enable GPU if available
- [ ] Optimize database regularly
- [ ] Clean logs periodically
- [ ] Monitor memory/CPU usage
- [ ] Test with your typical workload

---

## Further Reading

- [Architecture](ARCHITECTURE.md) - System design
- [Configuration](CONFIGURATION.md) - Configuration options
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues

---

**Questions?** Check [FAQ](FAQ.md) or open an [issue](https://github.com/HARSHAN-DEVHUB/IRIS/issues).
