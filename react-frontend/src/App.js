// src/App.js

import React, { useState } from 'react';
import { CssBaseline, Container } from '@mui/material';
import AppBarComponent from './components/AppBar';
import XrayPrediction from './components/XrayPrediction';
import Chatbot from './components/Chatbot';

function App() {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [overlayImage, setOverlayImage] = useState(null);
  const [explanation, setExplanation] = useState(null);

  // Session ID can be generated or fetched based on your requirements
  const sessionId = 'unique-session-id';

  return (
    <>
      <CssBaseline />
      <AppBarComponent />
      <Container>
        <XrayPrediction
          setModalIsOpen={setModalIsOpen}
          setPreviewImage={setPreviewImage}
          setPrediction={setPrediction}
          setOverlayImage={setOverlayImage}
          setExplanation={setExplanation}
        />
      </Container>
      <Chatbot sessionId={sessionId} />
    </>
  );
}

export default App;
