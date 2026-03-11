"use client";

import { useState } from "react";
import Image from "next/image";
import { SignIn } from "@clerk/nextjs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

type Role = "coach" | "manager";

export default function SignInPage() {
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);

  const handleRoleSelect = (role: Role) => {
    localStorage.setItem("fithire_role", role);
    setSelectedRole(role);
  };

  if (selectedRole) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-zinc-50 to-white">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <Image src="/logos/360-icon-green.png" alt="Coach 360" width={72} height={72} className="mx-auto mb-5" priority />
            <h1 className="text-3xl font-bold mb-2">Welcome Back</h1>
            <p className="text-muted-foreground">
              Sign in as a {selectedRole === "coach" ? "Coach" : "Hiring Manager"}
            </p>
          </div>
          <SignIn
            appearance={{
              elements: {
                rootBox: "mx-auto",
                card: "shadow-lg",
              },
            }}
          />
          <div className="text-center mt-4">
            <button
              onClick={() => setSelectedRole(null)}
              className="text-sm text-muted-foreground hover:text-foreground underline underline-offset-4"
            >
              Choose a different role
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-zinc-50 to-white">
      <div className="w-full max-w-lg px-4">
        <div className="text-center mb-8">
          <Image src="/logos/fithire-by-coach360.png" alt="FitHire by Coach 360" width={240} height={75} className="mx-auto mb-6" priority />
          <h1 className="text-3xl font-bold mb-2">Welcome to FitHire</h1>
          <p className="text-muted-foreground">
            How are you using FitHire?
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Card
            className="cursor-pointer transition-all hover:shadow-md hover:border-zinc-400"
            onClick={() => handleRoleSelect("coach")}
          >
            <CardHeader className="text-center pb-2">
              <div className="text-4xl mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-10 h-10 mx-auto text-zinc-700">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
              </div>
              <CardTitle className="text-lg">Coach</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <CardDescription>
                Find jobs and showcase your coaching profile
              </CardDescription>
            </CardContent>
          </Card>

          <Card
            className="cursor-pointer transition-all hover:shadow-md hover:border-zinc-400"
            onClick={() => handleRoleSelect("manager")}
          >
            <CardHeader className="text-center pb-2">
              <div className="text-4xl mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-10 h-10 mx-auto text-zinc-700">
                  <rect width="20" height="14" x="2" y="7" rx="2" ry="2" />
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                </svg>
              </div>
              <CardTitle className="text-lg">Hiring Manager</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <CardDescription>
                Post jobs and find the right coaching talent
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
