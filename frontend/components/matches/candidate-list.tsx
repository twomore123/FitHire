"use client";

import Link from "next/link";
import Image from "next/image";
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
  profile_image_url?: string;
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
        <Card key={candidate.coach_id} className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <div className="flex justify-between items-start">
              <div className="flex gap-4 items-start flex-1">
                {candidate.profile_image_url ? (
                  <div className="relative w-20 h-20 rounded-full overflow-hidden border-2 border-primary/30 shadow-md flex-shrink-0">
                    <Image
                      src={candidate.profile_image_url}
                      alt={`${candidate.first_name} ${candidate.last_name}`}
                      fill
                      className="object-cover"
                    />
                  </div>
                ) : (
                  <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-100 to-blue-200 border-2 border-blue-300 flex items-center justify-center flex-shrink-0 shadow-md">
                    <span className="text-3xl font-semibold text-blue-600">
                      {candidate.first_name?.charAt(0) || "C"}{candidate.last_name?.charAt(0) || ""}
                    </span>
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm font-medium text-muted-foreground">
                      #{index + 1}
                    </span>
                    <CardTitle className="truncate">
                      {candidate.first_name} {candidate.last_name}
                    </CardTitle>
                  </div>
                  <CardDescription className="mb-1">
                    {candidate.city}, {candidate.state} • {candidate.role_type}
                  </CardDescription>
                  <div className="text-xs text-muted-foreground">
                    {candidate.years_experience} {candidate.years_experience === 1 ? "year" : "years"} of experience
                  </div>
                </div>
              </div>
              <div className="text-right flex-shrink-0 ml-4">
                <div className="text-4xl font-bold bg-gradient-to-br from-primary to-primary/70 bg-clip-text text-transparent">
                  {Math.round(candidate.fitscore * 100)}
                </div>
                <div className="text-xs text-muted-foreground font-medium">FitScore</div>
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

                <div>
                  <Link href={`/dashboard/manager/coaches/${candidate.coach_id}`}>
                    <Button size="sm">View Full Profile</Button>
                  </Link>
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
