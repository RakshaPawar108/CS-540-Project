import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import styles from './ChatWindow.module.css';

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <main className={styles.window} aria-live="polite" aria-label="Chat messages">
      {messages.length === 0 && !loading && (
        <div className={styles.empty}>
          <p className={styles.emptyText}>Ask a medical question to get started.</p>
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
