import React from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText, Divider } from '@mui/material';

interface LearningPathDisplayProps {
  learningPath: string;
}

const LearningPathDisplay: React.FC<LearningPathDisplayProps> = ({ learningPath }) => {
  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4, p: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          生成的学习路径
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Typography component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
          {learningPath}
        </Typography>
      </Paper>
    </Box>
  );
};

export default LearningPathDisplay;
