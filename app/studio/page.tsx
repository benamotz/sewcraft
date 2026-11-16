import { Suspense } from "react";
import { getCards, getCategories, getPublishedProjects } from "@/lib/content";
import Studio from "@/components/studio/Studio";

export const metadata = { title: "My Studio" };

export default function StudioPage() {
  return (
    <Suspense>
      <Studio cards={getCards()} projects={getPublishedProjects()} categories={getCategories()} />
    </Suspense>
  );
}
