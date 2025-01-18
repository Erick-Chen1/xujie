import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export interface LearningPathRequest {
  subject: string;
  difficulty_level: string;
  learning_goals: string;
  available_time: string;
  learning_style: string;
}

export const generateLearningPath = async (data: LearningPathRequest) => {
  try {
    const response = await axios.post(`${API_URL}/api/v1/learning-path`, data);
    return response.data;
  } catch (error) {
    console.error('Error generating learning path:', error);
    throw error;
  }
};
