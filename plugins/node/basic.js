#!/usr/bin/env node
const readline = require('readline');

const META = {
  name: 'node-basic',
  version: '0.1.0',
  language: 'node',
  capabilities: ['string.reverse']
};

function invoke(tool, args) {
  if (tool === 'string.reverse') {
    const text = (args && args.text) ? String(args.text) : '';
    return text.split('').reverse().join('');
  }
  throw new Error('Unknown tool: ' + tool);
}

function serve() {
  const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
  rl.on('line', (line) => {
    if (!line) return;
    let req; try { req = JSON.parse(line); } catch { return; }
    const id = req.id;
    const method = req.method;
    const params = req.params || {};
    try {
      if (method === 'get_meta') {
        process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, result: META }) + '\n');
      } else if (method === 'invoke') {
        const tool = params.tool;
        const args = params.args || {};
        const result = invoke(tool, args);
        process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, result }) + '\n');
      } else if (method === 'shutdown') {
        process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, result: true }) + '\n');
        process.exit(0);
      } else {
        throw new Error('Unknown method');
      }
    } catch (e) {
      process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, error: { message: e.message } }) + '\n');
    }
  });
}

if (process.argv.includes('--serve')) {
  serve();
}
