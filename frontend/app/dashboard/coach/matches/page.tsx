import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { JobMatchList } from "@/components/matches/job-match-list";
import { coachAPI } from "@/lib/api-client";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function CoachMatchesPage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();
  let matches: any[] = [];
  let coachId: number | null = null;

  // Fetch the coach profile to get the coach ID
  try {
    if (token) {
      const coachList = await coachAPI.list({ page: 1, page_size: 1 }, token);
      if (coachList.coaches && coachList.coaches.length > 0) {
        const fetchedCoachId = coachList.coaches[0].id;
        coachId = fetchedCoachId;
        // Fetch matches for this coach
        const matchesData = await coachAPI.getMatches(fetchedCoachId, 20, token);

        // Transform backend response to match frontend interface
        matches = (matchesData.matches || []).map((match: any) => ({
          job_id: match.job.id,
          title: match.job.title,
          description: match.job.description,
          city: match.job.city,
          state: match.job.state,
          role_type: match.job.role_type,
          compensation_type: match.job.compensation_type,
          compensation_min: match.job.compensation_min,
          compensation_max: match.job.compensation_max,
          brand_logo_url: match.job.brand_logo_url,
          fitscore: match.fitscore,
          fitscore_breakdown: {
            certification_score: match.score_breakdown?.cert_score || 0,
            experience_score: match.score_breakdown?.experience_score || 0,
            availability_score: match.score_breakdown?.availability_score || 0,
            location_score: match.score_breakdown?.location_score || 0,
            culture_score: match.score_breakdown?.culture_score || 0,
            engagement_score: match.score_breakdown?.engagement_score || 0,
          },
        }));
      }
    }
  } catch (error) {
    // Profile doesn't exist yet or API error - show empty state
    console.log("No coach profile found or API error:", error);
  }

  // Show create profile prompt if no coach profile exists
  if (!coachId) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card className="border-0 shadow-sm">
          <CardContent className="pt-6">
            <div className="text-center py-16">
              <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-5">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Create Your Profile First</h3>
              <p className="text-muted-foreground mb-6 max-w-sm mx-auto">
                You need to create a coach profile before you can see job matches
              </p>
              <Link href="/dashboard/coach/edit">
                <Button size="lg">Create Profile</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-1">My Job Matches</h1>
        <p className="text-muted-foreground">
          Jobs ranked by FitScore based on your profile
        </p>
      </div>

      <JobMatchList matches={matches} />

      {matches.length > 0 && (
        <div className="grid md:grid-cols-3 gap-4 mt-8">
          <div className="bg-white rounded-xl p-5 shadow-sm border border-border/50">
            <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">FitScore Range</div>
            <div className="text-2xl font-bold">0.0 - 1.0</div>
            <p className="text-xs text-muted-foreground mt-1">Higher scores mean better matches</p>
          </div>

          <div className="bg-white rounded-xl p-5 shadow-sm border border-border/50">
            <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Match Factors</div>
            <div className="flex flex-wrap gap-1.5 mt-1">
              {["Certs", "Experience", "Availability", "Location", "Culture", "Engagement"].map(f => (
                <span key={f} className="px-2 py-0.5 bg-primary/10 text-primary rounded-md text-xs font-medium">{f}</span>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl p-5 shadow-sm border border-border/50">
            <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Threshold</div>
            <div className="text-2xl font-bold text-primary">&ge; 60%</div>
            <p className="text-xs text-muted-foreground mt-1">Only qualified matches shown</p>
          </div>
        </div>
      )}
    </div>
  );
}
