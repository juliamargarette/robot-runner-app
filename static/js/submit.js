import { writeFile, readFile } from 'fs/promises';
import path from 'path';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Only POST allowed' });
  }

  const { name, duration } = req.body;
  if (!name || !duration) {
    return res.status(400).json({ message: 'Missing name or duration' });
  }

  const filePath = path.join(process.cwd(), 'data.json');
  const raw = await readFile(filePath, 'utf8');
  const data = JSON.parse(raw);

  data.push({ name, duration: parseFloat(duration), timestamp: new Date().toISOString() });
  await writeFile(filePath, JSON.stringify(data, null, 2));

  res.status(200).json({ message: 'Submission saved!' });
}
