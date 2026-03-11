"use client";

import Image from "next/image";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FitScoreDisplay } from "@/components/fitscore/fitscore-display";

interface JobMatch {
  job_id: number;
  title: string;
  description: string;
  city: string;
  state: string;
  role_type: string;
  compensation_type?: string;
  compensation_min?: number;
  compensation_max?: number;
  brand_logo_url?: string;
  fitscore: number;
  fitscore_breakdown: {
    certification_score: number;
    experience_score: number;
    availability_score: number;
    location_score: number;
    culture_score: number;
    engagement_score: number;
  };
}

interface JobMatchListProps {
  matches: JobMatch[];
}

export function JobMatchList({ matches }: JobMatchListProps) {
  if (matches.length === 0) {
    return (
      <Card className="border-0 shadow-sm">
        <CardContent className="pt-6">
          <div className="text-center py-16">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-5">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <path d="M8 14s1.5 2 4 2 4-2 4-2" />
                <line x1="9" y1="9" x2="9.01" y2="9" />
                <line x1="15" y1="9" x2="15.01" y2="9" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">No Matches Yet</h3>
            <p className="text-muted-foreground mb-4 max-w-md mx-auto">
              Complete your profile to start seeing job matches. Once verified, you&apos;ll see your top 20 matches ranked by FitScore.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {matches.map((match, index) => (
        <Card key={match.job_id} className="border-0 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader>
            <div className="flex justify-between items-start">
              <div className="flex gap-4 items-start flex-1">
                {match.brand_logo_url ? (
                  <div className="relative w-16 h-16 rounded-2xl overflow-hidden border-2 border-border/60 flex-shrink-0 bg-white shadow-md">
                    <Image
                      src={match.brand_logo_url}
                      alt={`${match.title} logo`}
                      fill
                      className="object-cover"
                    />
                  </div>
                ) : (
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/15 to-primary/5 border-2 border-primary/15 flex items-center justify-center flex-shrink-0 shadow-md">
                    <span className="text-2xl font-bold text-primary">
                      {match.title?.charAt(0) || "J"}
                    </span>
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
                      #{index + 1}
                    </span>
                    <CardTitle className="truncate text-lg">{match.title}</CardTitle>
                  </div>
                  <CardDescription>
                    {match.city}, {match.state} &middot; {match.role_type}
                  </CardDescription>
                  {match.compensation_type && match.compensation_min && (
                    <div className="text-xs font-medium text-primary mt-0.5">
                      ${match.compensation_min}
                      {match.compensation_max && ` - $${match.compensation_max}`}
                      {match.compensation_type === "hourly" && "/hr"}
                      {match.compensation_type === "salary" && "/yr"}
                      {match.compensation_type === "per_class" && "/class"}
                    </div>
                  )}
                </div>
              </div>
              <div className="text-right flex-shrink-0 ml-4">
                <div className="text-4xl font-bold text-primary">
                  {Math.round(match.fitscore * 100)}
                </div>
                <div className="text-xs text-muted-foreground font-medium">FitScore</div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Description</h4>
                  <p className="text-sm text-muted-foreground line-clamp-3">
                    {match.description}
                  </p>
                </div>

                {match.compensation_type && (
                  <div>
                    <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Compensation</h4>
                    <p className="text-sm">
                      {match.compensation_type === "hourly" && "$"}
                      {match.compensation_min}
                      {match.compensation_max && ` - $${match.compensation_max}`}
                      {match.compensation_type === "hourly" && "/hour"}
                      {match.compensation_type === "salary" && "/year"}
                      {match.compensation_type === "per_class" && "/class"}
                    </p>
                  </div>
                )}

                <div className="flex gap-2">
                  <Button size="sm">View Details</Button>
                  <Button size="sm" variant="outline">
                    Apply
                  </Button>
                </div>
              </div>

              <div>
                <FitScoreDisplay
                  totalScore={match.fitscore}
                  breakdown={match.fitscore_breakdown}
                  showDetails={true}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
