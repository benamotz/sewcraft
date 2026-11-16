import { Suspense } from "react";
import { getCards, getCategories, getPublishedProjects } from "@/lib/content";
import Explore from "@/components/Explore";

export const metadata = { title: "Explore projects" };

export default function ExplorePage() {
  const projects = getPublishedProjects().map((p) => ({ id: p.id, title: p.title, materials: p.materials, pieces: p.pieces, constants: p.constants, params: p.params }));
  return (
    <Suspense>
      <Explore cards={getCards()} categories={getCategories()} fabricProjects={projects} />
    </Suspense>
  );
}
