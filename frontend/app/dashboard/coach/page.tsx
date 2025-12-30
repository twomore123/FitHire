import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default async function CoachProfilePage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold mb-2">Coach Profile</h1>
          <p className="text-muted-foreground">
            Manage your professional profile and certifications
          </p>
        </div>
        <Button>Edit Profile</Button>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Profile Status</CardTitle>
          <CardDescription>
            Your profile is pending verification
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
            <p className="text-sm text-yellow-800">
              Your profile is currently under review. Once verified by an administrator,
              you'll be able to see job matches and apply to opportunities.
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
              <div className="text-sm text-muted-foreground">Role Type</div>
              <div className="font-medium text-muted-foreground">Not set</div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Certifications</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              No certifications added yet. Click "Edit Profile" to add your certifications.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Availability</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              No availability set. Click "Edit Profile" to set your available times.
            </p>
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
                <span className="font-medium">20%</span>
              </div>
              <div className="w-full bg-zinc-200 rounded-full h-2">
                <div className="bg-primary h-2 rounded-full" style={{ width: "20%" }}></div>
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                Complete your profile to increase your match visibility
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Next Steps</CardTitle>
          <CardDescription>
            Complete these steps to get the most out of FitHire
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            <li className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
              <span>Add your certifications</span>
            </li>
            <li className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
              <span>Set your availability</span>
            </li>
            <li className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
              <span>Upload a profile photo</span>
            </li>
            <li className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
              <span>Add a verification video</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
