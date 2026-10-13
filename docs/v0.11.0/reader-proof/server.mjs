import { preview } from 'vite';

const server = await preview({
  preview: { host: '127.0.0.1', port: 5193, strictPort: true },
});
console.log('Built website preview at http://127.0.0.1:5193');
for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => server.httpServer.close(() => process.exit(0)));
}
