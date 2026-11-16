import { getPublishedProjects } from "@/lib/content";
import Calculator from "@/components/Calculator";

export const metadata = { title: "Fabric calculator" };

export default function CalculatorPage() {
  return <Calculator projects={getPublishedProjects()} />;
}
