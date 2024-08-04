import React, { useState } from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import {
  Container,
  Typography,
  CircularProgress,
  Card,
  CardMedia,
  CardContent,
  Button,
  AppBar,
  Toolbar,
  IconButton,
  Grid,
  Paper,
  Box,
} from '@mui/material';

import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import CloseIcon from '@mui/icons-material/Close';

Modal.setAppElement('#root');

function App() {
  const [imageFile, setImageFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modalIsOpen, setModalIsOpen] = useState(false);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setImageFile(file);
    setError(null);

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      setPreviewImage(reader.result);
    };
  };

  const handlePredict = () => {
    if (imageFile) {
      setIsLoading(true);

      const reader = new FileReader();
      reader.readAsDataURL(imageFile);
      reader.onloadend = () => {
        const base64Image = reader.result.split(',')[1];
        const imageData = { image: base64Image };

        axios.post('http://127.0.0.1:5000/predict', imageData)
          .then(response => {
            setPrediction(response.data);
            setIsLoading(false);
            setModalIsOpen(true);
          })
          .catch(error => {
            setError(error.message || 'An error occurred.');
            setIsLoading(false);
          });
      };
    } else {
      setError('Please upload an image first.');
    }
  };

  return (
    <>
      <AppBar position="static" color="primary">
        <Toolbar variant="dense">
          <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
            <img src="logo-classification.PNG" alt="Logo" style={{ height: '40px',borderRadius: '50%' }} />
          </IconButton>
          <Typography variant="h6" color="inherit" component="div">
            Chest X-Ray Prediction
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="sm" sx={{ flexGrow: 1, mt: '2rem' }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ padding: '2rem' }}>
              <Typography variant="h5" gutterBottom>
                Select Image for Prediction
              </Typography>
              <Box display="flex" justifyContent="center" alignItems="center" gap="1rem">
                <Button
                  variant="contained"
                  component="label"
                  disabled={isLoading}
                  startIcon={<PhotoCameraIcon />}
                >
                  Upload Image
                  <input
                    type="file"
                    accept="image/*"
                    hidden
                    onChange={handleImageUpload}
                  />
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={handlePredict}
                  disabled={!imageFile || isLoading}
                >
                  {isLoading ? <CircularProgress size={24} /> : 'Predict'}
                </Button>
              </Box>
              {error && (
                <Typography variant="body2" color="error" sx={{ mt: 1 }}>
                  Error: {error}
                </Typography>
              )}
            </Paper>
          </Grid>
          {previewImage && (
            <Grid item xs={12}>
              <Card>
                <CardMedia
                  component="img"
                  height="300"
                  image={previewImage}
                  alt="Uploaded chest X-ray"
                />
                <CardContent>
                  <Typography variant="h6">Uploaded Image</Typography>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </Container>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={() => setModalIsOpen(false)}
        contentLabel="Prediction Result"
        style={{
          content: {
            top: '50%',
            left: '50%',
            right: 'auto',
            bottom: 'auto',
            transform: 'translate(-50%, -50%)',
            width: '80%',
            maxWidth: '500px',
            padding: '2rem',
          },
        }}
      >
        <Typography variant="h5" gutterBottom>
          Prediction Results
        </Typography>
        <Typography variant="body1">{prediction}</Typography>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => setModalIsOpen(false)}
          style={{ marginTop: '1rem' }}
        >
          Close
        </Button>
      </Modal>
    </>
  );
}

export default App;
