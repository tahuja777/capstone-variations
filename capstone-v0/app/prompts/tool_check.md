## 4. `tool_check.md` — Tool Justification & Hallucination Control
Used for tool validation and ensuring the model trusts real data sources.

```markdown
# Tool Justification Prompt

Before finalizing your answer, confirm that each statement is backed by either:
- Tool output (JSON data), or
- Document evidence (chunk IDs or file names).

## Self-Verification Steps
1. Compare the final answer against all evidence items.
2. If any statement lacks evidence, flag it.

## Response Format
```json
{
  "verified": true | false,
  "missing_evidence_for": ["<list of unsupported claims>"],
  "confidence_score": "<0-1>"
}
