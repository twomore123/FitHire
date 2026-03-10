"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";

export interface CustomWeights {
  certifications: number;
  experience: number;
  availability: number;
  location: number;
  cultural_fit: number;
  engagement: number;
}

interface WeightingSlidersProps {
  value: CustomWeights;
  onChange: (weights: CustomWeights) => void;
}

const WEIGHT_CRITERIA = [
  {
    key: "certifications" as keyof CustomWeights,
    label: "Certifications",
    description: "Required and preferred certifications match",
  },
  {
    key: "experience" as keyof CustomWeights,
    label: "Experience",
    description: "Years of coaching experience",
  },
  {
    key: "availability" as keyof CustomWeights,
    label: "Availability",
    description: "Schedule match and flexibility",
  },
  {
    key: "location" as keyof CustomWeights,
    label: "Location",
    description: "Geographic proximity to job",
  },
  {
    key: "cultural_fit" as keyof CustomWeights,
    label: "Cultural Fit",
    description: "Coaching style and values alignment",
  },
  {
    key: "engagement" as keyof CustomWeights,
    label: "Engagement",
    description: "Profile completeness and activity",
  },
];

const BALANCED_WEIGHTS: CustomWeights = {
  certifications: 0.25,
  experience: 0.20,
  availability: 0.15,
  location: 0.15,
  cultural_fit: 0.15,
  engagement: 0.10,
};

export function WeightingSliders({ value, onChange }: WeightingSlidersProps) {
  const [localWeights, setLocalWeights] = useState<CustomWeights>(value);

  const handleSliderChange = (key: keyof CustomWeights, newValue: number) => {
    const otherKeys = WEIGHT_CRITERIA.map((c) => c.key).filter((k) => k !== key);
    const remaining = 1.0 - newValue;
    const otherTotal = otherKeys.reduce((sum, k) => sum + localWeights[k], 0);

    const newWeights = { ...localWeights, [key]: newValue };

    if (otherTotal === 0) {
      // Distribute evenly among others
      const evenShare = remaining / otherKeys.length;
      otherKeys.forEach((k) => {
        newWeights[k] = evenShare;
      });
    } else {
      // Distribute proportionally among others
      otherKeys.forEach((k) => {
        newWeights[k] = (localWeights[k] / otherTotal) * remaining;
      });
    }

    // Fix floating point drift — ensure exact sum of 1.0
    const total = Object.values(newWeights).reduce((s, v) => s + v, 0);
    const drift = 1.0 - total;
    const largestKey = otherKeys.reduce((a, b) => (newWeights[b] > newWeights[a] ? b : a));
    newWeights[largestKey] = Math.max(0, newWeights[largestKey] + drift);

    setLocalWeights(newWeights);
    onChange(newWeights);
  };

  const resetToBalanced = () => {
    setLocalWeights(BALANCED_WEIGHTS);
    onChange(BALANCED_WEIGHTS);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle>Custom Weighting</CardTitle>
            <CardDescription>
              Adjust the importance of each criterion in the FitScore calculation
            </CardDescription>
          </div>
          <button
            type="button"
            onClick={resetToBalanced}
            className="text-xs px-3 py-1 rounded border border-zinc-300 hover:bg-zinc-50"
          >
            Reset to Balanced
          </button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {WEIGHT_CRITERIA.map((criterion) => {
          const weight = localWeights[criterion.key];
          const percentage = Math.round(weight * 100);

          return (
            <div key={criterion.key} className="space-y-2">
              <div className="flex justify-between items-center">
                <div>
                  <Label htmlFor={`weight-${criterion.key}`} className="font-medium">
                    {criterion.label}
                  </Label>
                  <p className="text-xs text-muted-foreground">{criterion.description}</p>
                </div>
                <span className="text-2xl font-bold">{percentage}%</span>
              </div>
              <input
                id={`weight-${criterion.key}`}
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={weight}
                onChange={(e) => handleSliderChange(criterion.key, parseFloat(e.target.value))}
                className="w-full h-2 rounded-lg appearance-none cursor-pointer bg-zinc-200"
                style={{
                  background: `linear-gradient(to right, hsl(var(--primary)) 0%, hsl(var(--primary)) ${percentage}%, rgb(228, 228, 231) ${percentage}%, rgb(228, 228, 231) 100%)`,
                }}
              />
            </div>
          );
        })}

        <div className="pt-4 border-t border-zinc-200">
          <div className="flex justify-between items-center">
            <div>
              <Label className="text-lg font-semibold">Total</Label>
              <p className="text-xs text-muted-foreground">Always sums to 100%</p>
            </div>
            <span className="text-3xl font-bold text-green-600">100%</span>
          </div>
          <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-md">
            <p className="text-sm text-green-800">
              ✓ Weights automatically balance to 100%
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
