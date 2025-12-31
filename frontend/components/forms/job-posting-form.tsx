"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { jobAPI } from "@/lib/api-client";
import { useRouter } from "next/navigation";

interface JobPostingFormProps {
  initialData?: any;
  jobId?: number;
  token: string;
}

const ROLE_TYPES = [
  "Group Fitness Instructor",
  "Personal Trainer",
  "Yoga Instructor",
  "Pilates Instructor",
];

const CERTIFICATIONS = [
  "NASM-CPT",
  "ACE",
  "ACSM",
  "RYT-200",
  "RYT-500",
  "PMA",
  "STOTT",
];

const TIME_SLOTS = [
  "Mon AM", "Mon PM", "Mon Evening",
  "Tue AM", "Tue PM", "Tue Evening",
  "Wed AM", "Wed PM", "Wed Evening",
  "Thu AM", "Thu PM", "Thu Evening",
  "Fri AM", "Fri PM", "Fri Evening",
  "Sat AM", "Sat PM", "Sat Evening",
  "Sun AM", "Sun PM", "Sun Evening",
];

const CULTURE_TAGS = [
  "Wellness-Focused", "Performance-Driven", "Community-Oriented",
  "Holistic Health", "Science-Based", "Mindful Movement",
  "High-Energy", "Low-Impact", "Strength-Focused",
  "Motivational", "Technical", "Encouraging",
];

const WEIGHTING_PRESETS = [
  { value: "balanced", label: "Balanced", description: "Equal weight across all criteria" },
  { value: "experience_heavy", label: "Experience-Heavy", description: "Prioritizes experience and certifications" },
  { value: "culture_heavy", label: "Culture-Heavy", description: "Prioritizes cultural fit tags" },
  { value: "availability_focused", label: "Availability-Focused", description: "Prioritizes schedule match" },
];

