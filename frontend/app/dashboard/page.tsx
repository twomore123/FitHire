import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { DashboardHome } from "@/components/dashboard-home";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function DashboardPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  return <DashboardHome firstName={user.firstName} />;
}
