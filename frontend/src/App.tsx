import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { createTheme, Container, Alert } from '@mui/material'
import LearningPathForm from './components/LearningPathForm'
import LearningPathDisplay from './components/LearningPathDisplay'
import TaskList, { Task } from './components/TaskList'
import { generateLearningPath, LearningPathRequest } from './services/api'
import { v4 as uuidv4 } from 'uuid'

const theme = createTheme()

const App: React.FC = () => {
  const [learningPath, setLearningPath] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [tasks, setTasks] = useState<Task[]>([])

  const handleSubmit = async (data: LearningPathRequest) => {
    try {
      setError('')
      const result = await generateLearningPath(data)
      setLearningPath(result)
      
      // Parse the learning path into tasks
      const lines = result.split('\n')
      const newTasks: Task[] = []
      
      let currentTask: Partial<Task> = {}
      
      for (const line of lines) {
        if (line.trim().startsWith('- ')) {
          // Save previous task if exists
          if (currentTask.title) {
            newTasks.push({
              id: uuidv4(),
              title: currentTask.title!,
              description: currentTask.description || '',
              type: currentTask.type || 'THEORY',
              status: 'TODO',
              dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            } as Task)
          }
          
          // Start new task
          const content = line.trim().substring(2)
          if (content.toLowerCase().includes('练习') || content.toLowerCase().includes('作业')) {
            currentTask = { type: 'EXERCISE' }
          } else if (content.toLowerCase().includes('实践') || content.toLowerCase().includes('应用')) {
            currentTask = { type: 'PRACTICE' }
          } else {
            currentTask = { type: 'THEORY' }
          }
          currentTask.title = content
          currentTask.description = ''
        } else if (line.trim() && currentTask.title) {
          currentTask.description = (currentTask.description || '') + line.trim() + '\n'
        }
      }
      
      // Add last task if exists
      if (currentTask.title) {
        newTasks.push({
          id: uuidv4(),
          title: currentTask.title,
          description: currentTask.description || '',
          type: currentTask.type || 'THEORY',
          status: 'TODO',
          dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        } as Task)
      }
      
      setTasks(newTasks)
    } catch (err) {
      setError('生成学习路径时出错，请稍后重试')
    }
  }

  const handleToggleTask = (taskId: string) => {
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === taskId
          ? { ...task, status: task.status === 'COMPLETED' ? 'TODO' : 'COMPLETED' }
          : task
      )
    )
  }

  const handleDeleteTask = (taskId: string) => {
    setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId))
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Container>
          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
          <Routes>
            <Route path="/" element={
              <>
                <LearningPathForm onSubmit={handleSubmit} />
                {learningPath && <LearningPathDisplay learningPath={learningPath} />}
                {tasks.length > 0 && (
                  <TaskList
                    tasks={tasks}
                    onToggleTask={handleToggleTask}
                    onDeleteTask={handleDeleteTask}
                  />
                )}
              </>
            } />
          </Routes>
        </Container>
      </Router>
    </ThemeProvider>
  )
}

export default App
