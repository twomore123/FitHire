import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { JobPostingForm } from "@/components/forms/job-posting-form";
import { auth } from "@clerk/nextjs/server";
import { getCurrentUserProfile } from "@/lib/user";

// Disable caching for this page - each user should see their own data
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function NewJobPage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const userProfile = await getCurrentUserProfile();
  if (userProfile && userProfile.role !== "location_manager") {
    redirect("/dashboard");
  }

  const token = await getToken();

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Post New Job</h1>
        <p className="text-muted-foreground">
          Create a job listing to start finding qualified coaches
        </p>
      </div>

      <JobPostingForm token={token || ""} />
    </div>
  );
}
