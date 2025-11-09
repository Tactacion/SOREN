// frontend/static/chat.js

let videoPlayer;
let chatPanel;
let askButton;
let questionInput;
let sendButton;
let chatMessages;
let currentJobId;
let currentVideoNumber;
let pausedTimestamp;

function initVideoPlayer(jobId, videoNumber) {
    currentJobId = jobId;
    currentVideoNumber = videoNumber;
    
    // Get DOM elements
    videoPlayer = document.getElementById('videoPlayer');
    chatPanel = document.getElementById('chatPanel');
    askButton = document.getElementById('askButton');
    questionInput = document.getElementById('questionInput');
    sendButton = document.getElementById('sendQuestion');
    chatMessages = document.getElementById('chatMessages');
    
    // Event listeners
    askButton.addEventListener('click', openChat);
    document.getElementById('closeChat').addEventListener('click', closeChat);
    sendButton.addEventListener('click', sendQuestion);
    questionInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });
    
    // Update timestamp display
    videoPlayer.addEventListener('timeupdate', updateTimestamp);
}

function updateTimestamp() {
    const time = videoPlayer.currentTime.toFixed(1);
    document.getElementById('timestamp').textContent = `Current time: ${time}s`;
}

function openChat() {
    // Pause video
    videoPlayer.pause();
    pausedTimestamp = videoPlayer.currentTime;
    
    // Show chat panel
    chatPanel.classList.remove('hidden');
    
    // Update paused time display
    document.getElementById('pausedTime').textContent = pausedTimestamp.toFixed(1);
    
    // Focus input
    questionInput.focus();
}

function closeChat() {
    chatPanel.classList.add('hidden');
}

async function sendQuestion() {
    const question = questionInput.value.trim();
    if (!question) return;
    
    // Disable input
    questionInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message
    addMessage('user', question);
    questionInput.value = '';
    
    // Add loading indicator
    addMessage('loading', 'Thinking...');
    
    try {
        // Call API
        const response = await fetch('/api/ask-doubt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                job_id: currentJobId,
                video_number: currentVideoNumber,
                timestamp: pausedTimestamp,
                question: question,
                context_window: 15
            })
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        const data = await response.json();
        
        // Remove loading
        removeLastMessage();
        
        // Add assistant response
        addMessage('assistant', data.answer);
        
    } catch (error) {
        // Remove loading
        removeLastMessage();
        
        // Show error
        addMessage('error', 'Sorry, there was an error processing your question. Please try again.');
        console.error('Error:', error);
    }
    
    // Re-enable input
    questionInput.disabled = false;
    sendButton.disabled = false;
    questionInput.focus();
}

function addMessage(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
    if (type === 'user') {
        messageDiv.innerHTML = `<div class="user-message">${escapeHtml(content)}</div>`;
    } else if (type === 'assistant') {
        messageDiv.innerHTML = `<div class="assistant-message">${formatMarkdown(content)}</div>`;
    } else if (type === 'loading') {
        messageDiv.innerHTML = `<div class="assistant-message">
            <span class="loading"></span>
            <span class="loading" style="animation-delay: 0.2s"></span>
            <span class="loading" style="animation-delay: 0.4s"></span>
        </div>`;
        messageDiv.id = 'loading-message';
    } else if (type === 'error') {
        messageDiv.innerHTML = `<div class="system-message" style="background: #ffebee; color: #c62828;">${escapeHtml(content)}</div>`;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeLastMessage() {
    const loading = document.getElementById('loading-message');
    if (loading) {
        loading.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatMarkdown(text) {
    // Basic markdown formatting
    text = escapeHtml(text);
    
    // Bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Code
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Line breaks
    text = text.replace(/\n\n/g, '</p><p>');
    text = text.replace(/\n/g, '<br>');
    
    return '<p>' + text + '</p>';
}