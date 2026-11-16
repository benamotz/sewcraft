import { getCards, getToolCatalog } from "@/lib/content";
import CommunityHub from "@/components/community/CommunityHub";

export const metadata = { title: "Community guides" };

export default function CommunityPage() {
  return <CommunityHub cards={getCards().filter((c) => c.source === "community")} catalog={getToolCatalog()} />;
}
