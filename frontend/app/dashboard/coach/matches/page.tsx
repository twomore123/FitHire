import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { JobMatchList } from "@/components/matches/job-match-list";
import { coachAPI } from "@/lib/api-client";

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
        matches = matchesData.matches || [];
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
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2">Create Your Profile First</h3>
              <p className="text-muted-foreground mb-4">
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
        <h1 className="text-4xl font-bold mb-2">My Job Matches</h1>
        <p className="text-muted-foreground">
          Jobs ranked by FitScore based on your profile
        </p>
      </div>

      <JobMatchList matches={matches} />

      {matches.length > 0 && (
        <div className="grid md:grid-cols-3 gap-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium text-muted-foreground">
                FitScore Range
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">0.0 - 1.0</div>
              <p className="text-xs text-muted-foreground mt-1">
                Higher scores mean better matches
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Match Factors
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="text-sm space-y-1">
                <li>✓ Certifications</li>
                <li>✓ Experience</li>
                <li>✓ Availability</li>
                <li>✓ Location</li>
                <li>✓ Cultural Fit</li>
                <li>✓ Engagement</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Threshold Filter
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">≥ 0.60</div>
              <p className="text-xs text-muted-foreground mt-1">
                Only jobs you're qualified for
              </p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
