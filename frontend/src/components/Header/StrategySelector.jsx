import { useState, useEffect, useRef } from 'react';
import { STRATEGIES } from '../../api/strategies';
import styles from './StrategySelector.module.css';

export default function StrategySelector({ strategy, onChange }) {
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    const handleClick = (e) => {
      if (!wrapperRef.current?.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [open]);

  return (
    <div className={styles.wrapper} ref={wrapperRef}>
      <label htmlFor="strategy-select" className={styles.label}>
        Strategy:
      </label>
      <select
        id="strategy-select"
        className={styles.select}
        value={strategy.id}
        onChange={e => onChange(STRATEGIES.find(s => s.id === e.target.value))}
      >
        {STRATEGIES.map(s => (
          <option key={s.id} value={s.id}>
            {s.label}
          </option>
        ))}
      </select>

      <button
        type="button"
        className={styles.infoBtn}
        onClick={() => setOpen(o => !o)}
        aria-label="Strategy descriptions"
        aria-expanded={open}
      >
        ⓘ
      </button>

      {open && (
        <div className={styles.popover} role="dialog" aria-label="Strategy descriptions">
          {STRATEGIES.map(s => (
            <div key={s.id} className={styles.popoverItem}>
              <div className={styles.popoverHeader}>
                <span className={styles.popoverLabel}>{s.label}</span>
                <div className={styles.popoverBadges}>
                  <span className={`${styles.popoverBadge} ${s.hasRAG ? styles.badgeOn : styles.badgeOff}`}>RAG</span>
                  <span className={`${styles.popoverBadge} ${s.hasMemory ? styles.badgeOn : styles.badgeOff}`}>Memory</span>
                </div>
              </div>
              <p className={styles.popoverDesc}>{s.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
