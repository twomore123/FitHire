import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface FitScoreBreakdown {
  certification_score: number;
  experience_score: number;
  availability_score: number;
  location_score: number;
  culture_score: number;
  engagement_score: number;
}

interface FitScoreDisplayProps {
  totalScore: number;
  breakdown: FitScoreBreakdown;
  showDetails?: boolean;
}

const SCORE_DESCRIPTIONS = {
  certification_score: {
    name: "Certifications",
    description: "Match between required/preferred certifications",
  },
  experience_score: {
    name: "Experience",
    description: "Years of professional experience vs requirements",
  },
  availability_score: {
    name: "Availability",
    description: "Schedule overlap with required time slots",
  },
  location_score: {
    name: "Location",
    description: "Geographic proximity to job location",
  },
  culture_score: {
    name: "Cultural Fit",
    description: "Alignment with coaching style and values",
  },
  engagement_score: {
    name: "Engagement",
    description: "Profile completeness and activity",
  },
};

function getScoreColor(score: number): string {
  if (score >= 0.8) return "bg-primary";
  if (score >= 0.6) return "bg-primary/70";
  if (score >= 0.4) return "bg-amber-400";
  return "bg-red-400";
}

function getScoreTextColor(score: number): string {
  if (score >= 0.8) return "text-primary";
  if (score >= 0.6) return "text-primary/80";
  if (score >= 0.4) return "text-amber-600";
  return "text-red-500";
}

function getScoreRingColor(score: number): string {
  if (score >= 0.8) return "text-primary";
  if (score >= 0.6) return "text-primary/70";
  if (score >= 0.4) return "text-amber-400";
  return "text-red-400";
}

export function FitScoreDisplay({ totalScore, breakdown, showDetails = true }: FitScoreDisplayProps) {
  const scorePercentage = Math.round(totalScore * 100);
  const scoreTextColor = getScoreTextColor(totalScore);
  const scoreRingColor = getScoreRingColor(totalScore);

  return (
    <div className="space-y-4">
      {/* Overall FitScore */}
      <div className="flex items-center gap-4">
        <div className="relative w-20 h-20">
          <svg className="w-20 h-20 transform -rotate-90">
            <circle
              cx="40"
              cy="40"
              r="36"
              stroke="currentColor"
              strokeWidth="6"
              fill="none"
              className="text-muted/50"
            />
            <circle
              cx="40"
              cy="40"
              r="36"
              stroke="currentColor"
              strokeWidth="6"
              fill="none"
              strokeDasharray={`${2 * Math.PI * 36}`}
              strokeDashoffset={`${2 * Math.PI * 36 * (1 - totalScore)}`}
              className={scoreRingColor}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={`text-xl font-bold ${scoreTextColor}`}>
              {scorePercentage}
            </span>
          </div>
        </div>

        <div>
          <div className="text-2xl font-bold">FitScore</div>
          <div className="text-sm text-muted-foreground">
            {scorePercentage >= 80 && "Excellent Match"}
            {scorePercentage >= 60 && scorePercentage < 80 && "Good Match"}
            {scorePercentage >= 40 && scorePercentage < 60 && "Fair Match"}
            {scorePercentage < 40 && "Low Match"}
          </div>
        </div>
      </div>

      {/* Detailed Breakdown */}
      {showDetails && (
        <div className="space-y-3">
          <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Score Breakdown</div>
          {Object.entries(breakdown).map(([key, value]) => {
            const info = SCORE_DESCRIPTIONS[key as keyof FitScoreBreakdown];
            const scoreValue = Math.round(value * 100);
            const barColor = getScoreColor(value);

            return (
              <div key={key} className="space-y-1">
                <div className="flex justify-between items-center text-sm">
                  <span className="font-medium">{info.name}</span>
                  <span className={`font-semibold ${getScoreTextColor(value)}`}>
                    {scoreValue}%
                  </span>
                </div>
                <div className="w-full bg-muted rounded-full h-1.5">
                  <div
                    className={`h-1.5 rounded-full transition-all ${barColor}`}
                    style={{ width: `${scoreValue}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export function FitScoreCard({ totalScore, breakdown }: Omit<FitScoreDisplayProps, 'showDetails'>) {
  return (
    <Card className="border-0 shadow-sm">
      <CardHeader>
        <CardTitle>FitScore Analysis</CardTitle>
        <CardDescription>
          How well this candidate matches the job requirements
        </CardDescription>
      </CardHeader>
      <CardContent>
        <FitScoreDisplay totalScore={totalScore} breakdown={breakdown} showDetails={true} />
      </CardContent>
    </Card>
  );
}
