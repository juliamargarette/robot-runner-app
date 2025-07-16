import { readFile } from 'fs/promises';
import path from 'path';

export default async function handler(req, res) {
  const filePath = path.join(process.cwd(), 'data.json');
  const raw = await readFile(filePath, 'utf8');
  const data = JSON.parse(raw);

  // sort by duration
  const sorted = data.sort((a, b) => a.duration - b.duration);
  res.status(200).json(sorted);
}
