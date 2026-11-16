import { notFound } from "next/navigation";
import { Suspense } from "react";
import { getGlossary, getProject, getPublishedProjects, getTechniques } from "@/lib/content";
import SewMode from "@/components/sew/SewMode";

export function generateStaticParams() {
  return getPublishedProjects().map((p) => ({ id: p.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return { title: `Sewing: ${getProject(id)?.title ?? ""}` };
}

export default async function SewPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const project = getProject(id);
  if (!project) notFound();
  const techniques = getTechniques().map(({ id, name, summary }) => ({ id, name, summary }));
  return (
    <Suspense>
      <SewMode project={project} techniques={techniques} glossary={getGlossary()} />
    </Suspense>
  );
}
