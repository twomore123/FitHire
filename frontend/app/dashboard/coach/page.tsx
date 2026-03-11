import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { auth } from "@clerk/nextjs/server";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { coachAPI } from "@/lib/api-client";
import { ScheduleDisplay } from "@/components/ui/schedule-display";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function CoachProfilePage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();
  let existingCoach: any = null;

  // Fetch the existing coach profile
  try {
    if (token) {
      const coachList = await coachAPI.list({ page: 1, page_size: 1 }, token);
      if (coachList.coaches && coachList.coaches.length > 0) {
        existingCoach = coachList.coaches[0];
      }
    }
  } catch (error) {
    console.error("Failed to fetch coach profile:", error);
  }

  // If no coach profile exists, show create prompt
  if (!existingCoach) {
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
              <h3 className="text-xl font-semibold mb-2">No Profile Yet</h3>
              <p className="text-muted-foreground mb-6 max-w-sm mx-auto">
                Create your coach profile to start matching with jobs
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

  const completeness = Math.round((existingCoach.profile_completeness || 0) * 100);
  const isVerified = !!existingCoach.verified_at;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="bg-white rounded-2xl shadow-sm border border-border/50 p-8 mb-6">
        <div className="flex justify-between items-start">
          <div className="flex gap-6 items-start flex-1">
            <div className="relative">
              {existingCoach.profile_image_url ? (
                <div className="relative w-28 h-28 rounded-2xl overflow-hidden border-2 border-primary/20 shadow-lg flex-shrink-0">
                  <Image
                    src={existingCoach.profile_image_url}
                    alt="Profile"
                    fill
                    className="object-cover"
                  />
                </div>
              ) : (
                <div className="w-28 h-28 rounded-2xl bg-gradient-to-br from-primary/10 to-primary/5 border-2 border-primary/10 flex items-center justify-center flex-shrink-0 shadow-lg">
                  <span className="text-4xl font-bold text-primary">
                    {user.firstName?.charAt(0) || "C"}
                  </span>
                </div>
              )}
              {isVerified && (
                <div className="absolute -bottom-1 -right-1 w-8 h-8 bg-primary rounded-lg border-3 border-white flex items-center justify-center shadow-md">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
              )}
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold tracking-tight mb-1">
                {user.firstName} {user.lastName}
              </h1>
              <p className="text-muted-foreground mb-3">
                {existingCoach.city}, {existingCoach.state} &middot; {existingCoach.years_experience} years experience
              </p>
              <div className="flex items-center gap-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                  {completeness}% Complete
                </span>
                {isVerified && (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                    Verified
                  </span>
                )}
              </div>
            </div>
          </div>
          <Link href="/dashboard/coach/edit">
            <Button variant="outline" size="lg">Edit Profile</Button>
          </Link>
        </div>
      </div>

      {/* Status Banner */}
      <div className={`rounded-xl p-4 mb-6 ${
        isVerified
          ? 'bg-primary/5 border border-primary/10'
          : 'bg-amber-50 border border-amber-100'
      }`}>
        <p className={`text-sm ${isVerified ? 'text-primary' : 'text-amber-700'}`}>
          {isVerified
            ? "Your profile has been verified. You can now see job matches and apply to opportunities."
            : "Your profile is currently under review. Once verified, you'll be able to see job matches and apply to opportunities."}
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card className="border-0 shadow-sm">
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Name</div>
              <div className="font-medium mt-0.5">{user.firstName} {user.lastName}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Email</div>
              <div className="font-medium mt-0.5">{user.emailAddresses[0]?.emailAddress}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Location</div>
              <div className="font-medium mt-0.5">{existingCoach.city}, {existingCoach.state}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Experience</div>
              <div className="font-medium mt-0.5">{existingCoach.years_experience} years</div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-sm">
          <CardHeader>
            <CardTitle>Certifications</CardTitle>
          </CardHeader>
          <CardContent>
            {existingCoach.certifications && existingCoach.certifications.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {existingCoach.certifications.map((cert: any, index: number) => (
                  <span
                    key={index}
                    className="px-3 py-1.5 bg-primary/10 text-primary rounded-lg text-xs font-medium"
                  >
                    {cert.name}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No certifications added yet. Click &quot;Edit Profile&quot; to add your certifications.
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="md:col-span-2 border-0 shadow-sm">
          <CardHeader>
            <CardTitle>Availability</CardTitle>
            <CardDescription>Your available time slots</CardDescription>
          </CardHeader>
          <CardContent>
            {existingCoach.available_times && existingCoach.available_times.length > 0 ? (
              <ScheduleDisplay availableTimes={existingCoach.available_times} />
            ) : (
              <p className="text-sm text-muted-foreground">
                No availability set. Click &quot;Edit Profile&quot; to set your available times.
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="md:col-span-2 border-0 shadow-sm">
          <CardHeader>
            <CardTitle>Profile Completeness</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Progress</span>
                <span className="font-semibold text-primary">{completeness}%</span>
              </div>
              <div className="w-full bg-primary/10 rounded-full h-2">
                <div className="bg-primary h-2 rounded-full transition-all" style={{ width: `${completeness}%` }}></div>
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                Complete your profile to increase your match visibility
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {existingCoach.bio && (
        <Card className="mt-6 border-0 shadow-sm">
          <CardHeader>
            <CardTitle>Bio</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground whitespace-pre-wrap leading-relaxed">
              {existingCoach.bio}
            </p>
          </CardContent>
        </Card>
      )}

      {(existingCoach.lifestyle_tags?.length > 0 || existingCoach.movement_tags?.length > 0 || existingCoach.instruction_tags?.length > 0) && (
        <Card className="mt-6 border-0 shadow-sm">
          <CardHeader>
            <CardTitle>Coaching Style</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {existingCoach.lifestyle_tags && existingCoach.lifestyle_tags.length > 0 && (
              <div>
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Lifestyle</h4>
                <div className="flex flex-wrap gap-2">
                  {existingCoach.lifestyle_tags.map((tag: string) => (
                    <span key={tag} className="px-3 py-1.5 bg-purple-50 text-purple-700 rounded-lg text-xs font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {existingCoach.movement_tags && existingCoach.movement_tags.length > 0 && (
              <div>
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Movement</h4>
                <div className="flex flex-wrap gap-2">
                  {existingCoach.movement_tags.map((tag: string) => (
                    <span key={tag} className="px-3 py-1.5 bg-primary/10 text-primary rounded-lg text-xs font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {existingCoach.instruction_tags && existingCoach.instruction_tags.length > 0 && (
              <div>
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Instruction</h4>
                <div className="flex flex-wrap gap-2">
                  {existingCoach.instruction_tags.map((tag: string) => (
                    <span key={tag} className="px-3 py-1.5 bg-amber-50 text-amber-700 rounded-lg text-xs font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
