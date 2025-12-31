"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { coachAPI } from "@/lib/api-client";
import { useRouter } from "next/navigation";

interface CoachProfileFormProps {
  initialData?: any;
  coachId?: number;
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

const LIFESTYLE_TAGS = [
  "Wellness-Focused", "Performance-Driven", "Community-Oriented",
  "Holistic Health", "Science-Based", "Mindful Movement",
];

const MOVEMENT_TAGS = [
  "High-Energy", "Low-Impact", "Strength-Focused", "Flexibility-Focused",
  "Mind-Body Connection", "Athletic Performance",
];

const INSTRUCTION_TAGS = [
  "Motivational", "Technical", "Encouraging", "Challenging",
  "Adaptive", "Detail-Oriented",
];

export function CoachProfileForm({ initialData, coachId, token }: CoachProfileFormProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    location_id: initialData?.location_id || 1, // Default to 1 for now
    first_name: initialData?.first_name || "",
    last_name: initialData?.last_name || "",
    email: initialData?.email || "",
    phone: initialData?.phone || "",
    city: initialData?.city || "",
    state: initialData?.state || "",
    role_type: initialData?.role_type || "",
    years_experience: initialData?.years_experience || 0,
    certifications: initialData?.certifications || [],
    available_times: initialData?.available_times || [],
    lifestyle_tags: initialData?.lifestyle_tags || [],
    movement_tags: initialData?.movement_tags || [],
    instruction_tags: initialData?.instruction_tags || [],
    bio: initialData?.bio || "",
  });

  const [selectedCertifications, setSelectedCertifications] = useState<string[]>(
    initialData?.certifications?.map((c: any) => c.name) || []
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const submitData = {
        ...formData,
        certifications: selectedCertifications.map((name) => ({
          name,
          issued_date: null,
          expiry_date: null,
          credential_id: null,
        })),
      };

      if (coachId) {
        await coachAPI.update(coachId, submitData, token);
      } else {
        await coachAPI.create(submitData, token);
      }

      router.push("/dashboard/coach");
      router.refresh();
    } catch (err: any) {
      setError(err.message || "Failed to save profile");
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
          <CardTitle>Basic Information</CardTitle>
          <CardDescription>Tell us about yourself</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="first_name">First Name *</Label>
              <Input
                id="first_name"
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="last_name">Last Name *</Label>
              <Input
                id="last_name"
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email *</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone</Label>
              <Input
                id="phone"
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              />
            </div>
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

      {/* Professional Details */}
      <Card>
        <CardHeader>
          <CardTitle>Professional Details</CardTitle>
          <CardDescription>Your fitness expertise</CardDescription>
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
            <Label htmlFor="years_experience">Years of Experience *</Label>
            <Input
              id="years_experience"
              type="number"
              min="0"
              value={formData.years_experience}
              onChange={(e) => setFormData({ ...formData, years_experience: parseInt(e.target.value) || 0 })}
              required
            />
          </div>

          <div className="space-y-2">
            <Label>Certifications</Label>
            <div className="flex flex-wrap gap-2">
              {CERTIFICATIONS.map((cert) => (
                <button
                  key={cert}
                  type="button"
                  onClick={() => toggleSelection(cert, selectedCertifications, setSelectedCertifications)}
                  className={`px-3 py-1 rounded-full text-sm border ${
                    selectedCertifications.includes(cert)
                      ? "bg-primary text-white border-primary"
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

      {/* Availability */}
      <Card>
        <CardHeader>
          <CardTitle>Availability</CardTitle>
          <CardDescription>When can you work?</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex flex-wrap gap-2">
            {TIME_SLOTS.map((slot) => (
              <button
                key={slot}
                type="button"
                onClick={() => toggleSelection(slot, formData.available_times, (values) => setFormData({ ...formData, available_times: values }))}
                className={`px-3 py-1 rounded-full text-sm border ${
                  formData.available_times.includes(slot)
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

      {/* Cultural Fit Tags */}
      <Card>
        <CardHeader>
          <CardTitle>Cultural Fit</CardTitle>
          <CardDescription>What defines your coaching style?</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Lifestyle Approach</Label>
            <div className="flex flex-wrap gap-2">
              {LIFESTYLE_TAGS.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleSelection(tag, formData.lifestyle_tags, (values) => setFormData({ ...formData, lifestyle_tags: values }))}
                  className={`px-3 py-1 rounded-full text-sm border ${
                    formData.lifestyle_tags.includes(tag)
                      ? "bg-primary text-white border-primary"
                      : "bg-white border-zinc-300"
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Movement Style</Label>
            <div className="flex flex-wrap gap-2">
              {MOVEMENT_TAGS.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleSelection(tag, formData.movement_tags, (values) => setFormData({ ...formData, movement_tags: values }))}
                  className={`px-3 py-1 rounded-full text-sm border ${
                    formData.movement_tags.includes(tag)
                      ? "bg-primary text-white border-primary"
                      : "bg-white border-zinc-300"
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Instruction Style</Label>
            <div className="flex flex-wrap gap-2">
              {INSTRUCTION_TAGS.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleSelection(tag, formData.instruction_tags, (values) => setFormData({ ...formData, instruction_tags: values }))}
                  className={`px-3 py-1 rounded-full text-sm border ${
                    formData.instruction_tags.includes(tag)
                      ? "bg-primary text-white border-primary"
                      : "bg-white border-zinc-300"
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Bio */}
      <Card>
        <CardHeader>
          <CardTitle>Bio</CardTitle>
          <CardDescription>Tell employers about yourself</CardDescription>
        </CardHeader>
        <CardContent>
          <textarea
            className="w-full border border-zinc-200 rounded-md px-3 py-2 min-h-32"
            value={formData.bio}
            onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
            maxLength={2000}
            placeholder="Share your coaching philosophy, experience, and what makes you unique..."
          />
          <p className="text-xs text-muted-foreground mt-1">
            {formData.bio.length}/2000 characters
          </p>
        </CardContent>
      </Card>

      <div className="flex gap-4">
        <Button type="submit" size="lg" disabled={loading}>
          {loading ? "Saving..." : coachId ? "Update Profile" : "Create Profile"}
        </Button>
        <Button
          type="button"
          variant="outline"
          size="lg"
          onClick={() => router.push("/dashboard/coach")}
        >
          Cancel
        </Button>
      </div>
    </form>
  );
}
