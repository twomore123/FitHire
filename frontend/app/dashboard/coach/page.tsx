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
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <div className="text-6xl mb-4">👤</div>
              <h3 className="text-xl font-semibold mb-2">No Profile Yet</h3>
              <p className="text-muted-foreground mb-4">
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
      {/* Hero Section with Profile Image */}
      <div className="mb-8">
        <div className="flex justify-between items-start">
          <div className="flex gap-6 items-start flex-1">
            <div className="relative">
              {existingCoach.profile_image_url ? (
                <div className="relative w-32 h-32 rounded-full overflow-hidden border-4 border-primary shadow-2xl flex-shrink-0">
                  <Image
                    src={existingCoach.profile_image_url}
                    alt="Profile"
                    fill
                    className="object-cover"
                  />
                </div>
              ) : (
                <div className="w-32 h-32 rounded-full bg-gradient-to-br from-zinc-100 to-zinc-200 border-4 border-zinc-300 flex items-center justify-center flex-shrink-0 shadow-lg">
                  <span className="text-5xl text-zinc-400">👤</span>
                </div>
              )}
              {isVerified && (
                <div className="absolute -bottom-1 -right-1 w-10 h-10 bg-green-500 rounded-full border-4 border-white flex items-center justify-center shadow-lg">
                  <span className="text-white text-xl">✓</span>
                </div>
              )}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-4xl font-bold">
                  {user.firstName} {user.lastName}
                </h1>
              </div>
              <p className="text-lg text-muted-foreground mb-3">
                {existingCoach.city}, {existingCoach.state} • {existingCoach.years_experience} years experience
              </p>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1 bg-blue-50 rounded-full">
                  <span className="text-sm font-medium text-blue-700">
                    {completeness}% Complete
                  </span>
                </div>
                {isVerified && (
                  <div className="flex items-center gap-2 px-3 py-1 bg-green-50 rounded-full">
                    <span className="text-sm font-medium text-green-700">✓ Verified</span>
                  </div>
                )}
              </div>
            </div>
          </div>
          <Link href="/dashboard/coach/edit">
            <Button size="lg">Edit Profile</Button>
          </Link>
        </div>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Profile Status</CardTitle>
          <CardDescription>
            {isVerified ? "Your profile is verified" : "Your profile is pending verification"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className={`p-4 border rounded-md ${isVerified ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'}`}>
            <p className={`text-sm ${isVerified ? 'text-green-800' : 'text-yellow-800'}`}>
              {isVerified
                ? "Your profile has been verified by an administrator. You can now see job matches and apply to opportunities."
                : "Your profile is currently under review. Once verified by an administrator, you'll be able to see job matches and apply to opportunities."}
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div>
              <div className="text-sm text-muted-foreground">Name</div>
              <div className="font-medium">{user.firstName} {user.lastName}</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Email</div>
              <div className="font-medium">{user.emailAddresses[0]?.emailAddress}</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Location</div>
              <div className="font-medium">{existingCoach.city}, {existingCoach.state}</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Years of Experience</div>
              <div className="font-medium">{existingCoach.years_experience} years</div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Certifications</CardTitle>
          </CardHeader>
          <CardContent>
            {existingCoach.certifications && existingCoach.certifications.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {existingCoach.certifications.map((cert: any, index: number) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs font-medium"
                  >
                    {cert.name}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No certifications added yet. Click "Edit Profile" to add your certifications.
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Availability</CardTitle>
            <CardDescription>Your available time slots</CardDescription>
          </CardHeader>
          <CardContent>
            {existingCoach.available_times && existingCoach.available_times.length > 0 ? (
              <ScheduleDisplay availableTimes={existingCoach.available_times} />
            ) : (
              <p className="text-sm text-muted-foreground">
                No availability set. Click "Edit Profile" to set your available times.
              </p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Profile Completeness</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Progress</span>
                <span className="font-medium">{completeness}%</span>
              </div>
              <div className="w-full bg-zinc-200 rounded-full h-2">
                <div className="bg-primary h-2 rounded-full" style={{ width: `${completeness}%` }}></div>
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                Complete your profile to increase your match visibility
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {existingCoach.bio && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Bio</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground whitespace-pre-wrap">
              {existingCoach.bio}
            </p>
          </CardContent>
        </Card>
      )}

      {(existingCoach.lifestyle_tags?.length > 0 || existingCoach.movement_tags?.length > 0 || existingCoach.instruction_tags?.length > 0) && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Coaching Style</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {existingCoach.lifestyle_tags && existingCoach.lifestyle_tags.length > 0 && (
              <div>
                <h4 className="font-semibold mb-2 text-sm">Lifestyle Tags</h4>
                <div className="flex flex-wrap gap-2">
                  {existingCoach.lifestyle_tags.map((tag: string) => (
                    <span key={tag} className="px-2 py-1 bg-purple-100 text-purple-700 rounded-md text-xs font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {existingCoach.movement_tags && existingCoach.movement_tags.length > 0 && (
              <div>
                <h4 className="font-semibold mb-2 text-sm">Movement Tags</h4>
                <div className="flex flex-wrap gap-2">
                  {existingCoach.movement_tags.map((tag: string) => (
                    <span key={tag} className="px-2 py-1 bg-green-100 text-green-700 rounded-md text-xs font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {existingCoach.instruction_tags && existingCoach.instruction_tags.length > 0 && (
              <div>
                <h4 className="font-semibold mb-2 text-sm">Instruction Tags</h4>
                <div className="flex flex-wrap gap-2">
                  {existingCoach.instruction_tags.map((tag: string) => (
                    <span key={tag} className="px-2 py-1 bg-orange-100 text-orange-700 rounded-md text-xs font-medium">
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
