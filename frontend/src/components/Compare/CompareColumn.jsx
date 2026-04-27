import { useEffect, useRef } from 'react';
import MessageBubble from '../Chat/MessageBubble';
import TypingIndicator from '../Chat/TypingIndicator';
import styles from './CompareColumn.module.css';

const COLUMN_ACCENTS = ['#17a398', '#5b8ef0', '#e07b39', '#c45c8a'];

export default function CompareColumn({ strategy, messages, loading, colorIndex }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const lastLatencyMs = [...messages].reverse().find(m => m.role === 'assistant')?.latencyMs;
  const accent = COLUMN_ACCENTS[colorIndex] ?? COLUMN_ACCENTS[0];

  return (
    <div className={styles.column}>
      <div className={styles.columnHeader} style={{ borderBottomColor: accent }}>
        <span className={styles.label}>{strategy.label}</span>
        <div className={styles.badges}>
          <span className={`${styles.badge} ${strategy.hasRAG ? styles.badgeOn : styles.badgeOff}`}>
            RAG
          </span>
          <span className={`${styles.badge} ${strategy.hasMemory ? styles.badgeOn : styles.badgeOff}`}>
            Memory
          </span>
          {loading
            ? <span className={`${styles.badge} ${styles.badgeTimer}`} style={{ color: accent }}>…</span>
            : lastLatencyMs != null && (
              <span className={`${styles.badge} ${styles.badgeTimer}`} style={{ color: accent }}>
                {(lastLatencyMs / 1000).toFixed(1)}s
              </span>
            )
          }
        </div>
      </div>

      <div className={styles.messages}>
        {messages.length === 0 && !loading && (
          <p className={styles.empty}>Awaiting query…</p>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
