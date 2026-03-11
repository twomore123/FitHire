import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import Link from "next/link";
import Image from "next/image";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CandidateList } from "@/components/matches/candidate-list";
import { jobAPI } from "@/lib/api-client";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function JobDetailPage({ params }: { params: Promise<{ jobId: string }> | { jobId: string } }) {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  // Await params if it's a Promise (Next.js 15+)
  const resolvedParams = params instanceof Promise ? await params : params;
  const token = await getToken();
  const jobId = parseInt(resolvedParams.jobId);

  let job: any = null;
  let candidates: any[] = [];

  try {
    if (token) {
      if (isNaN(jobId)) {
        throw new Error("Invalid job ID");
      }

      job = await jobAPI.get(jobId, token);

      const candidatesData = await jobAPI.getCandidates(jobId, 20, token);

      candidates = (candidatesData.candidates || []).map((c: any) => ({
        coach_id: c.coach.id,
        first_name: c.coach.user?.first_name || "Coach",
        last_name: c.coach.user?.last_name || `#${c.coach.id}`,
        email: c.coach.user?.email || "",
        city: c.coach.city,
        state: c.coach.state,
        role_type: "Fitness Coach",
        years_experience: c.coach.years_experience || 0,
        certifications: Array.isArray(c.coach.certifications)
          ? c.coach.certifications.map((cert: any) =>
              typeof cert === 'string' ? cert : (cert.name || 'Unknown')
            )
          : [],
        profile_image_url: c.coach.profile_image_url,
        fitscore: c.fitscore,
        fitscore_breakdown: {
          certification_score: c.score_breakdown?.cert_score || 0,
          experience_score: c.score_breakdown?.experience_score || 0,
          availability_score: c.score_breakdown?.availability_score || 0,
          location_score: c.score_breakdown?.location_score || 0,
          culture_score: c.score_breakdown?.culture_score || 0,
          engagement_score: c.score_breakdown?.engagement_score || 0,
        },
      }));
    }
  } catch (error: any) {
    console.error("Error fetching job or candidates:", error);
  }

  if (!job) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card className="border-0 shadow-sm">
          <CardContent className="pt-6">
            <div className="text-center py-16">
              <h3 className="text-xl font-semibold mb-2">Job Not Found</h3>
              <p className="text-muted-foreground mb-6">
                The job you&apos;re looking for doesn&apos;t exist or you don&apos;t have access to it.
              </p>
              <Link href="/dashboard/manager">
                <Button>Back to Jobs</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <Link href="/dashboard/manager" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors mb-4">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
          Back to Jobs
        </Link>
      </div>

      {job.brand_banner_url && (
        <div className="relative w-full h-48 rounded-2xl overflow-hidden mb-6 shadow-sm">
          <Image
            src={job.brand_banner_url}
            alt={`${job.title} banner`}
            fill
            className="object-cover"
          />
        </div>
      )}

      <div className="bg-white rounded-2xl shadow-sm border border-border/50 p-8 mb-8">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold tracking-tight mb-2">{job.title}</h1>
            <p className="text-muted-foreground">
              {job.city}, {job.state} &middot; {job.role_type}
            </p>
          </div>
          <div className="flex gap-2 items-center">
            <Link href={`/dashboard/manager/${job.id}/edit`}>
              <Button variant="outline">Edit Job</Button>
            </Link>
            <span className={`px-3 py-2 rounded-lg text-sm font-medium ${
              job.is_active
                ? 'bg-primary/10 text-primary'
                : 'bg-muted text-muted-foreground'
            }`}>
              {job.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <Card className="border-0 shadow-sm">
            <CardHeader>
              <CardTitle>Job Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground whitespace-pre-wrap leading-relaxed">
                {job.description}
              </p>
            </CardContent>
          </Card>

          <div className="mt-6">
            <h2 className="text-2xl font-bold tracking-tight mb-4">
              Matched Candidates ({candidates.length})
            </h2>
            <CandidateList candidates={candidates} />
          </div>
        </div>

        <div className="space-y-6">
          <Card className="border-0 shadow-sm">
            <CardHeader>
              <CardTitle>Requirements</CardTitle>
            </CardHeader>
            <CardContent className="space-y-5">
              <div>
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Experience</h4>
                <p className="text-sm font-medium">
                  Minimum {job.min_experience} {job.min_experience === 1 ? 'year' : 'years'}
                </p>
              </div>

              {job.required_certifications && job.required_certifications.length > 0 && (
                <div>
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Required Certifications</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.required_certifications.map((cert: string) => (
                      <span
                        key={cert}
                        className="px-2.5 py-1 bg-red-50 text-red-600 rounded-lg text-xs font-medium"
                      >
                        {cert}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {job.preferred_certifications && job.preferred_certifications.length > 0 && (
                <div>
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Preferred Certifications</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.preferred_certifications.map((cert: string) => (
                      <span
                        key={cert}
                        className="px-2.5 py-1 bg-primary/10 text-primary rounded-lg text-xs font-medium"
                      >
                        {cert}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {job.required_availability && job.required_availability.length > 0 && (
                <div>
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Required Availability</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.required_availability.map((slot: string) => (
                      <span
                        key={slot}
                        className="px-2.5 py-1 bg-muted rounded-lg text-xs font-medium"
                      >
                        {slot}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm">
            <CardHeader>
              <CardTitle>FitScore Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">Weighting Preset</h4>
                <p className="text-sm font-medium capitalize">
                  {job.weighting_preset.replace('_', ' ')}
                </p>
              </div>
              <div>
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">Threshold</h4>
                <p className="text-sm font-medium text-primary">
                  {(job.fitscore_threshold * 100).toFixed(0)}% minimum
                </p>
              </div>
            </CardContent>
          </Card>

          {job.compensation_type && (
            <Card className="border-0 shadow-sm">
              <CardHeader>
                <CardTitle>Compensation</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm font-medium">
                  {job.compensation_type === "hourly" && "$"}
                  {job.compensation_min}
                  {job.compensation_max && ` - $${job.compensation_max}`}
                  {job.compensation_type === "hourly" && "/hour"}
                  {job.compensation_type === "salary" && "/year"}
                  {job.compensation_type === "per_class" && "/class"}
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
