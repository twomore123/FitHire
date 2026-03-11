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
      <Card className="border-0 shadow-sm">
        <CardContent className="pt-6">
          <div className="text-center py-16">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-5">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">No Candidates Found</h3>
            <p className="text-muted-foreground mb-4 max-w-md mx-auto">
              No coaches currently match this job&apos;s requirements. Try adjusting your FitScore threshold or weighting preset.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {candidates.map((candidate, index) => (
        <Card key={candidate.coach_id} className="border-0 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader>
            <div className="flex justify-between items-start">
              <div className="flex gap-4 items-start flex-1">
                {candidate.profile_image_url ? (
                  <div className="relative w-16 h-16 rounded-xl overflow-hidden border border-primary/20 shadow-sm flex-shrink-0">
                    <Image
                      src={candidate.profile_image_url}
                      alt={`${candidate.first_name} ${candidate.last_name}`}
                      fill
                      className="object-cover"
                    />
                  </div>
                ) : (
                  <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/10 flex items-center justify-center flex-shrink-0">
                    <span className="text-xl font-semibold text-primary">
                      {candidate.first_name?.charAt(0) || "C"}{candidate.last_name?.charAt(0) || ""}
                    </span>
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
                      #{index + 1}
                    </span>
                    <CardTitle className="truncate text-lg">
                      {candidate.first_name} {candidate.last_name}
                    </CardTitle>
                  </div>
                  <CardDescription>
                    {candidate.city}, {candidate.state} &middot; {candidate.role_type}
                  </CardDescription>
                  <div className="text-xs text-muted-foreground mt-0.5">
                    {candidate.years_experience} {candidate.years_experience === 1 ? "year" : "years"} of experience
                  </div>
                </div>
              </div>
              <div className="text-right flex-shrink-0 ml-4">
                <div className="text-4xl font-bold text-primary">
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
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Experience</h4>
                  <p className="text-sm">
                    {candidate.years_experience} {candidate.years_experience === 1 ? "year" : "years"} of professional experience
                  </p>
                </div>

                <div>
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">Certifications</h4>
                  <div className="flex flex-wrap gap-2">
                    {candidate.certifications.map((cert: string) => (
                      <span
                        key={cert}
                        className="px-2.5 py-1 bg-primary/10 text-primary rounded-lg text-xs font-medium"
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
