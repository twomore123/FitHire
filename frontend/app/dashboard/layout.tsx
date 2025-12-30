import Link from "next/link";
import { UserButton } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-zinc-50">
      <nav className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/dashboard">
              <h1 className="text-2xl font-bold">FitHire</h1>
            </Link>

            <div className="flex items-center gap-6">
              <Link href="/dashboard/coach">
                <Button variant="ghost">My Profile</Button>
              </Link>
              <Link href="/dashboard/coach/matches">
                <Button variant="ghost">My Matches</Button>
              </Link>
              <Link href="/dashboard/manager">
                <Button variant="ghost">Jobs</Button>
              </Link>
              <UserButton />
            </div>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
}
