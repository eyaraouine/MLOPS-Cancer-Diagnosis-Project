// src/components/Chatbot.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, List, ListItem, ListItemText, IconButton, TextField, Fab,Typography } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import CloseIcon from '@mui/icons-material/Close';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function Chatbot({ sessionId }) {
  const [chatbotOpen, setChatbotOpen] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [mediaFile, setMediaFile] = useState(null);

  useEffect(() => {
    if (chatbotOpen && chatMessages.length === 0) {
      const initialMessage = {
        type: 'bot',
        content: "Hello, I'm MedBot, your AI-powered assistant for chest cancer diagnostics. How can I assist you today?",
      };
      setChatMessages([initialMessage]);
    }
  }, [chatbotOpen]);

  const sendMessageToChatbot = () => {
    if (chatInput.trim() || mediaFile) {
      const userMessage = { type: 'user', content: chatInput, media: mediaFile };
      setChatMessages((prevMessages) => [...prevMessages, userMessage]);

      axios.post('http://127.0.0.1:5000/chat', { message: chatInput, media: mediaFile, sessionId })
        .then(response => {
          if (response.data.error) {
            const errorMessage = { type: 'bot', content: response.data.error.toString() };
            setChatMessages((prevMessages) => [...prevMessages, errorMessage]);
          } else {
            const botMessage = { type: 'bot', content: response.data.reply };
            setChatMessages((prevMessages) => [...prevMessages, botMessage]);
          }
        })
        .catch(error => {
          const errorMessage = { type: 'bot', content: 'Error communicating with the chatbot.' };
          setChatMessages((prevMessages) => [...prevMessages, errorMessage]);
        });

      setChatInput('');  // Clear input
      setMediaFile(null); // Clear media
    }
  };

  const handleMediaUpload = (event) => {
    const file = event.target.files[0];
    setMediaFile(file);
  };

  return (
    <>
      <Fab
        color="primary"
        aria-label="chat"
        style={{ position: 'fixed', bottom: '20px', right: '20px' }}
        onClick={() => setChatbotOpen(!chatbotOpen)}
      >
        <ChatIcon />
      </Fab>

      {chatbotOpen && (
        <Box
          sx={{
            position: 'fixed',
            bottom: '80px',
            right: '20px',
            width: '450px',
            maxWidth: '90vw',
            height: '560px',
            backgroundColor: 'white',
            boxShadow: 3,
            display: 'flex',
            flexDirection: 'column',
            borderRadius: '10px',
            overflow: 'hidden',
          }}
        >
          <Box sx={{ p: 2, backgroundColor: '#3f51b5', color: 'white', position: 'relative' }}>
            <Typography variant="h6">MedBot</Typography>
            <IconButton
              color="inherit"
              onClick={() => setChatbotOpen(false)}
              sx={{ position: 'absolute', top: 0, right: 0 }}
            >
              <CloseIcon />
            </IconButton>
          </Box>
          <Box sx={{ flexGrow: 1, p: 2, overflowY: 'auto' }}>
            <List>
              {chatMessages.map((msg, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={
                      <ReactMarkdown
                        children={msg.content}
                        remarkPlugins={[remarkGfm]}
                      />
                    }
                    secondary={msg.media && (
                      <Box>
                        {msg.media.type.startsWith('image/') ? (
                          <img src={URL.createObjectURL(msg.media)} alt="Media" style={{ maxWidth: '100%', borderRadius: '8px' }} />
                        ) : (
                          <video controls style={{ maxWidth: '100%', borderRadius: '8px' }}>
                            <source src={URL.createObjectURL(msg.media)} />
                            Your browser does not support the video tag.
                          </video>
                        )}
                      </Box>
                    )}
                    sx={{ textAlign: msg.type === 'bot' ? 'left' : 'right' }}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
          <Box sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
            <IconButton color="primary" component="label">
              <AttachFileIcon />
              <input
                type="file"
                hidden
                onChange={handleMediaUpload}
              />
            </IconButton>
            <TextField
              fullWidth
              variant="outlined"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessageToChatbot()}
              placeholder="Type your message..."
            />
            <IconButton color="primary" onClick={sendMessageToChatbot}>
              <SendIcon />
            </IconButton>
          </Box>
        </Box>
      )}
    </>
  );
}

export default Chatbot;
