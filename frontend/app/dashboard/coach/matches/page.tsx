import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default async function CoachMatchesPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  // In a real implementation, we would fetch matches from the API here
  // const matches = await coachAPI.getMatches(coachId, 20, token);

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">My Job Matches</h1>
        <p className="text-muted-foreground">
          Jobs ranked by FitScore based on your profile
        </p>
      </div>

      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold mb-2">No Matches Yet</h3>
            <p className="text-muted-foreground mb-4">
              Complete your profile to start seeing job matches
            </p>
            <p className="text-sm text-muted-foreground max-w-md mx-auto">
              Once your profile is verified and complete, you'll see your top 20 job matches here,
              ranked by FitScore with detailed breakdowns showing why each job is a good fit.
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-3 gap-4">
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
    </div>
  );
}
