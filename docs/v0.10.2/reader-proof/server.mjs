import { createServer } from 'vite';
import { realpathSync } from 'node:fs';
const server=await createServer({server:{host:'127.0.0.1',port:5190,strictPort:true,fs:{allow:['src/lib/data',realpathSync('node_modules')]}}});
await server.listen();
console.log(`v0.10.2 proof server PID ${process.pid} at http://127.0.0.1:5190`);
for (const signal of ['SIGINT','SIGTERM']) process.on(signal, async()=>{await server.close();process.exit(0)});
