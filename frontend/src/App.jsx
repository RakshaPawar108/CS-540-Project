import { useState } from 'react';
import { useChat } from './hooks/useChat';
import { useCompare } from './hooks/useCompare';
import Header from './components/Header/Header';
import ChatWindow from './components/Chat/ChatWindow';
import CompareView from './components/Compare/CompareView';
import InputBar from './components/InputBar/InputBar';
import styles from './App.module.css';

export default function App() {
  const [compareMode, setCompareMode] = useState(false);
  const { strategy, messages, loading, handleSend, handleNewChat, handleStrategyChange } = useChat();
  const { columns, isAnyLoading, handleSend: handleCompareSend, handleNewChat: handleCompareNewChat } = useCompare();

  return (
    <div className={styles.app}>
      <Header
        strategy={strategy}
        onStrategyChange={handleStrategyChange}
        onNewChat={compareMode ? handleCompareNewChat : handleNewChat}
        compareMode={compareMode}
        onToggleCompare={() => setCompareMode(m => !m)}
      />
      {compareMode
        ? <CompareView columns={columns} />
        : <ChatWindow messages={messages} loading={loading} />
      }
      <InputBar
        onSend={compareMode ? handleCompareSend : handleSend}
        disabled={compareMode ? isAnyLoading : loading}
      />
    </div>
  );
}
