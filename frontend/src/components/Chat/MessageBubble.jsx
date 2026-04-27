import ReactMarkdown from 'react-markdown';
import Avatar from './Avatar';
import SourceChunks from './SourceChunks';
import styles from './MessageBubble.module.css';

export default function MessageBubble({ message }) {
  const { role, content, chunks, isError, latencyMs } = message;
  const isUser = role === 'user';

  return (
    <div className={`${styles.row} ${isUser ? styles.userRow : styles.assistantRow}`}>
      {!isUser && <Avatar role="assistant" />}

      <div className={`${styles.bubble} ${isUser ? styles.userBubble : styles.assistantBubble} ${isError ? styles.errorBubble : ''}`}>
        {isUser
          ? <p className={styles.text}>{content}</p>
          : <div className={styles.markdown}><ReactMarkdown>{content}</ReactMarkdown></div>
        }
        {!isUser && <SourceChunks chunks={chunks} />}
        {!isUser && latencyMs != null && (
          <span className={styles.latency}>{(latencyMs / 1000).toFixed(1)}s</span>
        )}
      </div>

      {isUser && <Avatar role="user" />}
    </div>
  );
}
