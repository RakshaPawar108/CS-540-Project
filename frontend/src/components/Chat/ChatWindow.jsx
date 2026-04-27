import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import { SUGGESTED_QUESTIONS } from '../../constants/suggestedQuestions';
import styles from './ChatWindow.module.css';

export default function ChatWindow({ messages, loading, onSuggestedQuestion }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <main className={styles.window} aria-live="polite" aria-label="Chat messages">
      {messages.length === 0 && !loading && (
        <div className={styles.empty}>
          <div className={styles.emptyIcon} aria-hidden="true">
            <svg viewBox="0 0 48 48" fill="currentColor" width="64" height="64">
              <rect x="18" y="4" width="12" height="40" rx="3" />
              <rect x="4" y="18" width="40" height="12" rx="3" />
            </svg>
          </div>
          <p className={styles.emptyText}>Ask a medical question to get started.</p>
          <div className={styles.suggestions}>
            {SUGGESTED_QUESTIONS.map((q) => (
              <button
                key={q}
                type="button"
                className={styles.suggestionChip}
                onClick={() => onSuggestedQuestion(q)}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {messages.map((msg, i) => (
        <MessageBubble key={i} message={msg} />
      ))}

      {loading && <TypingIndicator />}

      <div ref={bottomRef} />
    </main>
  );
}
