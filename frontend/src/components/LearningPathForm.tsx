import React, { useState } from 'react';
import { Button, TextField, FormControl, InputLabel, Select, MenuItem, Box, Typography, SelectChangeEvent } from '@mui/material';

interface LearningPathFormProps {
  onSubmit: (data: FormData) => void;
}

interface FormData {
  subject: string;
  difficulty_level: string;
  learning_goals: string;
  available_time: string;
  learning_style: string;
}

const LearningPathForm: React.FC<LearningPathFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<FormData>({
    subject: '高中数学',
    difficulty_level: '中等',
    learning_goals: '',
    available_time: '',
    learning_style: '实践与理论结合',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleTextFieldChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSelectChange = (e: SelectChangeEvent) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 600, mx: 'auto', mt: 4, p: 3 }}>
      <Typography variant="h5" gutterBottom>
        生成学习路径
      </Typography>
      
      <TextField
        fullWidth
        margin="normal"
        name="subject"
        label="学科"
        value={formData.subject}
        onChange={handleTextFieldChange}
      />

      <FormControl fullWidth margin="normal">
        <InputLabel>难度级别</InputLabel>
        <Select
          name="difficulty_level"
          value={formData.difficulty_level}
          label="难度级别"
          onChange={handleSelectChange}
        >
          <MenuItem value="初级">初级</MenuItem>
          <MenuItem value="中等">中等</MenuItem>
          <MenuItem value="高级">高级</MenuItem>
        </Select>
      </FormControl>

      <TextField
        fullWidth
        margin="normal"
        name="learning_goals"
        label="学习目标"
        multiline
        rows={3}
        value={formData.learning_goals}
        onChange={handleTextFieldChange}
      />

      <TextField
        fullWidth
        margin="normal"
        name="available_time"
        label="可用时间"
        placeholder="例如：每天2小时"
        value={formData.available_time}
        onChange={handleTextFieldChange}
      />

      <FormControl fullWidth margin="normal">
        <InputLabel>学习方式</InputLabel>
        <Select
          name="learning_style"
          value={formData.learning_style}
          label="学习方式"
          onChange={handleSelectChange}
        >
          <MenuItem value="实践与理论结合">实践与理论结合</MenuItem>
          <MenuItem value="以理论为主">以理论为主</MenuItem>
          <MenuItem value="以实践为主">以实践为主</MenuItem>
        </Select>
      </FormControl>

      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        sx={{ mt: 3 }}
      >
        生成学习路径
      </Button>
    </Box>
  );
};

export default LearningPathForm;
