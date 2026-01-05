import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { CoachProfileForm } from "@/components/forms/coach-profile-form";
import { auth } from "@clerk/nextjs/server";
import { coachAPI } from "@/lib/api-client";

export default async function CoachEditPage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();

  // Fetch the existing coach profile
  // For Phase 1, we fetch the list and use the first coach (one coach per user)
  let existingCoach = null;
  let coachId = null;

  try {
    if (token) {
      const coachList = await coachAPI.list({ page: 1, page_size: 1 }, token);
      if (coachList.coaches && coachList.coaches.length > 0) {
        existingCoach = coachList.coaches[0];
        coachId = existingCoach.id;
      }
    }
  } catch (error) {
    console.error("Failed to fetch coach profile:", error);
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          {existingCoach ? "Edit Coach Profile" : "Create Coach Profile"}
        </h1>
        <p className="text-muted-foreground">
          {existingCoach
            ? "Update your professional profile and certifications"
            : "Set up your professional profile to start matching with jobs"}
        </p>
      </div>

      <CoachProfileForm
        token={token || ""}
        initialData={existingCoach}
        coachId={coachId}
      />
    </div>
  );
}
