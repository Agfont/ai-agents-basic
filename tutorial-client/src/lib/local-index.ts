import { readdirSync } from "node:fs";
import { join } from "node:path";

export type LocalTask = {
  id: number;
  filename: string;
};

export type LocalLab = {
  slug: string;
  tasks: LocalTask[];
};

const LAB_PATTERN = /^\d+-/;
const TASK_PATTERN = /^task_(\d+)_.*\.py$/;

function repoRootFromCurrentDir(): string {
  return join(process.cwd(), "..");
}

export function getLocalLabs(): LocalLab[] {
  const root = repoRootFromCurrentDir();
  const entries = readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && LAB_PATTERN.test(entry.name))
    .map((entry) => entry.name)
    .sort();

  return entries.map((slug) => {
    const labDir = join(root, slug);
    const tasks = readdirSync(labDir, { withFileTypes: true })
      .filter((entry) => entry.isFile() && TASK_PATTERN.test(entry.name))
      .map((entry) => {
        const match = TASK_PATTERN.exec(entry.name);
        return {
          id: Number(match?.[1] ?? 0),
          filename: entry.name
        };
      })
      .filter((task) => task.id > 0)
      .sort((a, b) => a.id - b.id);

    return { slug, tasks };
  });
}
