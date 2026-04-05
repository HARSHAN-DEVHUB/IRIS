# 📅 Development Roadmap

Project phases, features, and development status.

## Phase Overview

| Phase | Status | Timeline | Goal |
|-------|--------|----------|------|
| Phase 1 (MVP) | ✅ **Complete** | Weeks 1-2 | Core voice assistant |
| Phase 2 (AI Brain) | 🔄 **In Progress** | Weeks 3-4 | Intelligent conversation |
| Phase 3 (Memory) | 📅 **Planned** | Weeks 5-6 | Personalization |
| Phase 4 (Automation) | 📅 **Planned** | Weeks 7-8 | Advanced integration |
| Phase 5 (Polish) | 📅 **Planned** | Weeks 9+ | Production ready |

---

## Phase 1: MVP - Basic Voice Assistant ✅

**Status**: ✅ Complete  
**Timeline**: Weeks 1-2  
**Goal**: Get core voice-to-action working

### Implemented ✅

- ✅ Speech-to-text engine (Whisper)
- ✅ Wake-word detection (Vosk)
- ✅ Basic intent parsing
- ✅ Text-to-speech output (pyttsx3)
- ✅ System command execution
- ✅ Application launching
- ✅ Basic logging

### Deliverable

Users can say "Open Chrome" and it opens.

### Branch

`main`  
**Test Coverage**: 70%  
**Performance**: 5-15 second response time

---

## Phase 2: AI Brain Enhancement 🔄

**Status**: 🔄 In Progress  
**Timeline**: Weeks 3-4  
**Estimated Completion**: 2026-04-20  
**Goal**: Intelligent, context-aware conversation

### Features

- [ ] Full LLM integration (Ollama/Llama 2)
- [ ] Multi-turn conversations
- [ ] Context awareness
- [ ] Advanced intent parsing
- [ ] Named entity extraction
- [ ] Error recovery & clarification
- [ ] Response generation with context

### Currently Working On

```
⚙️  Core LLM integration
⚙️  Intent parser improvements
⚙️  Entity extraction engine
```

### Example: Before vs After

**Before (Phase 1)**:
```
User: "Schedule a meeting with team"
IRIS: "I can't understand that."
```

**After (Phase 2)**:
```
User: "Schedule a meeting with team about Q2 planning"
IRIS: "When would you like to schedule this?"
User: "Next Tuesday at 2 PM"
IRIS: "For how long?"
User: "One hour"
IRIS: "I've scheduled 1-hour meeting with team about Q2 planning for next Tuesday 2 PM"
```

### Branch

`develop`  
**Test Coverage Target**: 80%

---

## Phase 3: Memory & Personalization 📅

**Status**: 📅 Planned  
**Timeline**: Weeks 5-6  
**Estimated Start**: 2026-04-20  
**Goal**: Personal, adaptive assistant

### Features

- [ ] User preference storage
- [ ] Conversation history with vector embeddings
- [ ] Habit pattern recognition
- [ ] ChromaDB integration for semantic search
- [ ] Recommendation engine
- [ ] User profiling

### Example

```
User: "What did I ask you about last week?"
IRIS: "You asked about Python tutorials. Would you like to continue where we left off?"

User: "Show my typical meeting time"
IRIS: "Based on your habits, you usually have meetings on Tuesdays at 2 PM"
```

### Branch

`feature/memory`  
**Depends On**: Phase 2 completion

---

## Phase 4: Advanced Automation 📅

**Status**: 📅 Planned  
**Timeline**: Weeks 7-8  
**Estimated Start**: 2026-05-04  
**Goal**: Enterprise automation capabilities

### Features

- [ ] Google Calendar API integration
- [ ] Gmail API integration
- [ ] Browser automation (Selenium)
- [ ] Advanced file operations
- [ ] Email composition & sending
- [ ] Meeting coordination
- [ ] Document processing

### Example

```
User: "Email the Q2 report to executives"
IRIS: Uses Gmail API to send, Calendar to find who executives are, Files to attach document
Result: Email sent successfully to 8 executives

User: "Find conflicting meetings tomorrow"
IRIS: Uses Calendar API to identify overlapping times
Result: "You have 2 conflicting meetings tomorrow at 2-3 PM"
```

### Branch

`feature/automation`  
**Depends On**: Phase 3 completion

---

## Phase 5: Security & Polish 📅

**Status**: 📅 Planned  
**Timeline**: Weeks 9+  
**Estimated Start**: 2026-05-18  
**Goal**: Production-ready security & UX

### Features

- [ ] Voice biometric authentication
- [ ] End-to-end encryption (E2E)
- [ ] RBAC permission system
- [ ] Comprehensive audit logging
- [ ] GDPR compliance
- [ ] Web dashboard UI
- [ ] Mobile app support
- [ ] System tray integration

### Example

```
Startup: IRIS asks you to say a phrase for voice authentication
User: Says phrase correctly
IRIS: "Voice verified. Welcome!"

Later (Unauthorized access attempt):
Third party: Says wake word
IRIS: "Voice verification failed. Unknown user."
```

### Branch

`feature/security`  
**Depends On**: Phase 4 completion

---

## Future Considerations (Post-Phase 5)

- Smart home integration (Alexa, HomeKit)
- Custom plugin ecosystem
- Cloud synchronization
- Cross-device support
- Offline-first improvements
- Multilingual support
- Advanced reasoning capabilities

---

## How to Contribute

See [Contributing Guide](CONTRIBUTING.md) for:
- Development setup
- Workflow for starting new phases
- Code standards
- PR submission process

---

## Version History

| Version | Date | Phase | Status |
|---------|------|-------|--------|
| 0.1.0 | 2026-04-05 | MVP | Current |
| 0.2.0 | 2026-04-20 | Phase 2 | In Progress |
| 0.3.0 | 2026-05-04 | Phase 3 | Planned |
| 0.4.0 | 2026-05-18 | Phase 4 | Planned |
| 0.5.0 | 2026-06-15 | Phase 5 | Planned |
| 1.0.0 | 2026-07-01 | Release | Planned |

---

## Getting Involved

- 🎯 Check [open issues](https://github.com/HARSHAN-DEVHUB/IRIS/issues)
- 🤝 Join [discussions](https://github.com/HARSHAN-DEVHUB/IRIS/discussions)
- 📝 Read [Contributing](CONTRIBUTING.md) guide
- 🔗 Check [Project Board](https://github.com/HARSHAN-DEVHUB/IRIS/projects/1)

---

See [Project Structure](PROJECT_STRUCTURE.md) for codebase organization and [Testing](TESTING.md) for development tools.
