import styles from './Avatar.module.css';

function UserIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15" aria-hidden="true">
      <circle cx="10" cy="6" r="4" />
      <path d="M2 18c0-4.4 3.6-8 8-8s8 3.6 8 8" />
    </svg>
  );
}

function MedicalIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15" aria-hidden="true">
      <rect x="7.5" y="2" width="5" height="16" rx="1.5" />
      <rect x="2" y="7.5" width="16" height="5" rx="1.5" />
    </svg>
  );
}

export default function Avatar({ role }) {
  return (
    <div
      className={`${styles.avatar} ${role === 'user' ? styles.user : styles.assistant}`}
      aria-hidden="true"
    >
      {role === 'user' ? <UserIcon /> : <MedicalIcon />}
    </div>
  );
}
