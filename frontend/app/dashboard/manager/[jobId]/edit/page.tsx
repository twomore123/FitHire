import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { JobPostingForm } from "@/components/forms/job-posting-form";
import { auth } from "@clerk/nextjs/server";
import { jobAPI } from "@/lib/api-client";
import { getCurrentUserProfile } from "@/lib/user";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function JobEditPage({ params }: { params: Promise<{ jobId: string }> | { jobId: string } }) {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const userProfile = await getCurrentUserProfile();
  if (userProfile && userProfile.role !== "location_manager") {
    redirect("/dashboard");
  }

  // Await params if it's a Promise (Next.js 15+)
  const resolvedParams = params instanceof Promise ? await params : params;
  const token = await getToken();
  const jobId = parseInt(resolvedParams.jobId);
  let existingJob = null;

  // Fetch the existing job
  try {
    if (token) {
      existingJob = await jobAPI.get(jobId, token);
    }
  } catch (error) {
    console.error("Failed to fetch job:", error);
    redirect("/dashboard/manager");
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          Edit Job Posting
        </h1>
        <p className="text-muted-foreground">
          Update your job posting details
        </p>
      </div>

      <JobPostingForm
        token={token || ""}
        initialData={existingJob}
        jobId={jobId}
      />
    </div>
  );
}
