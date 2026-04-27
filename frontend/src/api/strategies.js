export const STRATEGIES = [
  {
    id: 'S1',
    label: 'S1 — Simple LLM',
    description: 'Sends your question directly to the LLM with no retrieval or conversation memory. Fast responses based purely on the model\'s training data.',
    endpoint: '/api/v1/chat/single-llm/',
    hasMemory: false,
    hasRAG: false,
  },
  {
    id: 'S2',
    label: 'S2 — Single RAG',
    description: 'Retrieves relevant PubMed abstracts before each response, grounding answers in medical literature. Each turn is independent — prior context is not retained.',
    endpoint: '/api/v1/chat/single-rag/',
    hasMemory: false,
    hasRAG: true,
  },
  {
    id: 'S3',
    label: 'S3 — Multi-Turn LLM',
    description: 'Maintains full conversation history across turns, enabling follow-up questions. Responses rely on model knowledge alone — no document retrieval.',
    endpoint: '/api/v1/chat/multi-turn-llm/',
    hasMemory: true,
    hasRAG: false,
  },
  {
    id: 'S4',
    label: 'S4 — Multi-Turn RAG',
    description: 'Combines PubMed retrieval with conversation memory. The most capable strategy for multi-turn medical Q&A grounded in clinical literature.',
    endpoint: '/api/v1/chat/multi-turn-rag/',
    hasMemory: true,
    hasRAG: true,
  },
];

export const DEFAULT_STRATEGY = STRATEGIES[0];

export function makeSessionId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}
