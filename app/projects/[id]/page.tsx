import { notFound } from "next/navigation";
import { getCards, getProject, getPublishedProjects, getTechniques } from "@/lib/content";
import ProjectDetail from "@/components/project/ProjectDetail";

export function generateStaticParams() {
  return getPublishedProjects().map((p) => ({ id: p.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const p = getProject(id);
  return { title: p?.title ?? "Project", description: p?.summary };
}

export default async function ProjectPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const project = getProject(id);
  if (!project) notFound();
  const techniques = getTechniques().filter((t) => project.techniques.includes(t.id) || project.steps.some((s) => s.techniques?.includes(t.id)));
  const related = getCards().filter((c) => project.related.includes(c.id));
  return <ProjectDetail project={project} techniques={techniques.map(({ id, name, summary }) => ({ id, name, summary }))} related={related} />;
}
