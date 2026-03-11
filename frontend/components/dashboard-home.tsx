"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export function DashboardHome({ firstName }: { firstName: string | null }) {
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    setRole(localStorage.getItem("fithire_role"));
  }, []);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-10">
        <h1 className="text-4xl font-bold tracking-tight mb-2">
          Welcome back, {firstName || "there"}
        </h1>
        <p className="text-muted-foreground text-lg">
          What would you like to do today?
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {role !== "manager" && (
          <Card className={`border-0 shadow-sm hover:shadow-md transition-shadow ${role === "coach" ? "md:col-span-2" : ""}`}>
            <CardHeader>
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center mb-3">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <CardTitle>Coach Profile</CardTitle>
              <CardDescription>
                Manage your professional profile and view job matches
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              <Link href="/dashboard/coach">
                <Button className="w-full">View Profile</Button>
              </Link>
              <Link href="/dashboard/coach/matches">
                <Button variant="outline" className="w-full">View My Matches</Button>
              </Link>
            </CardContent>
          </Card>
        )}

        {role !== "coach" && (
          <Card className={`border-0 shadow-sm hover:shadow-md transition-shadow ${role === "manager" ? "md:col-span-2" : ""}`}>
            <CardHeader>
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center mb-3">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                </svg>
              </div>
              <CardTitle>Hiring Manager</CardTitle>
              <CardDescription>
                Post jobs and review coach candidates
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              <Link href="/dashboard/manager">
                <Button className="w-full">View Jobs</Button>
              </Link>
              <Link href="/dashboard/manager/new">
                <Button variant="outline" className="w-full">Post New Job</Button>
              </Link>
            </CardContent>
          </Card>
        )}
      </div>

      <Card className="mt-8 border-0 shadow-sm">
        <CardHeader>
          <CardTitle className="text-sm font-medium text-muted-foreground">Quick Stats</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-2">
            <div className="text-4xl font-bold text-primary">0</div>
            <div className="text-sm text-muted-foreground mt-1">Job Matches</div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
