import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { CoachProfileForm } from "@/components/forms/coach-profile-form";
import { auth } from "@clerk/nextjs/server";

export default async function CoachEditPage() {
  const user = await currentUser();
  const { getToken } = await auth();

  if (!user) {
    redirect("/sign-in");
  }

  const token = await getToken();

  // In a real implementation, we would fetch the existing coach profile
  // const coach = await coachAPI.get(coachId, token);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          Edit Coach Profile
        </h1>
        <p className="text-muted-foreground">
          Update your professional profile and certifications
        </p>
      </div>

      <CoachProfileForm token={token || ""} />
    </div>
  );
}
