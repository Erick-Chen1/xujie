import Router from '@koa/router';
import { generateLearningPath } from '../services/kimi';
import type { CreateLearningPathDto } from '../types';

const router = new Router({
  prefix: '/api/v1/learning-path'
});

interface KoaContext {
  request: {
    body: CreateLearningPathDto;
  };
  body: any;
  status: number;
}

router.post('/', async (ctx: KoaContext) => {
  try {
    const { body } = ctx.request;
    const learningPath = await generateLearningPath({
      subject: body.subject,
      difficultyLevel: body.difficulty_level,
      learningGoals: body.learning_goals,
      availableTime: body.available_time,
      learningStyle: body.learning_style,
    });
    
    ctx.body = learningPath;
  } catch (error) {
    ctx.status = 500;
    ctx.body = { error: 'Failed to generate learning path' };
  }
});

export default router;
