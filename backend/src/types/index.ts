export interface LearningPath {
  id: string;
  subject: string;
  difficultyLevel: string;
  learningGoals: string;
  availableTime: string;
  learningStyle: string;
  tasks: Task[];
  createdAt: Date;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  type: 'THEORY' | 'PRACTICE' | 'EXERCISE';
  status: 'TODO' | 'IN_PROGRESS' | 'COMPLETED';
  dueDate: Date;
  learningPathId: string;
}

export interface Material {
  id: string;
  title: string;
  content: string;
  type: 'CONCEPT' | 'EXAMPLE' | 'EXERCISE';
  subject: string;
  tags: string[];
  difficulty: string;
}

export interface CreateLearningPathDto {
  subject: string;
  difficulty_level: string;
  learning_goals: string;
  available_time: string;
  learning_style: string;
}
