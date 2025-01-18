import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const KIMI_API_URL = 'https://api.kimi.moonshot.cn';
const KIMI_API_KEY = process.env.KIMI_API_KEY;

if (!KIMI_API_KEY) {
  throw new Error('KIMI_API_KEY is not defined in environment variables');
}

const kimiClient = axios.create({
  baseURL: KIMI_API_URL,
  headers: {
    'Authorization': `Bearer ${KIMI_API_KEY}`,
    'Content-Type': 'application/json',
  },
});

export const generateLearningPath = async (params: {
  subject: string;
  difficultyLevel: string;
  learningGoals: string;
  availableTime: string;
  learningStyle: string;
}) => {
  try {
    const prompt = `Generate a structured learning path for ${params.subject} with:
- Difficulty: ${params.difficultyLevel}
- Goals: ${params.learningGoals}
- Available time: ${params.availableTime}
- Learning style: ${params.learningStyle}

Please provide a detailed plan with specific tasks, including theory study, practice exercises, and assessments.`;

    const response = await kimiClient.post('/v1/chat/completions', {
      messages: [{ role: 'user', content: prompt }],
      model: 'moonshot-v1-8k',
      temperature: 0.7,
    });

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Error generating learning path:', error);
    throw error;
  }
};
