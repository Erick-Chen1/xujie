import React from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText, ListItemIcon, Checkbox, IconButton, Chip } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

export interface Task {
  id: string;
  title: string;
  description: string;
  type: 'THEORY' | 'PRACTICE' | 'EXERCISE';
  status: 'TODO' | 'IN_PROGRESS' | 'COMPLETED';
  dueDate: string;
}

interface TaskListProps {
  tasks: Task[];
  onToggleTask: (taskId: string) => void;
  onDeleteTask: (taskId: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onToggleTask, onDeleteTask }) => {
  const getStatusColor = (status: Task['status']) => {
    switch (status) {
      case 'TODO':
        return 'error';
      case 'IN_PROGRESS':
        return 'warning';
      case 'COMPLETED':
        return 'success';
      default:
        return 'default';
    }
  };

  const getTypeColor = (type: Task['type']) => {
    switch (type) {
      case 'THEORY':
        return 'primary';
      case 'PRACTICE':
        return 'secondary';
      case 'EXERCISE':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          学习任务清单
        </Typography>
        <List>
          {tasks.map((task) => (
            <ListItem
              key={task.id}
              secondaryAction={
                <IconButton edge="end" aria-label="delete" onClick={() => onDeleteTask(task.id)}>
                  <DeleteIcon />
                </IconButton>
              }
              sx={{ flexDirection: 'column', alignItems: 'flex-start', borderBottom: 1, borderColor: 'divider' }}
            >
              <Box sx={{ display: 'flex', width: '100%', alignItems: 'center', mb: 1 }}>
                <ListItemIcon>
                  <Checkbox
                    edge="start"
                    checked={task.status === 'COMPLETED'}
                    onChange={() => onToggleTask(task.id)}
                  />
                </ListItemIcon>
                <ListItemText
                  primary={task.title}
                  sx={{ mr: 2 }}
                />
                <Box>
                  <Chip
                    label={task.type}
                    color={getTypeColor(task.type)}
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  <Chip
                    label={task.status}
                    color={getStatusColor(task.status)}
                    size="small"
                  />
                </Box>
              </Box>
              <Box sx={{ pl: 7, width: '100%' }}>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {task.description}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  截止日期: {task.dueDate}
                </Typography>
              </Box>
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default TaskList;
