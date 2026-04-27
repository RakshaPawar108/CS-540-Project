import { useState, useCallback, useRef } from 'react';
import { DEFAULT_STRATEGY, makeSessionId } from '../api/strategies';
import { sendMessage, clearSession } from '../api/chatApi';

export function useChat() {
  const [strategy, setStrategy] = useState(DEFAULT_STRATEGY);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const sessionIdRef = useRef(makeSessionId());

  const resetSession = useCallback(async (currentStrategy, currentMessages) => {
    if (currentStrategy.hasMemory && currentMessages.length > 0) {
      await clearSession(currentStrategy, sessionIdRef.current);
    }
    sessionIdRef.current = makeSessionId();
    setMessages([]);
  }, []);

  const handleNewChat = useCallback(() => {
    resetSession(strategy, messages);
  }, [strategy, messages, resetSession]);

  const handleStrategyChange = useCallback(async (newStrategy) => {
    await resetSession(strategy, messages);
    setStrategy(newStrategy);
  }, [strategy, messages, resetSession]);

  const handleSend = useCallback(async (text) => {
    if (!text.trim() || loading) return;

    const userMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    const start = Date.now();

    try {
      const data = await sendMessage({
        strategy,
        query: text,
        sessionId: sessionIdRef.current,
      });

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          chunks: data.retrieved_chunks ?? [],
          latencyMs: Date.now() - start,
          meta: {
            strategy: data.strategy,
            model: data.model,
            historyLength: data.history_length,
          },
        },
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: err.message, isError: true, latencyMs: Date.now() - start },
      ]);
    } finally {
      setLoading(false);
    }
  }, [strategy, loading]);

  return {
    strategy,
    messages,
    loading,
    handleSend,
    handleNewChat,
    handleStrategyChange,
  };
}
