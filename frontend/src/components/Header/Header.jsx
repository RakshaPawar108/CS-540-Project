import WindowControls from './WindowControls';
import StrategySelector from './StrategySelector';
import styles from './Header.module.css';

export default function Header({ strategy, onStrategyChange, onNewChat }) {
  return (
    <header className={styles.header}>
      <div className={styles.topRow}>
        <WindowControls />
        <h1 className={styles.title}>Medical Chatbot — Strategy Comparison</h1>
      </div>

      <div className={styles.bottomRow}>
        <StrategySelector strategy={strategy} onChange={onStrategyChange} />
        <button
          type="button"
          className={styles.newChatBtn}
          onClick={onNewChat}
          title="Start a new conversation"
        >
          New Chat
        </button>
      </div>

      <div className={styles.tealStripe} />
    </header>
  );
}
