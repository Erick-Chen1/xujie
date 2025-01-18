import Koa from 'koa';
import bodyParser from 'koa-bodyparser';
import dotenv from 'dotenv';
import cors from '@koa/cors';
import learningPathRouter from './routes/learning-path';
import materialsRouter from './routes/materials';

dotenv.config();

const app = new Koa();

// Middleware
app.use(cors());
app.use(bodyParser());

// Routes
app.use(learningPathRouter.routes());
app.use(materialsRouter.routes());
app.use(learningPathRouter.allowedMethods());
app.use(materialsRouter.allowedMethods());

const port = process.env.PORT || 8000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
