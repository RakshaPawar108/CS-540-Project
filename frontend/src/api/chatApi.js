async function postJSON(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed with status ${res.status}`);
  }

  return res.json();
}

export async function sendMessage({ strategy, query, sessionId, topK = 5 }) {
  const { id, endpoint } = strategy;

  const bodyByStrategy = {
    S1: { query },
    S2: { query, top_k: topK },
    S3: { session_id: sessionId, query },
    S4: { session_id: sessionId, query, top_k: topK },
  };

  return postJSON(endpoint, bodyByStrategy[id]);
}

export async function clearSession(strategy, sessionId) {
  if (!strategy.hasMemory) return;

  const baseByStrategy = {
    S3: '/api/v1/chat/multi-turn-llm',
    S4: '/api/v1/chat/multi-turn-rag',
  };

  const base = baseByStrategy[strategy.id];
  if (!base) return;

  await fetch(`${base}/${sessionId}`, { method: 'DELETE' }).catch(() => {});
}
