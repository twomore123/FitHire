import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CandidateList } from "@/components/matches/candidate-list";
import { jobAPI } from "@/lib/api-client";

export default async function JobDetailPage({ params }: { params: { jobId: string } }) {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();
  const jobId = parseInt(params.jobId);
  let job: any = null;
  let candidates: any[] = [];

  try {
    if (token) {
      // Fetch job details
      job = await jobAPI.get(jobId, token);

      // Fetch candidates for this job
      const candidatesData = await jobAPI.getCandidates(jobId, 20, token);
      candidates = candidatesData.candidates || [];
    }
  } catch (error) {
    console.log("Error fetching job or candidates:", error);
  }

  if (!job) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <h3 className="text-xl font-semibold mb-2">Job Not Found</h3>
              <p className="text-muted-foreground mb-4">
                The job you're looking for doesn't exist or you don't have access to it.
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
      <div className="mb-8">
        <Link href="/dashboard/manager">
          <Button variant="ghost" size="sm" className="mb-4">
            ← Back to Jobs
          </Button>
        </Link>
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-4xl font-bold mb-2">{job.title}</h1>
            <p className="text-muted-foreground">
              {job.city}, {job.state} • {job.role_type}
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">Edit Job</Button>
            <span className={`px-3 py-2 rounded-md text-sm font-medium ${
              job.status === 'open' ? 'bg-green-100 text-green-700' :
              job.status === 'filled' ? 'bg-blue-100 text-blue-700' :
              'bg-zinc-100 text-zinc-700'
            }`}>
              {job.status}
            </span>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Job Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                {job.description}
              </p>
            </CardContent>
          </Card>

          <div className="mt-6">
            <h2 className="text-2xl font-bold mb-4">
              Matched Candidates ({candidates.length})
            </h2>
            <CandidateList candidates={candidates} />
          </div>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Requirements</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Experience</h4>
                <p className="text-sm">
                  Minimum {job.min_experience} {job.min_experience === 1 ? 'year' : 'years'}
                </p>
              </div>

              {job.required_certifications && job.required_certifications.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Required Certifications</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.required_certifications.map((cert: string) => (
                      <span
                        key={cert}
                        className="px-2 py-1 bg-red-100 text-red-700 rounded-md text-xs font-medium"
                      >
                        {cert}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {job.preferred_certifications && job.preferred_certifications.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Preferred Certifications</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.preferred_certifications.map((cert: string) => (
                      <span
                        key={cert}
                        className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs font-medium"
                      >
                        {cert}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {job.required_availability && job.required_availability.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Required Availability</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.required_availability.map((slot: string) => (
                      <span
                        key={slot}
                        className="px-2 py-1 bg-zinc-100 rounded-md text-xs font-medium"
                      >
                        {slot}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>FitScore Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Weighting Preset</h4>
                <p className="text-sm capitalize">
                  {job.weighting_preset.replace('_', ' ')}
                </p>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Threshold</h4>
                <p className="text-sm">
                  {(job.fitscore_threshold * 100).toFixed(0)}% minimum
                </p>
              </div>
            </CardContent>
          </Card>

          {job.compensation_type && (
            <Card>
              <CardHeader>
                <CardTitle>Compensation</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm">
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
