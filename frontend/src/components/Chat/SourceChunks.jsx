import { useState } from 'react';
import styles from './SourceChunks.module.css';

export default function SourceChunks({ chunks }) {
  const [open, setOpen] = useState(false);

  if (!chunks || chunks.length === 0) return null;

  return (
    <div className={styles.wrapper}>
      <button
        type="button"
        className={styles.toggle}
        onClick={() => setOpen(o => !o)}
        aria-expanded={open}
      >
        <span className={styles.icon}>{open ? '▾' : '▸'}</span>
        {chunks.length} source{chunks.length !== 1 ? 's' : ''} retrieved
      </button>

      {open && (
        <ul className={styles.list}>
          {chunks.map((chunk, i) => (
            <li key={i} className={styles.chunk}>
              <div className={styles.chunkHeader}>
                <span className={styles.source}>PubMed: {chunk.source}</span>
                <span className={styles.score}>{(chunk.score * 100).toFixed(0)}% match</span>
              </div>
              <p className={styles.content}>{chunk.content}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