export function JobPostingForm({ initialData, jobId, token }: JobPostingFormProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    location_id: initialData?.location_id || 1, // Default to 1 for now
    title: initialData?.title || "",
    description: initialData?.description || "",
    role_type: initialData?.role_type || "",
    required_certifications: initialData?.required_certifications || [],
    preferred_certifications: initialData?.preferred_certifications || [],
    min_experience: initialData?.min_experience || 0,
    required_availability: initialData?.required_availability || [],
    city: initialData?.city || "",
    state: initialData?.state || "",
    culture_tags: initialData?.culture_tags || [],
    compensation_type: initialData?.compensation_type || "hourly",
    compensation_min: initialData?.compensation_min || "",
    compensation_max: initialData?.compensation_max || "",
    weighting_preset: initialData?.weighting_preset || "balanced",
    fitscore_threshold: initialData?.fitscore_threshold || 0.60,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const submitData = {
        ...formData,
        compensation_min: formData.compensation_min ? parseFloat(formData.compensation_min) : null,
        compensation_max: formData.compensation_max ? parseFloat(formData.compensation_max) : null,
      };

      if (jobId) {
        await jobAPI.update(jobId, submitData, token);
      } else {
        await jobAPI.create(submitData, token);
      }

      router.push("/dashboard/manager");
      router.refresh();
    } catch (err: any) {
      setError(err.message || "Failed to save job posting");
    } finally {
      setLoading(false);
    }
  };

  const toggleSelection = (value: string, currentValues: string[], setter: (values: string[]) => void) => {
    if (currentValues.includes(value)) {
      setter(currentValues.filter((v) => v !== value));
    } else {
      setter([...currentValues, value]);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Basic Information */}
      <Card>
        <CardHeader>
          <CardTitle>Job Details</CardTitle>
          <CardDescription>Basic information about the position</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">Job Title *</Label>
            <Input
              id="title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g., Group Fitness Instructor - Weekend AM"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description *</Label>
            <textarea
              id="description"
              className="w-full border border-zinc-200 rounded-md px-3 py-2 min-h-32"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Describe the role, responsibilities, and what makes your studio unique..."
              required
            />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="city">City *</Label>
              <Input
                id="city"
                value={formData.city}
                onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="state">State *</Label>
              <Input
                id="state"
                value={formData.state}
                onChange={(e) => setFormData({ ...formData, state: e.target.value.toUpperCase() })}
                maxLength={2}
                placeholder="CA"
                required
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Role Requirements */}
      <Card>
        <CardHeader>
          <CardTitle>Role Requirements</CardTitle>
          <CardDescription>What qualifications are needed?</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="role_type">Role Type *</Label>
            <select
              id="role_type"
              className="w-full border border-zinc-200 rounded-md px-3 py-2"
              value={formData.role_type}
              onChange={(e) => setFormData({ ...formData, role_type: e.target.value })}
              required
            >
              <option value="">Select a role</option>
              {ROLE_TYPES.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="min_experience">Minimum Years of Experience</Label>
            <Input
              id="min_experience"
              type="number"
              min="0"
              value={formData.min_experience}
              onChange={(e) => setFormData({ ...formData, min_experience: parseInt(e.target.value) || 0 })}
            />
          </div>

          <div className="space-y-2">
            <Label>Required Certifications (must have all)</Label>
            <div className="flex flex-wrap gap-2">
              {CERTIFICATIONS.map((cert) => (
                <button
                  key={cert}
                  type="button"
                  onClick={() => toggleSelection(cert, formData.required_certifications, (values) => setFormData({ ...formData, required_certifications: values }))}
                  className={`px-3 py-1 rounded-full text-sm border ${
                    formData.required_certifications.includes(cert)
                      ? "bg-primary text-white border-primary"
                      : "bg-white border-zinc-300"
                  }`}
                >
                  {cert}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Preferred Certifications (bonus)</Label>
            <div className="flex flex-wrap gap-2">
              {CERTIFICATIONS.map((cert) => (
                <button
                  key={cert}
                  type="button"
                  onClick={() => toggleSelection(cert, formData.preferred_certifications, (values) => setFormData({ ...formData, preferred_certifications: values }))}
                  className={`px-3 py-1 rounded-full text-sm border ${
                    formData.preferred_certifications.includes(cert)
                      ? "bg-blue-500 text-white border-blue-500"
                      : "bg-white border-zinc-300"
                  }`}
                >
                  {cert}
                </button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Schedule */}
      <Card>
        <CardHeader>
          <CardTitle>Schedule Requirements</CardTitle>
          <CardDescription>When do you need coverage?</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex flex-wrap gap-2">
            {TIME_SLOTS.map((slot) => (
              <button
                key={slot}
                type="button"
                onClick={() => toggleSelection(slot, formData.required_availability, (values) => setFormData({ ...formData, required_availability: values }))}
                className={`px-3 py-1 rounded-full text-sm border ${
                  formData.required_availability.includes(slot)
                    ? "bg-primary text-white border-primary"
                    : "bg-white border-zinc-300"
                }`}
              >
                {slot}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Culture */}
      <Card>
        <CardHeader>
          <CardTitle>Culture & Style</CardTitle>
          <CardDescription>What type of coach are you looking for?</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex flex-wrap gap-2">
            {CULTURE_TAGS.map((tag) => (
              <button
                key={tag}
                type="button"
                onClick={() => toggleSelection(tag, formData.culture_tags, (values) => setFormData({ ...formData, culture_tags: values }))}
                className={`px-3 py-1 rounded-full text-sm border ${
                  formData.culture_tags.includes(tag)
                    ? "bg-primary text-white border-primary"
                    : "bg-white border-zinc-300"
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Compensation */}
      <Card>
        <CardHeader>
          <CardTitle>Compensation (Optional)</CardTitle>
          <CardDescription>Salary or hourly rate information</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="compensation_type">Type</Label>
            <select
              id="compensation_type"
              className="w-full border border-zinc-200 rounded-md px-3 py-2"
              value={formData.compensation_type}
              onChange={(e) => setFormData({ ...formData, compensation_type: e.target.value })}
            >
              <option value="hourly">Hourly</option>
              <option value="salary">Salary</option>
              <option value="per_class">Per Class</option>
            </select>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="compensation_min">Minimum</Label>
              <Input
                id="compensation_min"
                type="number"
                step="0.01"
                value={formData.compensation_min}
                onChange={(e) => setFormData({ ...formData, compensation_min: e.target.value })}
                placeholder="0.00"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="compensation_max">Maximum</Label>
              <Input
                id="compensation_max"
                type="number"
                step="0.01"
                value={formData.compensation_max}
                onChange={(e) => setFormData({ ...formData, compensation_max: e.target.value })}
                placeholder="0.00"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Matching Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Matching Configuration</CardTitle>
          <CardDescription>How should FitScore prioritize candidates?</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="weighting_preset">Weighting Preset</Label>
            <select
              id="weighting_preset"
              className="w-full border border-zinc-200 rounded-md px-3 py-2"
              value={formData.weighting_preset}
              onChange={(e) => setFormData({ ...formData, weighting_preset: e.target.value })}
            >
              {WEIGHTING_PRESETS.map((preset) => (
                <option key={preset.value} value={preset.value}>
                  {preset.label} - {preset.description}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="fitscore_threshold">
              FitScore Threshold: {formData.fitscore_threshold.toFixed(2)}
            </Label>
            <input
              id="fitscore_threshold"
              type="range"
              min="0.40"
              max="0.80"
              step="0.05"
              value={formData.fitscore_threshold}
              onChange={(e) => setFormData({ ...formData, fitscore_threshold: parseFloat(e.target.value) })}
              className="w-full"
            />
            <p className="text-xs text-muted-foreground">
              Only show candidates with FitScore above this threshold (0.40 - 0.80)
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-4">
        <Button type="submit" size="lg" disabled={loading}>
          {loading ? "Saving..." : jobId ? "Update Job" : "Post Job"}
        </Button>
        <Button
          type="button"
          variant="outline"
          size="lg"
          onClick={() => router.push("/dashboard/manager")}
        >
          Cancel
        </Button>
      </div>
    </form>
  );
}
