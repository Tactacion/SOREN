import { useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from './Header';
import ChatPanel from './components/ChatPanel';
import { GridScan } from './GridScan';
import './VideoPlayer.css';

function VideoPlayer() {
  const { videoId } = useParams();
  const navigate = useNavigate();
  const videoRef = useRef(null);

  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Metadata for LDM sample
  const metadata = {
    title: 'LDM: Latent Diffusion Models',
    description: 'High-Resolution Image Synthesis with Latent Diffusion Models - A comprehensive explanation of how latent diffusion models work for generating high-quality images.',
    key_concepts: ['Latent Space', 'Diffusion Process', 'U-Net Architecture', 'Stable Diffusion']
  };

  const videoPath = '/output/ldm/media/videos/video1/480p15/Video1.mp4';

  const handleAskQuestion = async (e) => {
    e.preventDefault();

    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const currentTime = videoRef.current ? videoRef.current.currentTime : 0;

      // Call backend for real AI responses
      const contextResponse = await fetch('/api/context', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          pdf_name: 'ldm.pdf',
          output_folder: 'ldm',
          video_id: 'ldm_sample'
        })
      });

      const contextData = await contextResponse.json();

      if (!contextData.success) {
        throw new Error('Could not load context');
      }

      const response = await fetch('/api/doubt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          video_id: 'ldm_sample',
          timestamp: currentTime,
          extra_context: {
            pdf_text: contextData.context.pdf_text,
            manim_code: contextData.context.manim_code,
            pdf_name: 'ldm.pdf',
            output_folder: 'ldm'
          }
        })
      });

      const data = await response.json();

      if (data.success) {
        setAnswer({
          text: data.answer,
          sources: data.sources,
          context: data.context_used
        });
      } else {
        setError(data.error || 'Failed to get answer');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Could not reach backend. Make sure server is running on port 5001.');
    } finally {
      setLoading(false);
    }
  };

  const clearAnswer = () => {
    setAnswer(null);
    setQuestion('');
    setError(null);
  };

  return (
    <div className="video-player-page">
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

      <div className="video-player-content">
        <div className="player-header">
          <button onClick={() => navigate('/samples')} className="back-btn">
            ← Back to Samples
          </button>
          <h1>{metadata.title}</h1>
        </div>

        <div className="player-layout">
          <div className="video-section">
            <video
              ref={videoRef}
              controls
              className="main-video"
              src={videoPath}
            >
              <source src={videoPath} type="video/mp4" />
              Your browser does not support the video tag.
            </video>

            <div className="video-info">
              <h3>About</h3>
              <p>{metadata.description}</p>
            </div>

            {metadata.key_concepts && metadata.key_concepts.length > 0 && (
              <div className="key-concepts">
                <h3>Key Concepts</h3>
                <div className="concepts-list">
                  {metadata.key_concepts.map((concept, idx) => (
                    <span key={idx} className="concept-tag">
                      {concept}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <ChatPanel
            question={question}
            setQuestion={setQuestion}
            answer={answer}
            loading={loading}
            error={error}
            onSubmit={handleAskQuestion}
            onClear={clearAnswer}
          />
        </div>
      </div>
    </div>
  );
}

export default VideoPlayer;