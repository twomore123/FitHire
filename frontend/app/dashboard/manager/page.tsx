import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import Image from "next/image";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { jobAPI } from "@/lib/api-client";
import { DeleteJobButton } from "@/components/delete-job-button";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function ManagerJobsPage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();
  let jobs: any[] = [];
  let totalJobs = 0;

  // Try to fetch jobs
  try {
    if (token) {
      const jobsData = await jobAPI.list({ page: 1, page_size: 20 }, token);
      jobs = jobsData.jobs || [];
      totalJobs = jobsData.total || 0;

      // Filter out any jobs without valid IDs
      jobs = jobs.filter(job => job.id && typeof job.id === 'number');
    }
  } catch (error) {
    console.error("Error fetching jobs:", error);
  }

  const activeJobs = jobs.filter(job => job.is_active).length;

  // Fetch candidates for all jobs to compute average FitScore
  let avgFitScore: number | null = null;
  if (token && jobs.length > 0) {
    try {
      const allCandidateResults = await Promise.all(
        jobs.map((job) => jobAPI.getCandidates(job.id, 20, token).catch(() => ({ candidates: [] })))
      );
      const allScores: number[] = [];
      for (const result of allCandidateResults) {
        const candidates = result.candidates || result || [];
        if (Array.isArray(candidates)) {
          for (const candidate of candidates) {
            if (candidate.fitscore != null && typeof candidate.fitscore === "number") {
              allScores.push(candidate.fitscore);
            }
          }
        }
      }
      if (allScores.length > 0) {
        const sum = allScores.reduce((a: number, b: number) => a + b, 0);
        avgFitScore = Math.round((sum / allScores.length) * 100);
      }
    } catch (error) {
      console.error("Error computing avg FitScore:", error);
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Stats Strip */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-xl p-5 shadow-sm border border-border/50">
          <div className="text-sm font-medium text-muted-foreground mb-1">Active Jobs</div>
          <div className="text-3xl font-bold text-primary">{activeJobs}</div>
          <div className="text-xs text-muted-foreground mt-1">Currently open</div>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border border-border/50">
          <div className="text-sm font-medium text-muted-foreground mb-1">Total Jobs</div>
          <div className="text-3xl font-bold">{totalJobs}</div>
          <div className="text-xs text-muted-foreground mt-1">All postings</div>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border border-border/50">
          <div className="text-sm font-medium text-muted-foreground mb-1">Avg FitScore</div>
          <div className="text-3xl font-bold text-primary">
            {avgFitScore !== null ? avgFitScore : "--"}
          </div>
          <div className="text-xs text-muted-foreground mt-1">
            {avgFitScore !== null ? "Across all candidates" : "No candidates yet"}
          </div>
        </div>
      </div>

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Job Listings</h1>
          <p className="text-muted-foreground mt-1">
            Manage your job postings and review candidates
          </p>
        </div>
        <Link href="/dashboard/manager/new">
          <Button size="lg" className="shadow-sm">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mr-1">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Post New Job
          </Button>
        </Link>
      </div>

      {jobs.length === 0 ? (
        <Card className="border-0 shadow-sm">
          <CardContent className="pt-6">
            <div className="text-center py-16">
              <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-5">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">No Jobs Posted Yet</h3>
              <p className="text-muted-foreground mb-6 max-w-sm mx-auto">
                Create your first job posting to start finding candidates
              </p>
              <Link href="/dashboard/manager/new">
                <Button size="lg">Post Your First Job</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4 mb-6">
          {jobs.map((job) => (
            <Card key={job.id} className="relative border-0 shadow-sm hover:shadow-md transition-shadow group">
              <div className="absolute top-4 right-4 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
                <DeleteJobButton jobId={job.id} jobTitle={job.title} />
              </div>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="flex gap-4 items-start flex-1">
                    {job.brand_logo_url ? (
                      <div className="relative w-14 h-14 rounded-xl overflow-hidden border border-border/50 flex-shrink-0 bg-white shadow-sm">
                        <Image
                          src={job.brand_logo_url}
                          alt={`${job.title} logo`}
                          fill
                          className="object-contain p-1.5"
                        />
                      </div>
                    ) : (
                      <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/10 flex items-center justify-center flex-shrink-0">
                        <span className="text-xl font-bold text-primary">
                          {job.title?.charAt(0) || "J"}
                        </span>
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <CardTitle className="truncate text-lg">{job.title}</CardTitle>
                      <CardDescription className="mt-0.5">
                        {job.city}, {job.state} &middot; {job.role_type}
                      </CardDescription>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0 mr-8">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      job.is_active
                        ? 'bg-primary/10 text-primary'
                        : 'bg-muted text-muted-foreground'
                    }`}>
                      {job.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                  {job.description}
                </p>
                <div className="flex gap-2">
                  <Link href={`/dashboard/manager/${job.id}`}>
                    <Button size="sm">View Candidates</Button>
                  </Link>
                  <Link href={`/dashboard/manager/${job.id}/edit`}>
                    <Button size="sm" variant="outline">Edit</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {jobs.length === 0 && (
        <Card className="mt-6 border-0 shadow-sm">
          <CardHeader>
            <CardTitle>How Job Matching Works</CardTitle>
            <CardDescription>
              Understanding the FitScore algorithm
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="p-4 rounded-xl bg-primary/5">
                <h4 className="font-semibold mb-2">Configurable Matching</h4>
                <p className="text-sm text-muted-foreground">
                  Set your own FitScore threshold (0.40-0.80) and choose from weighting presets:
                  balanced, experience-heavy, culture-heavy, or availability-focused.
                </p>
              </div>
              <div className="p-4 rounded-xl bg-primary/5">
                <h4 className="font-semibold mb-2">Top 20 Candidates</h4>
                <p className="text-sm text-muted-foreground">
                  See the best-matched coaches instantly, ranked by FitScore with detailed
                  breakdowns of each scoring component.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
