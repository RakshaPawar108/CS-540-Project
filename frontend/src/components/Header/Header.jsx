import StrategySelector from './StrategySelector';
import styles from './Header.module.css';

export default function Header({ strategy, onStrategyChange, onNewChat, compareMode, onToggleCompare }) {
  return (
    <header className={styles.header}>
      <div className={styles.topRow}>
        <h1 className={styles.title}>Medical Chatbot — Strategy Comparison</h1>
      </div>

      <div className={styles.bottomRow}>
        {compareMode
          ? <span className={styles.compareActive}>All 4 strategies active</span>
          : <StrategySelector strategy={strategy} onChange={onStrategyChange} />
        }
        <div className={styles.actions}>
          <button
            type="button"
            className={`${styles.compareBtn} ${compareMode ? styles.compareBtnActive : ''}`}
            onClick={onToggleCompare}
            title={compareMode ? 'Exit compare mode' : 'Compare all strategies side by side'}
          >
            {compareMode ? 'Exit Compare' : 'Compare All'}
          </button>
          <button
            type="button"
            className={styles.newChatBtn}
            onClick={onNewChat}
            title="Start a new conversation"
          >
            New Chat
          </button>
        </div>
      </div>

      <div className={styles.tealStripe} />
    </header>
  );
}
