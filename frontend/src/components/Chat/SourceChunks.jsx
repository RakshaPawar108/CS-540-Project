import { useState } from 'react';
import styles from './SourceChunks.module.css';

function scoreColorClass(score) {
  if (score >= 0.75) return styles.scoreHigh;
  if (score >= 0.50) return styles.scoreMid;
  return styles.scoreLow;
}

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
                <div className={styles.scoreBar}>
                  <div className={styles.scoreTrack}>
                    <div
                      className={`${styles.scoreFill} ${scoreColorClass(chunk.score)}`}
                      style={{ width: `${(chunk.score * 100).toFixed(0)}%` }}
                    />
                  </div>
                  <span className={styles.scoreText}>{(chunk.score * 100).toFixed(0)}%</span>
                </div>
              </div>
              <p className={styles.content}>{chunk.content}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
