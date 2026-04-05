# 🎤 Command Reference

Complete list of voice commands and examples.

## Basic Commands

### Application Control

| Command | Example | What It Does |
|---------|---------|--------------|
| Open App | "Open Slack" | Launch application |
| Close App | "Close Chrome" | Quit application |
| List Apps | "What apps are open?" | Show running apps |
| Hide App | "Hide VS Code" | Minimize window |

### System Information

| Command | Example | What It Does |
|---------|---------|--------------|
| Time | "What time is it?" | Show current time |
| Date | "What's today's date?" | Show current date |
| Storage | "How much storage?" | Show disk space |
| Battery | "Show battery" | Show battery percentage |
| IP Address | "What's my IP?" | Show network IP |

### Help & Info

| Command | Example | What It Does |
|---------|---------|--------------|
| Help | "Help" or "What can you do?" | Show available commands |
| Version | "What version are you?" | Show IRIS version |
| Status | "Are you ready?" | Show system status |
| About | "Tell me about yourself" | Show IRIS info |

---

## Calendar & Scheduling

### Event Management

| Command | Example | What It Does |
|---------|---------|--------------|
| Create Event | "Schedule meeting with team tomorrow at 2 PM" | Create calendar event |
| List Events | "What's my agenda?" | Show upcoming events |
| List Events (Date) | "What's on my calendar Friday?" | Show events for specific day |
| Update Event | "Change meeting to 3 PM" | Modify event time |
| Delete Event | "Cancel tomorrow's meeting" | Remove event |

### Reminders

| Command | Example | What It Does |
|---------|---------|--------------|
| Set Reminder | "Remind me at 5 PM to call mom" | Create reminder |
| List Reminders | "What are my reminders?" | Show all reminders |
| Delete Reminder | "Cancel reminder about call" | Remove reminder |

---

## File Operations

### File Management

| Command | Example | What It Does |
|---------|---------|--------------|
| Open File | "Open notes.txt" | Open file in default app |
| Create File | "Create new note" | Create new file |
| Search Files | "Find PDF files" | Search for files by type |
| List Files | "Show my documents" | List directory contents |
| Delete File | "Delete old_file.txt" | Remove file |

### Folder Operations

| Command | Example | What It Does |
|---------|---------|--------------|
| Open Folder | "Open downloads folder" | Open directory |
| Organize Downloads | "Clean up downloads" | Organize file system |
| Show Desktop | "Show desktop files" | List desktop items |
| Go Home | "Open home folder" | Go to home directory |

---

## Communication

### Email

| Command | Example | What It Does |
|---------|---------|--------------|
| Send Email | "Send email to John" | Compose and send email |
| Check Email | "Show my emails" | List incoming emails |
| Read Email | "Read first email" | Read email aloud |
| Reply Email | "Reply to this email" | Reply to last email |

### Web Search

| Command | Example | What It Does |
|---------|---------|--------------|
| Search Web | "Search Python tutorials" | Search Google |
| Browse Site | "Open GitHub" | Open website |
| Show Results | "Show search results" | Display web results |

---

## System Control

### Display & Audio

| Command | Example | What It Does |
|---------|---------|--------------|
| Brightness Up | "Increase brightness" | Raise screen brightness |
| Brightness Down | "Decrease brightness" | Lower screen brightness |
| Volume Up | "Increase volume" | Raise audio volume |
| Volume Down | "Decrease volume" | Lower audio volume |
| Mute | "Mute audio" | Silence audio |
| Unmute | "Unmute" | Restore audio |

### Power & Lock

| Command | Example | What It Does |
|---------|---------|--------------|
| Lock | "Lock the computer" | Lock screen |
| Sleep | "Go to sleep" | Enter sleep mode |
| Restart | "Restart computer" | Reboot system |
| Shutdown | "Shut down" | Power off machine |

---

## Conversation & Learning

### Information Queries

| Command | Example | What It Does |
|---------|---------|--------------|
| Explain | "Explain quantum computing" | Get explanation |
| Define | "Define artificial intelligence" | Get definition |
| Tell Story | "Tell me a story" | Tell short story |
| Tell Joke | "Tell me a joke" | Tell joke |

### Conversation

| Command | Example | What It Does |
|---------|---------|--------------|
| Hello | "Hello IRIS" or "Hi" | Start conversation |
| Goodbye | "Goodbye" or "See you later" | Exit IRIS |
| How Are You | "How are you?" | Respond about status |
| Thanks | "Thank you" | Acknowledgment |

---

## Advanced Commands

### Multi-Step Automation

```
User: "Schedule a team meeting"
IRIS: "When would you like to schedule this?"
User: "Next Tuesday at 2 PM"
IRIS: "For how long?"
User: "One hour"
IRIS: "I've scheduled a 1-hour meeting for next Tuesday at 2 PM"
```

### Context-Aware Queries

```
User: "Open my project files from last week"
IRIS: Uses memory to find files you accessed last week

User: "What did I ask you about yesterday?"
IRIS: Retrieves from conversation history
```

### Natural Language Variations

All of these work the same:
- "Open Chrome" = "Launch Chrome" = "Start Chrome"
- "What time is it?" = "Tell me the time" = "Current time?"
- "Remind me at 5" = "Set reminder for 5 PM" = "Alert at 5 PM"

---

## Command Syntax

### Parameters

- **Time**: "2 PM", "14:00", "tomorrow at 3", "in 30 minutes"
- **Duration**: "1 hour", "30 minutes", "2 days"
- **Emails**: "john@example.com", "Jane at company.com"
- **Dates**: "tomorrow", "next Monday", "in 3 days", "April 15"
- **Files**: "document.txt", "~/Documents/file", "downloads/report.pdf"

### Optional Modifiers

- "with [person/app]" - Include recipient/application
- "to [destination]" - Specify target
- "about [topic]" - Specify subject
- "for [duration]" - Specify time period

---

## Tips & Tricks

1. **Be Natural** - IRIS understands natural language, not just commands
2. **Context Matters** - IRIS remembers previous conversations
3. **Follow-up Questions** - IRIS asks for clarification if needed
4. **Variations Work** - Try different phrasings of same command
5. **Combine Commands** - Chain multiple operations together

---

See [API Reference](API_REFERENCE.md) for programmatic usage and [Quick Start](QUICK_START.md) for beginner examples.
