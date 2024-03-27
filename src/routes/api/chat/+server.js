import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';
import { OPENAI_API_KEY } from '$env/static/private';
import type { RequestHandler } from './$types';

const openai = new OpenAI({
  apiKey: OPENAI_API_KEY,
});

export const POST = (async ({ request }) => {
  const { messages } = await request.json();

  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    stream: true,
    messages: messages,
  });

  const stream = OpenAIStream(response);

  return new StreamingTextResponse(stream);
}) satisfies RequestHandler;