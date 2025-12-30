import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white">
      <nav className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">FitHire</h1>
          <div className="flex gap-4">
            <Link href="/sign-in">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/sign-up">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <h2 className="text-5xl font-bold mb-6">
            Find Your Perfect Fitness Match
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Connect fitness professionals with opportunities through intelligent FitScore matching.
            Streamline hiring, reduce turnover, and build stronger fitness teams.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/sign-up">
              <Button size="lg">Start Matching</Button>
            </Link>
            <Link href="#features">
              <Button variant="outline" size="lg">Learn More</Button>
            </Link>
          </div>
        </div>

        <div id="features" className="grid md:grid-cols-3 gap-8 mb-16">
          <Card>
            <CardHeader>
              <CardTitle>Intelligent Matching</CardTitle>
              <CardDescription>
                Our FitScore algorithm analyzes certifications, experience, availability, and cultural fit
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Get ranked candidates automatically, filtered by configurable thresholds and weighting presets.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>For Coaches</CardTitle>
              <CardDescription>
                Create your profile, showcase your certifications, and discover opportunities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                See your top job matches instantly with detailed score breakdowns showing why you're a great fit.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>For Managers</CardTitle>
              <CardDescription>
                Post jobs, review candidates, and find the perfect fit for your team
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Access top 20 candidates ranked by FitScore with detailed breakdowns of each match component.
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="text-center">
          <h3 className="text-3xl font-bold mb-4">Ready to get started?</h3>
          <p className="text-lg text-muted-foreground mb-6">
            Join fitness professionals and hiring managers using FitHire
          </p>
          <Link href="/sign-up">
            <Button size="lg">Create Your Account</Button>
          </Link>
        </div>
      </main>

      <footer className="border-t mt-16">
        <div className="container mx-auto px-4 py-8 text-center text-sm text-muted-foreground">
          <p>© 2025 FitHire. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
