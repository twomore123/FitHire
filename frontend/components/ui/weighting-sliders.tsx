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

type Priority = "low" | "medium" | "high";
type Priorities = Record<keyof CustomWeights, Priority>;

interface WeightingSlidersProps {
  value: CustomWeights;
  onChange: (weights: CustomWeights) => void;
}

const WEIGHT_CRITERIA: {
  key: keyof CustomWeights;
  label: string;
  description: string;
}[] = [
  { key: "certifications", label: "Certifications", description: "Required and preferred certifications match" },
  { key: "experience", label: "Experience", description: "Years of coaching experience" },
  { key: "availability", label: "Availability", description: "Schedule match and flexibility" },
  { key: "location", label: "Location", description: "Geographic proximity to job" },
  { key: "cultural_fit", label: "Cultural Fit", description: "Coaching style and values alignment" },
  { key: "engagement", label: "Engagement", description: "Profile completeness and activity" },
];

const PRIORITY_UNITS: Record<Priority, number> = {
  low: 1,
  medium: 2,
  high: 3,
};

const PRIORITY_LABELS: Record<Priority, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
};

const PRIORITIES: Priority[] = ["low", "medium", "high"];

function prioritiesToWeights(priorities: Priorities): CustomWeights {
  const totalUnits = Object.values(priorities).reduce(
    (sum, p) => sum + PRIORITY_UNITS[p],
    0
  );
  const weights: Partial<CustomWeights> = {};
  for (const { key } of WEIGHT_CRITERIA) {
    weights[key] = PRIORITY_UNITS[priorities[key]] / totalUnits;
  }
  return weights as CustomWeights;
}

const DEFAULT_PRIORITIES: Priorities = {
  certifications: "medium",
  experience: "medium",
  availability: "medium",
  location: "medium",
  cultural_fit: "medium",
  engagement: "medium",
};

export function WeightingSliders({ onChange }: WeightingSlidersProps) {
  // `value` prop kept for interface compatibility but priorities are managed internally
  const [priorities, setPriorities] = useState<Priorities>(DEFAULT_PRIORITIES);

  const handlePriorityChange = (key: keyof CustomWeights, priority: Priority) => {
    const updated = { ...priorities, [key]: priority };
    setPriorities(updated);
    onChange(prioritiesToWeights(updated));
  };

  const resetToBalanced = () => {
    setPriorities(DEFAULT_PRIORITIES);
    onChange(prioritiesToWeights(DEFAULT_PRIORITIES));
  };

  const weights = prioritiesToWeights(priorities);

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle>Custom Weighting</CardTitle>
            <CardDescription>
              Set the importance of each criterion in the FitScore calculation
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
      <CardContent className="space-y-4">
        {WEIGHT_CRITERIA.map(({ key, label, description }) => {
          const current = priorities[key];

          return (
            <div key={key} className="flex items-center gap-4">
              <div className="flex-1 min-w-0">
                <Label className="font-medium">{label}</Label>
                <p className="text-xs text-muted-foreground truncate">{description}</p>
              </div>

              <div className="flex rounded-md border border-zinc-200 overflow-hidden shrink-0">
                {PRIORITIES.map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => handlePriorityChange(key, p)}
                    className={`px-6 py-1.5 text-sm font-medium transition-colors ${
                      current === p
                        ? "bg-primary text-white"
                        : "bg-white text-zinc-600 hover:bg-zinc-50"
                    } ${p !== "low" ? "border-l border-zinc-200" : ""}`}
                  >
                    {PRIORITY_LABELS[p]}
                  </button>
                ))}
              </div>
            </div>
          );
        })}

      </CardContent>
    </Card>
  );
}
