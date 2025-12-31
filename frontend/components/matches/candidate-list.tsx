"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FitScoreDisplay } from "@/components/fitscore/fitscore-display";

interface Candidate {
  coach_id: number;
  first_name: string;
  last_name: string;
  email: string;
  city: string;
  state: string;
  role_type: string;
  years_experience: number;
  certifications: string[];
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

interface CandidateListProps {
  candidates: Candidate[];
}

export function CandidateList({ candidates }: CandidateListProps) {
  if (candidates.length === 0) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-center py-12">
            <div className="text-6xl mb-4">👥</div>
            <h3 className="text-xl font-semibold mb-2">No Candidates Found</h3>
            <p className="text-muted-foreground mb-4">
              No coaches currently match this job's requirements
            </p>
            <p className="text-sm text-muted-foreground max-w-md mx-auto">
              Try adjusting your FitScore threshold or weighting preset to see more candidates,
              or wait for more coaches to create profiles.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {candidates.map((candidate, index) => (
        <Card key={candidate.coach_id}>
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-sm font-medium text-muted-foreground">
                    #{index + 1}
                  </span>
                  <CardTitle>
                    {candidate.first_name} {candidate.last_name}
                  </CardTitle>
                </div>
                <CardDescription>
                  {candidate.city}, {candidate.state} • {candidate.role_type}
                </CardDescription>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-primary">
                  {Math.round(candidate.fitscore * 100)}
                </div>
                <div className="text-xs text-muted-foreground">FitScore</div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-2">Experience</h4>
                  <p className="text-sm">
                    {candidate.years_experience} {candidate.years_experience === 1 ? "year" : "years"} of professional experience
                  </p>
                </div>

                <div>
                  <h4 className="font-semibold mb-2">Certifications</h4>
                  <div className="flex flex-wrap gap-2">
                    {candidate.certifications.map((cert: string) => (
                      <span
                        key={cert}
                        className="px-2 py-1 bg-zinc-100 rounded-md text-xs font-medium"
                      >
                        {cert}
                      </span>
                    ))}
                    {candidate.certifications.length === 0 && (
                      <span className="text-sm text-muted-foreground">
                        No certifications listed
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button size="sm">View Full Profile</Button>
                  <Button size="sm" variant="outline">
                    Contact
                  </Button>
                </div>
              </div>

              <div>
                <FitScoreDisplay
                  totalScore={candidate.fitscore}
                  breakdown={candidate.fitscore_breakdown}
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
