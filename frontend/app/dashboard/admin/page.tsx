import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function AdminDashboardPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  // TODO: Add admin role check
  // if (user.publicMetadata.role !== "admin") {
  //   redirect("/dashboard");
  // }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
        <p className="text-muted-foreground">
          Manage verification queue and system settings
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Link href="/dashboard/admin/verification">
          <Card className="hover:border-primary transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle>Verification Queue</CardTitle>
              <CardDescription>
                Review and approve pending coach profiles
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="text-2xl font-bold">Pending Review</div>
                <Button>View Queue</Button>
              </div>
            </CardContent>
          </Card>
        </Link>

        <Card className="opacity-50">
          <CardHeader>
            <CardTitle>Brand Management</CardTitle>
            <CardDescription>
              Manage brands, regions, and locations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">Phase 2 Feature</div>
              <Button disabled variant="outline">Coming Soon</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="opacity-50">
          <CardHeader>
            <CardTitle>User Management</CardTitle>
            <CardDescription>
              Manage user roles and permissions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">Phase 2 Feature</div>
              <Button disabled variant="outline">Coming Soon</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="opacity-50">
          <CardHeader>
            <CardTitle>Analytics</CardTitle>
            <CardDescription>
              View platform analytics and metrics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">Phase 2 Feature</div>
              <Button disabled variant="outline">Coming Soon</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
