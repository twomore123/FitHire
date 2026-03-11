import { DashboardNav } from "@/components/dashboard-nav";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-brand-green-light/50 to-white">
      <DashboardNav />

      <main className="container mx-auto px-6 py-8">
        {children}
      </main>
    </div>
  );
}
