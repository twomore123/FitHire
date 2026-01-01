import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { JobMatchList } from "@/components/matches/job-match-list";
import { coachAPI } from "@/lib/api-client";

export default async function CoachMatchesPage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();
  let matches = [];

  // Try to fetch matches - will fail gracefully if coach profile doesn't exist
  try {
    if (token) {
      // In a real implementation, we'd get the coach_id from the user's metadata or database
      // For now, we'll pass a placeholder ID and handle the error gracefully
      const coachId = 1; // TODO: Get actual coach ID from user metadata
      const matchesData = await coachAPI.getMatches(coachId, 20, token);
      matches = matchesData.matches || [];
    }
  } catch (error) {
    // Profile doesn't exist yet or API error - show empty state
    console.log("No coach profile found or API error:", error);
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
