// src/components/AppBar.js

import React from 'react';
import { AppBar, Toolbar, IconButton, Typography } from '@mui/material';


function AppBarComponent() {
  return (
    <AppBar position="static" color="primary">
      <Toolbar variant="dense">
        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
          <img src="logo-classification.PNG" alt="Logo" style={{ height: '40px', borderRadius: '50%' }} />
        </IconButton>
        <Typography variant="h6" color="inherit" component="div">
          AI-Powered Chest Cancer Diagnosis Platform
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default AppBarComponent;
