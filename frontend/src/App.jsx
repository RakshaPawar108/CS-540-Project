import { useState } from 'react';
import { useChat } from './hooks/useChat';
import { useCompare } from './hooks/useCompare';
import Header from './components/Header/Header';
import ChatWindow from './components/Chat/ChatWindow';
import CompareView from './components/Compare/CompareView';
import InputBar from './components/InputBar/InputBar';
import { SUGGESTED_QUESTIONS } from './constants/suggestedQuestions';
import styles from './App.module.css';

export default function App() {
  const [compareMode, setCompareMode] = useState(false);
  const { strategy, messages, loading, handleSend, handleNewChat, handleStrategyChange } = useChat();
  const { columns, isAnyLoading, handleSend: handleCompareSend, handleNewChat: handleCompareNewChat } = useCompare();

  const showCompareSuggestions =
    compareMode &&
    !isAnyLoading &&
    Object.values(columns).every(c => c.messages.length === 0);

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
        : <ChatWindow messages={messages} loading={loading} onSuggestedQuestion={handleSend} />
      }
      {showCompareSuggestions && (
        <div className={styles.compareSuggestions}>
          {SUGGESTED_QUESTIONS.map(q => (
            <button
              key={q}
              type="button"
              className={styles.compareSuggestionChip}
              onClick={() => handleCompareSend(q)}
            >
              {q}
            </button>
          ))}
        </div>
      )}
      <InputBar
        onSend={compareMode ? handleCompareSend : handleSend}
        disabled={compareMode ? isAnyLoading : loading}
      />
    </div>
  );
}
