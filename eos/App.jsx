import { GridScan } from './GridScan';
import { useNavigate } from 'react-router-dom';
import Header from './Header';
import ChatPanel from './components/ChatPanel';
import './App.css';
import { useState, useRef, useEffect } from 'react';

function App() {
  const navigate = useNavigate();
  const [uploadState, setUploadState] = useState('initial');
  const [fileInfo, setFileInfo] = useState({ name: '', size: '' });
  const fileInputRef = useRef(null);
  const [generationStage, setGenerationStage] = useState('');
  const [progress, setProgress] = useState(0);

  // Video and Q&A states
  const [videoUrl, setVideoUrl] = useState('');
  const [videoId, setVideoId] = useState('');
  const [uploadedPdfName, setUploadedPdfName] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [isAsking, setIsAsking] = useState(false);
  const [qaError, setQaError] = useState(null);
  const videoRef = useRef(null);

  // Mode toggle (hidden from UI but works in background)
  const [mode, setMode] = useState('demo');
  const keyPressCount = useRef(0);
  const keyPressTimer = useRef(null);

  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.key === 'd' || e.key === 'D') {
        keyPressCount.current += 1;

        if (keyPressCount.current === 3) {
          setMode(prev => {
            const newMode = prev === 'demo' ? 'real' : 'demo';
            console.log(`🔧 Mode switched to: ${newMode.toUpperCase()}`);
            return newMode;
          });
          keyPressCount.current = 0;
        }

        clearTimeout(keyPressTimer.current);
        keyPressTimer.current = setTimeout(() => {
          keyPressCount.current = 0;
        }, 1000);
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => {
      window.removeEventListener('keydown', handleKeyPress);
      clearTimeout(keyPressTimer.current);
    };
  }, []);

  // Map PDF to video
  const getVideoForPdf = (pdfFileName) => {
    const name = pdfFileName.toLowerCase();
    
    console.log('==========================================');
    console.log(`📄 PDF: "${pdfFileName}"`);
    
    if (name.includes('lora')) {
      console.log('✅ LoRA Paper → LoRA Video');
      return {
        videoPath: '/output/lorapaper/media/videos/video1/1080p60/Video1.mp4',
        videoId: 'video1_lorapaper',
        contextPdf: 'lorapaper.pdf',
        contextCode: 'output/lorapaper/video1.py',
        outputFolder: 'lorapaper'
      };
    } else {
      console.log('✅ Other PDF → GAG Video');
      return {
        videoPath: '/output/gag/media/videos/video1/1080p60/Video2.mp4',
        videoId: 'video2_gag',
        contextPdf: 'gag.pdf',
        contextCode: 'output/gag/video1.py',
        outputFolder: 'gag'
      };
    }
  };

  const handleFile = async (file) => {
    if (file && file.type === 'application/pdf') {
      setUploadState('loading');
      setProgress(0);

      const videoMapping = getVideoForPdf(file.name);
      console.log('🎬 Video:', videoMapping.videoPath);

      if (mode === 'demo') {
        const stages = [
          { text: 'Analyzing PDF...', duration: 600, progress: 20 },
          { text: 'Extracting concepts...', duration: 800, progress: 50 },
          { text: 'Generating animation...', duration: 1000, progress: 80 },
          { text: 'Finalizing...', duration: 400, progress: 100 }
        ];

        for (const stage of stages) {
          setGenerationStage(stage.text);
          setProgress(stage.progress);
          await new Promise(resolve => setTimeout(resolve, stage.duration));
        }

        setFileInfo({
          name: file.name,
          size: (file.size / 1024 / 1024).toFixed(2) + ' MB'
        });
        setUploadedPdfName(file.name);
        setVideoUrl(videoMapping.videoPath);
        setVideoId(videoMapping.videoId);
        setUploadState('success');
        setGenerationStage('');
        setAnswer(null);
        setQuestion('');
      } else {
        try {
          const formData = new FormData();
          formData.append('file', file);

          setGenerationStage('Uploading...');
          setProgress(5);

          const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
          });

          const data = await response.json();

          if (data.success) {
            setFileInfo({
              name: file.name,
              size: (file.size / 1024 / 1024).toFixed(2) + ' MB'
            });
            setUploadedPdfName(file.name);
            setVideoUrl(data.video_path);
            setVideoId(data.video_id);
            setUploadState('success');
            setGenerationStage('');
            setProgress(100);
            setAnswer(null);
            setQuestion('');
          } else {
            alert('Error: ' + (data.error || 'Failed'));
            setUploadState('initial');
          }
        } catch (error) {
          console.error('Upload error:', error);
          alert('Failed: ' + error.message);
          setUploadState('initial');
        }
      }
    } else {
      alert('Please upload a PDF file');
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files.length) {
      handleFile(e.target.files[0]);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length) {
      handleFile(files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const resetUpload = () => {
    setUploadState('initial');
    setFileInfo({ name: '', size: '' });
    setVideoUrl('');
    setVideoId('');
    setUploadedPdfName('');
    setAnswer(null);
    setQuestion('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const downloadVideo = () => {
    if (videoUrl) {
      const link = document.createElement('a');
      link.href = videoUrl;
      link.download = `generated_video.mp4`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handleAskQuestion = async (e) => {
    e.preventDefault();

    if (!question.trim()) {
      return;
    }

    setIsAsking(true);
    setAnswer(null);
    setQaError(null);

    try {
      const currentTime = videoRef.current ? videoRef.current.currentTime : 0;
      const videoMapping = getVideoForPdf(uploadedPdfName);

      console.log('❓ Question:', question);
      console.log('📚 Context:', videoMapping.contextPdf);
      console.log('⏱️ Timestamp:', Math.floor(currentTime), 's');

      // BOTH demo and real mode use the backend!
      console.log('🔄 Fetching context from backend...');
      
      const contextResponse = await fetch('/api/context', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          pdf_name: videoMapping.contextPdf,
          output_folder: videoMapping.outputFolder,
          video_id: videoId
        })
      });

      const contextData = await contextResponse.json();
      console.log('📦 Context loaded:', contextData.success);

      if (!contextData.success) {
        throw new Error('Could not load context from backend');
      }

      console.log('🤖 Asking Claude AI...');

      const response = await fetch('/api/doubt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          video_id: videoId,
          timestamp: currentTime,
          extra_context: {
            pdf_text: contextData.context.pdf_text,
            manim_code: contextData.context.manim_code,
            pdf_name: videoMapping.contextPdf,
            output_folder: videoMapping.outputFolder
          }
        })
      });

      const data = await response.json();

      if (data.success) {
        setAnswer({
          text: data.answer,
          sources: data.sources,
          context: data.context_used,
        });
        console.log('✅ Answer received!');
      } else {
        setQaError(data.error || 'Failed to get answer');
      }
    } catch (error) {
      console.error('❌ Error:', error);
      setQaError(`Could not reach backend server. Make sure it's running on port 5001:\n\ncd backend\npython server.py`);
    } finally {
      setIsAsking(false);
    }
  };

  const clearAnswer = () => {
    setAnswer(null);
    setQuestion('');
    setQaError(null);
  };

  const goToSamples = () => {
    navigate('/samples');
  };

  return (
    <div className="app">
      <div className="grid-container">
        <GridScan
          sensitivity={0.3}
          lineThickness={1}
          linesColor="#888888"
          gridScale={0.08}
          scanColor="#aaaaaa"
          scanOpacity={0.4}
          enablePost={true}
          bloomIntensity={0.3}
          bloomThreshold={0.5}
          chromaticAberration={0.001}
          scanDirection="pingpong"
          scanDuration={1.5}
          scanDelay={0.2}
          lineJitter={0.15}
          noiseIntensity={0.02}
          scanGlow={1.0}
          scanSoftness={0.8}
        />
      </div>
      
      <Header />
      
      <div className="content">
        <div className="hero">
          <div className="hero-badge">
            ✨ AI EDITING MODELS
          </div>
          <h2 className="hero-title">
            Soren - Your Concept Mentor
          </h2>
          <p className="hero-description">
            Soren distills your PDFs into clear, bite-sized animated lessons.
          </p>
        </div>

        <div className="demo-card">
          <div className="demo-label">Upload Document</div>
          <div className="demo-content">
            {uploadState === 'initial' && (
              <div className="upload-zone-wrapper">
                <label 
                  htmlFor="fileInput" 
                  className="upload-zone"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                >
                  <div className="upload-icon-circle">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                    </svg>
                  </div>
                  <p className="upload-text">Drop your PDF here</p>
                  <p className="upload-subtext">or click to browse</p>
                </label>

                <input 
                  type="file" 
                  id="fileInput" 
                  ref={fileInputRef}
                  className="file-input" 
                  accept=".pdf"
                  onChange={handleFileInput}
                />

                <div className="features-section">
                  <div className="features-grid">
                    <div className="feature-item">
                      <div className="feature-icon-wrapper">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                      </div>
                      <h3 className="feature-title">Smart Parsing</h3>
                      <p className="feature-description">AI extracts key concepts</p>
                    </div>
                    <div className="feature-item">
                      <div className="feature-icon-wrapper">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                        </svg>
                      </div>
                      <h3 className="feature-title">Manim Animation</h3>
                      <p className="feature-description">Beautiful visualizations</p>
                    </div>
                    <div className="feature-item">
                      <div className="feature-icon-wrapper">
                        <svg fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2L9 9L2 12L9 15L12 22L15 15L22 12L15 9L12 2Z"></path>
                        </svg>
                      </div>
                      <h3 className="feature-title">AI Voiceover</h3>
                      <p className="feature-description">Natural narration</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {uploadState === 'loading' && (
              <div className="loading-content">
                <div className="loading-spinner"></div>
                <p className="upload-text">{generationStage || 'Processing...'}</p>
                <p className="upload-subtext">Progress: {progress}%</p>
                <div style={{
                  width: '100%',
                  maxWidth: '400px',
                  height: '4px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  borderRadius: '2px',
                  marginTop: '12px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${progress}%`,
                    height: '100%',
                    background: '#ffffff',
                    transition: 'width 0.3s ease'
                  }}></div>
                </div>
              </div>
            )}

            {uploadState === 'success' && (
              <div className="success-content-wrapper">
                <div className="success-header">
                  <div className="success-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                  <p className="upload-text">Video Ready!</p>
                  <div className="file-info">
                    <svg className="file-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <div className="file-details">
                      <p className="file-name">{fileInfo.name}</p>
                      <p className="file-size">{fileInfo.size}</p>
                    </div>
                  </div>
                </div>

                <div className="split-screen-container">
                  <div className="video-section-split">
                    <video
                      ref={videoRef}
                      controls
                      className="generated-video"
                      key={videoUrl}
                    >
                      <source src={videoUrl} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                    <div className="button-group">
                      <button className="btn btn-primary" onClick={downloadVideo}>Download</button>
                      <button className="btn btn-secondary" onClick={resetUpload}>New Upload</button>
                    </div>
                  </div>

                  <ChatPanel
                    question={question}
                    setQuestion={setQuestion}
                    answer={answer}
                    loading={isAsking}
                    error={qaError}
                    onSubmit={handleAskQuestion}
                    onClear={clearAnswer}
                  />
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="view-samples-section">
          <button className="view-samples-btn" onClick={goToSamples}>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
            View Sample Outputs
          </button>
        </div>

        <footer className="footer">
          <p className="footer-text">Built for learners, creators, and educators – powered by AI clarity✨</p>
        </footer>
      </div>
    </div>
  );
}

export default App;