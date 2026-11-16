import { notFound } from "next/navigation";
import { getProject, getPublishedProjects } from "@/lib/content";
import PrintPattern from "@/components/PrintPattern";

export function generateStaticParams() {
  return getPublishedProjects().map((p) => ({ id: p.id }));
}

export const metadata = { title: "Print pattern" };

export default async function PrintPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const project = getProject(id);
  if (!project) notFound();
  return <PrintPattern project={project} />;
}
