import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default async function DashboardPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          Welcome back, {user.firstName || "there"}!
        </h1>
        <p className="text-muted-foreground">
          What would you like to do today?
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Coach Profile</CardTitle>
            <CardDescription>
              Manage your professional profile and view job matches
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Link href="/dashboard/coach">
              <Button className="w-full">View Profile</Button>
            </Link>
            <Link href="/dashboard/coach/matches">
              <Button variant="outline" className="w-full">View My Matches</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Hiring Manager</CardTitle>
            <CardDescription>
              Post jobs and review coach candidates
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Link href="/dashboard/manager">
              <Button className="w-full">View Jobs</Button>
            </Link>
            <Link href="/dashboard/manager/new">
              <Button variant="outline" className="w-full">Post New Job</Button>
            </Link>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Quick Stats</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-3xl font-bold">0</div>
              <div className="text-sm text-muted-foreground">Profile Views</div>
            </div>
            <div>
              <div className="text-3xl font-bold">0</div>
              <div className="text-sm text-muted-foreground">Job Matches</div>
            </div>
            <div>
              <div className="text-3xl font-bold">0%</div>
              <div className="text-sm text-muted-foreground">Profile Complete</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
