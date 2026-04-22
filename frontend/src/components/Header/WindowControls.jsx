import styles from './WindowControls.module.css';

export default function WindowControls() {
  return (
    <div className={styles.controls} aria-hidden="true">
      <span className={`${styles.dot} ${styles.red}`} />
      <span className={`${styles.dot} ${styles.orange}`} />
      <span className={`${styles.dot} ${styles.green}`} />
    </div>
  );
}
