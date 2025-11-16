
---

## `rag_synth.md` — RAG Synthesis Prompt
Used by the **Synthesize Node** to generate final answers from evidence or tool output.

```markdown
# RAG Synthesis Prompt

You will synthesize a final customer answer using the retrieved **evidence** and current **state**.

## Instructions
1. Combine all provided evidence into a coherent summary.
2. Verify facts for consistency and completeness.
3. If conflicting evidence exists, prefer the most specific or recent one.
4. Never hallucinate or assume missing data — instead state:
   "_The information is not available in the retrieved records._"

## Format
Respond in JSON:

```json
{
  "answer": "<clear response text>",
  "evidence_used": ["<list of evidence references>"],
  "hallucination_check": "<Passed | Potential Issue>"
}
