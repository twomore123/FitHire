import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Link from "next/link";
import { auth } from "@clerk/nextjs/server";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { adminAPI } from "@/lib/api-client";
import { VerificationActions } from "@/components/admin/verification-actions";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function VerificationQueuePage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();
  let pendingCoaches: any[] = [];

  // Fetch pending coaches
  try {
    if (token) {
      pendingCoaches = await adminAPI.getVerificationQueue(token);
    }
  } catch (error) {
    console.error("Failed to fetch verification queue:", error);
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <Link href="/dashboard/admin">
          <Button variant="ghost" size="sm" className="mb-4">
            ← Back to Admin Dashboard
          </Button>
        </Link>
        <h1 className="text-4xl font-bold mb-2">Verification Queue</h1>
        <p className="text-muted-foreground">
          Review and approve coach profiles pending verification
        </p>
      </div>

      {pendingCoaches.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <div className="text-6xl mb-4">✓</div>
              <h3 className="text-xl font-semibold mb-2">All Caught Up!</h3>
              <p className="text-muted-foreground">
                No coaches pending verification at this time
              </p>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {pendingCoaches.map((coach) => (
            <Card key={coach.id}>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle>Coach ID: {coach.id}</CardTitle>
                    <CardDescription>
                      {coach.city}, {coach.state} • {coach.years_experience} years experience
                    </CardDescription>
                  </div>
                  <VerificationActions coachId={coach.id} token={token || ""} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold mb-2 text-sm">Certifications</h4>
                    {coach.certifications && coach.certifications.length > 0 ? (
                      <div className="flex flex-wrap gap-2">
                        {coach.certifications.map((cert: any, index: number) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs font-medium"
                          >
                            {cert.name}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-muted-foreground">No certifications listed</p>
                    )}
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2 text-sm">Availability</h4>
                    {coach.available_times && coach.available_times.length > 0 ? (
                      <div className="flex flex-wrap gap-2">
                        {coach.available_times.slice(0, 5).map((slot: string) => (
                          <span
                            key={slot}
                            className="px-2 py-1 bg-zinc-100 rounded-md text-xs font-medium"
                          >
                            {slot}
                          </span>
                        ))}
                        {coach.available_times.length > 5 && (
                          <span className="px-2 py-1 text-xs text-muted-foreground">
                            +{coach.available_times.length - 5} more
                          </span>
                        )}
                      </div>
                    ) : (
                      <p className="text-sm text-muted-foreground">No availability set</p>
                    )}
                  </div>

                  {coach.bio && (
                    <div className="md:col-span-2">
                      <h4 className="font-semibold mb-2 text-sm">Bio</h4>
                      <p className="text-sm text-muted-foreground line-clamp-3">
                        {coach.bio}
                      </p>
                    </div>
                  )}

                  <div className="md:col-span-2">
                    <div className="flex gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">Profile Completeness:</span>{" "}
                        <span className="font-medium">
                          {Math.round((coach.profile_completeness || 0) * 100)}%
                        </span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Created:</span>{" "}
                        <span className="font-medium">
                          {new Date(coach.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <div className="grid md:grid-cols-3 gap-4 mt-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Pending Review
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{pendingCoaches.length}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Coaches awaiting verification
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Avg Completeness
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {pendingCoaches.length > 0
                ? Math.round(
                    (pendingCoaches.reduce(
                      (sum, c) => sum + (c.profile_completeness || 0),
                      0
                    ) /
                      pendingCoaches.length) *
                      100
                  )
                : 0}
              %
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Average profile quality
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Action Required
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{pendingCoaches.length}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Coaches need your review
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
