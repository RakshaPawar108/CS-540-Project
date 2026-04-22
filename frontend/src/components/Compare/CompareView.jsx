import { STRATEGIES } from '../../api/strategies';
import CompareColumn from './CompareColumn';
import styles from './CompareView.module.css';

export default function CompareView({ columns }) {
  return (
    <div className={styles.grid}>
      {STRATEGIES.map(strategy => (
        <CompareColumn
          key={strategy.id}
          strategy={strategy}
          messages={columns[strategy.id].messages}
          loading={columns[strategy.id].loading}
        />
      ))}
    </div>
  );
}
