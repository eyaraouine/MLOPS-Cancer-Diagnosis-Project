// src/components/XrayPrediction.js

import React, { useState } from 'react';
import { Container, Typography, Button, Box, CircularProgress, Card, CardMedia, CardContent, Paper, Grid } from '@mui/material';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import axios from 'axios';

function XrayPrediction({ setModalIsOpen, setPreviewImage, setPrediction, setOverlayImage, setExplanation }) {
  const [imageFile, setImageFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [previewImage, setPreviewImageLocal] = useState(null);  // Added this line to define previewImage

  // Handle image upload
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setImageFile(file);
    setError(null);

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      setPreviewImageLocal(reader.result); // Use the local state for previewImage
    };
  };

  // Handle prediction
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
            setPrediction(response.data.prediction);
            setOverlayImage(response.data.overlay_image);
            setExplanation(response.data.explanation);
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
    <Container maxWidth="sm" sx={{ flexGrow: 1, mt: '2rem' }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: '2rem' }}>
            <Typography variant="h5" gutterBottom>
              Select Chest X-ray for Diagnosis
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
                image={previewImage}  // Use the local state for previewImage
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
  );
}

export default XrayPrediction;
