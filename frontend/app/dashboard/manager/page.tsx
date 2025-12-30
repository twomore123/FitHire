import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default async function ManagerJobsPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  // In a real implementation, we would fetch jobs from the API here
  // const jobs = await jobAPI.list({ page: 1, page_size: 20 }, token);

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold mb-2">Job Listings</h1>
          <p className="text-muted-foreground">
            Manage your job postings and review candidates
          </p>
        </div>
        <Link href="/dashboard/manager/new">
          <Button size="lg">Post New Job</Button>
        </Link>
      </div>

      <Card>
        <CardContent className="pt-6">
          <div className="text-center py-12">
            <div className="text-6xl mb-4">💼</div>
            <h3 className="text-xl font-semibold mb-2">No Jobs Posted Yet</h3>
            <p className="text-muted-foreground mb-4">
              Create your first job posting to start finding candidates
            </p>
            <Link href="/dashboard/manager/new">
              <Button>Post Your First Job</Button>
            </Link>
          </div>
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-3 gap-4 mt-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Active Jobs
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground mt-1">
              Currently open positions
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Candidates
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground mt-1">
              Matched coaches across all jobs
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Avg FitScore
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">--</div>
            <p className="text-xs text-muted-foreground mt-1">
              Average match quality
            </p>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>How Job Matching Works</CardTitle>
          <CardDescription>
            Understanding the FitScore algorithm
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold mb-2">Configurable Matching</h4>
              <p className="text-sm text-muted-foreground">
                Set your own FitScore threshold (0.40-0.80) and choose from weighting presets:
                balanced, experience-heavy, culture-heavy, or availability-focused.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Top 20 Candidates</h4>
              <p className="text-sm text-muted-foreground">
                See the best-matched coaches instantly, ranked by FitScore with detailed
                breakdowns of each scoring component.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
