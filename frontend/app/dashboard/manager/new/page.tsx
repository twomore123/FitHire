import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default async function NewJobPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Post New Job</h1>
        <p className="text-muted-foreground">
          Create a job listing to start finding qualified coaches
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Job Details</CardTitle>
          <CardDescription>
            Provide information about the position you're hiring for
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="title">Job Title</Label>
              <Input
                id="title"
                placeholder="e.g., Group Fitness Instructor"
                disabled
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="role_type">Role Type</Label>
              <Input
                id="role_type"
                placeholder="Select role type..."
                disabled
              />
              <p className="text-xs text-muted-foreground">
                Group Fitness Instructor, Personal Trainer, Yoga Instructor, or Pilates Instructor
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input id="city" placeholder="e.g., Los Angeles" disabled />
              </div>
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Input id="state" placeholder="CA" maxLength={2} disabled />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Job Description</Label>
              <textarea
                id="description"
                className="flex min-h-[120px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                placeholder="Describe the position, responsibilities, and requirements..."
                disabled
              />
            </div>

            <div className="space-y-2">
              <Label>Required Certifications</Label>
              <Input placeholder="e.g., NASM-CPT, ACE" disabled />
              <p className="text-xs text-muted-foreground">
                Candidates must have all required certifications
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="min_experience">Minimum Experience (years)</Label>
              <Input
                id="min_experience"
                type="number"
                placeholder="0"
                min="0"
                disabled
              />
            </div>

            <div className="space-y-2">
              <Label>FitScore Settings</Label>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="preset">Weighting Preset</Label>
                  <Input id="preset" value="balanced" disabled />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="threshold">Minimum FitScore</Label>
                  <Input id="threshold" value="0.60" disabled />
                </div>
              </div>
              <p className="text-xs text-muted-foreground">
                Balanced preset weighs all factors equally. Threshold of 0.60 filters for qualified candidates.
              </p>
            </div>

            <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
              <p className="text-sm text-blue-800">
                <strong>Note:</strong> This is a preview interface. In the full implementation,
                this form would submit to the backend API and create a real job listing with
                configurable FitScore settings.
              </p>
            </div>

            <div className="flex gap-4">
              <Button type="button" disabled className="flex-1">
                Save as Draft
              </Button>
              <Button type="button" disabled className="flex-1">
                Publish Job
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
