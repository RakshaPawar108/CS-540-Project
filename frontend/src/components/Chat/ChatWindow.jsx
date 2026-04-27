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
