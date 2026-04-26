import { useState, useCallback, useRef } from 'react';
import { STRATEGIES, makeSessionId } from '../api/strategies';
import { sendMessage, clearSession } from '../api/chatApi';

const makeInitialColumns = () =>
  Object.fromEntries(STRATEGIES.map(s => [s.id, { messages: [], loading: false }]));

export function useCompare() {
  const [columns, setColumns] = useState(makeInitialColumns);
  const sessionIds = useRef(Object.fromEntries(STRATEGIES.map(s => [s.id, makeSessionId()])));
  const isLoadingRef = useRef(false);

  const handleSend = useCallback(async (text) => {
    if (!text.trim() || isLoadingRef.current) return;
    isLoadingRef.current = true;

    const userMessage = { role: 'user', content: text };

    setColumns(prev =>
      Object.fromEntries(
        STRATEGIES.map(s => [
          s.id,
          { messages: [...prev[s.id].messages, userMessage], loading: true },
        ])
      )
    );

    await Promise.allSettled(
      STRATEGIES.map(async (strategy) => {
        try {
          const data = await sendMessage({
            strategy,
            query: text,
            sessionId: sessionIds.current[strategy.id],
          });

          setColumns(prev => ({
            ...prev,
            [strategy.id]: {
              loading: false,
              messages: [
                ...prev[strategy.id].messages,
                {
                  role: 'assistant',
                  content: data.answer,
                  chunks: data.retrieved_chunks ?? [],
                  meta: {
                    strategy: data.strategy,
                    model: data.model,
                    historyLength: data.history_length,
                  },
                },
              ],
            },
          }));
        } catch (err) {
          setColumns(prev => ({
            ...prev,
            [strategy.id]: {
              loading: false,
              messages: [
                ...prev[strategy.id].messages,
                { role: 'assistant', content: err.message, isError: true },
              ],
            },
          }));
        }
      })
    );

    isLoadingRef.current = false;
  }, []);

  const handleNewChat = useCallback(() => {
    STRATEGIES.forEach(s => {
      if (s.hasMemory) {
        clearSession(s, sessionIds.current[s.id]).catch(() => {});
      }
      sessionIds.current[s.id] = makeSessionId();
    });
    setColumns(makeInitialColumns());
  }, []);

  const isAnyLoading = Object.values(columns).some(c => c.loading);

  return { columns, isAnyLoading, handleSend, handleNewChat };
}
