import ReactMarkdown from 'react-markdown';
import Avatar from './Avatar';
import SourceChunks from './SourceChunks';
import styles from './MessageBubble.module.css';

export default function MessageBubble({ message }) {
  const { role, content, chunks, isError } = message;
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
      </div>

      {isUser && <Avatar role="user" />}
    </div>
  );
}
