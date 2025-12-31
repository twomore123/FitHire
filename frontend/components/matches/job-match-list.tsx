"use client";

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
      <Card>
        <CardContent className="pt-6">
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold mb-2">No Matches Yet</h3>
            <p className="text-muted-foreground mb-4">
              Complete your profile to start seeing job matches
            </p>
            <p className="text-sm text-muted-foreground max-w-md mx-auto">
              Once your profile is verified and complete, you'll see your top 20 job matches here,
              ranked by FitScore with detailed breakdowns showing why each job is a good fit.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {matches.map((match, index) => (
        <Card key={match.job_id}>
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-sm font-medium text-muted-foreground">
                    #{index + 1}
                  </span>
                  <CardTitle>{match.title}</CardTitle>
                </div>
                <CardDescription>
                  {match.city}, {match.state} • {match.role_type}
                </CardDescription>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-primary">
                  {Math.round(match.fitscore * 100)}
                </div>
                <div className="text-xs text-muted-foreground">FitScore</div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-2">Job Description</h4>
                  <p className="text-sm text-muted-foreground line-clamp-3">
                    {match.description}
                  </p>
                </div>

                {match.compensation_type && (
                  <div>
                    <h4 className="font-semibold mb-2">Compensation</h4>
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
