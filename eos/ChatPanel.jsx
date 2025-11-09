import './ChatPanel.css';

function ChatPanel({ question, setQuestion, answer, loading, error, onSubmit, onClear }) {
  return (
    <div className="chat-panel">
      <div className="chat-header">
        <svg className="chat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3>Ask a Question</h3>
      </div>

      <form onSubmit={onSubmit} className="chat-input-group">
        <textarea
          className="chat-textarea"
          placeholder="Ask about any concept in the video..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
        />
        <button
          type="submit"
          className="btn btn-primary chat-submit"
          disabled={loading || !question.trim()}
        >
          {loading ? (
            <>
              <div className="mini-spinner"></div>
              Thinking...
            </>
          ) : (
            'Ask'
          )}
        </button>
      </form>

      {error && (
        <div className="chat-error">
          {error}
        </div>
      )}

      {answer && (
        <div className="chat-answer">
          <div className="answer-header">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Answer
          </div>
          <p className="answer-text">{answer.text}</p>
          <button onClick={onClear} className="btn btn-secondary" style={{ marginTop: '12px', width: '100%' }}>
            Clear
          </button>
        </div>
      )}
    </div>
  );
}

export default ChatPanel;