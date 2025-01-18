import Router from '@koa/router';
import { materialsService } from '../services/materials';

const router = new Router({
  prefix: '/api/v1/materials'
});

router.get('/:subject', async (ctx) => {
  try {
    const { subject } = ctx.params;
    const { difficulty, type, tags } = ctx.query;

    let materials;
    if (difficulty) {
      materials = materialsService.getMaterialsByDifficulty(subject, difficulty as string);
    } else if (type) {
      materials = materialsService.getMaterialsByType(subject, type as any);
    } else if (tags) {
      const tagList = (tags as string).split(',');
      materials = materialsService.searchMaterialsByTags(subject, tagList);
    } else {
      materials = materialsService.getMaterialsBySubject(subject);
    }

    ctx.body = materials;
  } catch (error) {
    ctx.status = 500;
    ctx.body = { error: 'Failed to fetch materials' };
  }
});

export default router;
