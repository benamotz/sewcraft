import { Suspense } from "react";
import { getGlossary, getTechniques, getToolCatalog } from "@/lib/content";
import LocalGuideView from "@/components/community/LocalGuideView";

export const metadata = { title: "Community guide" };

export default function Page() {
  const techniques = getTechniques().map(({ id, name, summary }) => ({ id, name, summary }));
  return (
    <Suspense>
      <LocalGuideView mode="sew" catalog={getToolCatalog()} techniques={techniques} glossary={getGlossary()} />
    </Suspense>
  );
}
