## Guilherme Rubatto Camargo

AI Engineer building LLM systems in production — RAG, tool-calling agents, and
the part most people skip: measuring whether they actually work.

Software Engineering student at SENAI FATESG · Goiânia, Brazil

---

### edital-radar — what I'm building now

An assistant that monitors Brazilian public tenders and surfaces the few a
software vendor could realistically win. ~1,100 tenders are published per day;
a vendor can serve maybe 3.

- **US$0.0031 per judgment** — a three-stage cascade where a free local filter
  discards 69% of the corpus before the paid model sees anything
- **The evaluation set was written before the pipeline**, then used to compare
  models: Haiku 4.5 → Sonnet 5 moved recall from 0.692 to 0.846 on an
  identical prompt and schema
- **A CI regression gate** that fails the build when measured quality drops —
  verified by breaking it on purpose
- **Langfuse tracing** with per-call cost reconciled exactly against an
  independent ledger, surfaced on a `/metrics` panel

→ **[github.com/Rubatto-Dev/edital-radar](https://github.com/Rubatto-Dev/edital-radar)**

---

### Also here

- **[JobRadar](https://github.com/Rubatto-Dev/JobRadar)** — job aggregation
  across Gupy and Remotive, with alerts and application tracking
- **[assistente-delivery-bedrock](https://github.com/Rubatto-Dev/assistente-delivery-bedrock)** —
  serverless delivery assistant on AWS Step Functions + Amazon Bedrock
- **[disparo_whatsapp](https://github.com/Rubatto-Dev/disparo_whatsapp)** —
  WhatsApp automation with n8n and Evolution API

---

### Stack

Python (FastAPI, SQLAlchemy) · PostgreSQL, pgvector · Node.js, TypeScript ·
React, Next.js · Docker · GitHub Actions · Langfuse

---

### Contact

[LinkedIn](https://linkedin.com/in/guirubatto) ·
rubattodev@gmail.com
