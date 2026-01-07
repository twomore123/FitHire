import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScheduleDisplay } from "@/components/ui/schedule-display";

// Disable caching for this page
export const dynamic = 'force-dynamic';
export const revalidate = 0;

async function getCoach(coachId: number, token: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/coaches/${coachId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    }
  );

  if (!res.ok) {
    console.error(`Failed to fetch coach ${coachId}: ${res.status} ${res.statusText}`);
    throw new Error("Failed to fetch coach");
  }

  return res.json();
}

export default async function CoachProfilePage({
  params
}: {
  params: Promise<{ coachId: string }> | { coachId: string }
}) {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  // Await params if it's a Promise (Next.js 15+)
  const resolvedParams = params instanceof Promise ? await params : params;
  const token = await getToken();
  const coachId = parseInt(resolvedParams.coachId);

  console.log(`Fetching coach profile for coach ID: ${coachId}`);

  let coach: any = null;
  let error: string | null = null;

  try {
    if (token) {
      coach = await getCoach(coachId, token);
      console.log(`Coach fetched successfully:`, {
        id: coach?.id,
        has_user: !!coach?.user,
        user_email: coach?.user?.email,
      });
    }
  } catch (err: any) {
    console.error("Error fetching coach:", err);
    error = err.message;
  }

  if (!coach) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <h3 className="text-xl font-semibold mb-2">Coach Not Found</h3>
              <p className="text-muted-foreground mb-4">
                The coach profile you're looking for doesn't exist or you don't have access to it.
              </p>
              {error && (
                <p className="text-sm text-red-600 mb-4">Error: {error}</p>
              )}
              <Button asChild>
                <Link href="/dashboard/manager">Back to Dashboard</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-4">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/dashboard/manager">← Back to Jobs</Link>
        </Button>
      </div>

      <div className="mb-6">
        <h1 className="text-4xl font-bold mb-2">
          {coach.user?.first_name || "Coach"} {coach.user?.last_name || `#${coach.id}`}
        </h1>
        <p className="text-muted-foreground">
          {coach.city}, {coach.state}
        </p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>About</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm whitespace-pre-wrap">
              {coach.bio || "No bio provided"}
            </p>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Experience</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm">
                {coach.years_experience} {coach.years_experience === 1 ? "year" : "years"} of professional experience
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Certifications</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {coach.certifications && coach.certifications.length > 0 ? (
                  coach.certifications.map((cert: any, idx: number) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-zinc-100 rounded-md text-xs font-medium"
                    >
                      {typeof cert === 'string' ? cert : cert.name}
                    </span>
                  ))
                ) : (
                  <span className="text-sm text-muted-foreground">
                    No certifications listed
                  </span>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {coach.specialties && coach.specialties.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Specialties</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {coach.specialties.map((specialty: string) => (
                  <span
                    key={specialty}
                    className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs font-medium"
                  >
                    {specialty}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Availability</CardTitle>
          </CardHeader>
          <CardContent>
            {coach.available_times && coach.available_times.length > 0 ? (
              <ScheduleDisplay availableTimes={coach.available_times} />
            ) : (
              <p className="text-sm text-muted-foreground">
                No availability listed
              </p>
            )}
          </CardContent>
        </Card>

        {(coach.lifestyle_tags?.length > 0 || coach.movement_tags?.length > 0 || coach.instruction_tags?.length > 0) && (
          <Card>
            <CardHeader>
              <CardTitle>Coaching Style</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {coach.lifestyle_tags && coach.lifestyle_tags.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2 text-sm">Lifestyle</h4>
                  <div className="flex flex-wrap gap-2">
                    {coach.lifestyle_tags.map((tag: string) => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-purple-100 text-purple-700 rounded-md text-xs font-medium"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {coach.movement_tags && coach.movement_tags.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2 text-sm">Movement</h4>
                  <div className="flex flex-wrap gap-2">
                    {coach.movement_tags.map((tag: string) => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-orange-100 text-orange-700 rounded-md text-xs font-medium"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {coach.instruction_tags && coach.instruction_tags.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2 text-sm">Instruction</h4>
                  <div className="flex flex-wrap gap-2">
                    {coach.instruction_tags.map((tag: string) => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-teal-100 text-teal-700 rounded-md text-xs font-medium"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Contact</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p className="text-sm">
                <span className="font-semibold">Email:</span>{" "}
                {coach.user?.email ? (
                  <a href={`mailto:${coach.user.email}`} className="text-blue-600 hover:underline">
                    {coach.user.email}
                  </a>
                ) : (
                  <span className="text-muted-foreground">Not available</span>
                )}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
