import { useChat } from './hooks/useChat';
import Header from './components/Header/Header';
import ChatWindow from './components/Chat/ChatWindow';
import InputBar from './components/InputBar/InputBar';
import styles from './App.module.css';

export default function App() {
  const { strategy, messages, loading, handleSend, handleNewChat, handleStrategyChange } = useChat();

  return (
    <div className={styles.app}>
      <Header
        strategy={strategy}
        onStrategyChange={handleStrategyChange}
        onNewChat={handleNewChat}
      />
      <ChatWindow messages={messages} loading={loading} />
      <InputBar onSend={handleSend} disabled={loading} />
    </div>
  );
}
