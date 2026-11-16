import { Suspense } from "react";
import { getCategories, getTechniques, getToolCatalog } from "@/lib/content";
import GuideBuilder from "@/components/community/GuideBuilder";

export const metadata = { title: "Write a guide" };

export default function NewGuidePage() {
  return (
    <Suspense>
      <GuideBuilder catalog={getToolCatalog()} techniques={getTechniques().map(({ id, name }) => ({ id, name }))} categories={getCategories()} />
    </Suspense>
  );
}
