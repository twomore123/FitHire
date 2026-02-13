import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getCurrentUserProfile } from "@/lib/user";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function DashboardPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  const userProfile = await getCurrentUserProfile();
  const role = userProfile?.role;

  // If user already has a role, redirect them straight to their section
  if (role === "coach") {
    redirect("/dashboard/coach");
  }
  if (role === "location_manager") {
    redirect("/dashboard/manager");
  }

  // No role yet — show role selection for new users
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          Welcome, {user.firstName || "there"}!
        </h1>
        <p className="text-muted-foreground">
          How would you like to use FitHire?
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>I&apos;m a Coach</CardTitle>
            <CardDescription>
              Create your professional profile and get matched with jobs
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Link href="/dashboard/coach">
              <Button className="w-full">Set Up Coach Profile</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>I&apos;m a Hiring Manager</CardTitle>
            <CardDescription>
              Post jobs and find qualified coach candidates
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Link href="/dashboard/manager">
              <Button className="w-full">Post a Job</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
