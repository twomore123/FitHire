"use client";

import { useEffect, useState } from "react";
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
    defaultValue: 0.25,
  },
  {
    key: "experience" as keyof CustomWeights,
    label: "Experience",
    description: "Years of coaching experience",
    defaultValue: 0.20,
  },
  {
    key: "availability" as keyof CustomWeights,
    label: "Availability",
    description: "Schedule match and flexibility",
    defaultValue: 0.15,
  },
  {
    key: "location" as keyof CustomWeights,
    label: "Location",
    description: "Geographic proximity to job",
    defaultValue: 0.15,
  },
  {
    key: "cultural_fit" as keyof CustomWeights,
    label: "Cultural Fit",
    description: "Coaching style and values alignment",
    defaultValue: 0.15,
  },
  {
    key: "engagement" as keyof CustomWeights,
    label: "Engagement",
    description: "Profile completeness and activity",
    defaultValue: 0.10,
  },
];

export function WeightingSliders({ value, onChange }: WeightingSlidersProps) {
  const [localWeights, setLocalWeights] = useState<CustomWeights>(value);
  const [isValid, setIsValid] = useState(true);

  // Calculate total weight
  const total = Object.values(localWeights).reduce((sum, weight) => sum + weight, 0);
  const totalPercentage = Math.round(total * 100);

  // Validate that weights sum to 1.0 (with small tolerance for floating point)
  useEffect(() => {
    const valid = Math.abs(total - 1.0) < 0.01;
    setIsValid(valid);
    if (valid) {
      // Normalize to exactly 1.0 before calling onChange
      const normalized = {
        ...localWeights,
      };
      // Adjust the largest value to make total exactly 1.0
      const diff = 1.0 - total;
      const largestKey = Object.entries(normalized).reduce((a, b) => (b[1] > a[1] ? b : a))[0] as keyof CustomWeights;
      normalized[largestKey] = normalized[largestKey] + diff;
      onChange(normalized);
    }
  }, [localWeights, total, onChange]);

  const handleSliderChange = (key: keyof CustomWeights, newValue: number) => {
    setLocalWeights({
      ...localWeights,
      [key]: newValue,
    });
  };

  const resetToBalanced = () => {
    const balanced: CustomWeights = {
      certifications: 0.25,
      experience: 0.20,
      availability: 0.15,
      location: 0.15,
      cultural_fit: 0.15,
      engagement: 0.10,
    };
    setLocalWeights(balanced);
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
                <div className="text-right">
                  <span className="text-2xl font-bold">{percentage}%</span>
                </div>
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

        {/* Total indicator */}
        <div className="pt-4 border-t border-zinc-200">
          <div className="flex justify-between items-center">
            <div>
              <Label className="text-lg font-semibold">Total</Label>
              <p className="text-xs text-muted-foreground">Must equal 100%</p>
            </div>
            <div className="text-right">
              <span
                className={`text-3xl font-bold ${
                  isValid ? "text-green-600" : "text-red-600"
                }`}
              >
                {totalPercentage}%
              </span>
            </div>
          </div>
          {!isValid && (
            <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-800">
                ⚠ Weights must sum to exactly 100%. Current total: {totalPercentage}%
              </p>
            </div>
          )}
          {isValid && (
            <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-md">
              <p className="text-sm text-green-800">
                ✓ Weights are valid and sum to 100%
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
