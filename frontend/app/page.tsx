import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BrandLogo } from "@/components/brand-logo";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-border/50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/">
            <BrandLogo variant="fithire" size="sm" />
          </Link>
          <div className="flex gap-3 items-center">
            <Link href="/sign-in">
              <Button variant="ghost" className="text-muted-foreground hover:text-foreground">
                Sign In
              </Button>
            </Link>
            <Link href="/sign-up">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-brand-green-light via-white to-white" />
        <div className="absolute top-20 right-0 w-[500px] h-[500px] rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] rounded-full bg-primary/5 blur-3xl" />

        <div className="relative container mx-auto px-6">
          <div className="max-w-3xl mx-auto text-center">
            <div className="flex justify-center mb-10">
              <Image
                src="/logos/360-icon-green.png"
                alt="Coach 360"
                width={120}
                height={120}
                priority
              />
            </div>

            <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6 leading-[1.1]">
              Find Your Perfect
              <br />
              <span className="text-primary">Fitness Match</span>
            </h1>

            <p className="text-lg text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
              Connect fitness professionals with opportunities through intelligent FitScore matching.
              Streamline hiring, reduce turnover, and build stronger fitness teams.
            </p>

            <div className="flex gap-4 justify-center">
              <Link href="/sign-up">
                <Button size="lg" className="px-8 h-12 text-base shadow-lg shadow-primary/20">
                  Start Matching
                </Button>
              </Link>
              <Link href="#features">
                <Button variant="outline" size="lg" className="px-8 h-12 text-base">
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 bg-secondary/30">
        <div className="container mx-auto px-6">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold mb-3">How It Works</h2>
            <p className="text-muted-foreground max-w-lg mx-auto">
              Our platform connects the right coaches with the right opportunities using data-driven matching.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="border-0 shadow-sm bg-white hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 2L2 7l10 5 10-5-10-5z" />
                    <path d="M2 17l10 5 10-5" />
                    <path d="M2 12l10 5 10-5" />
                  </svg>
                </div>
                <CardTitle className="text-lg">Intelligent Matching</CardTitle>
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

            <Card className="border-0 shadow-sm bg-white hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                </div>
                <CardTitle className="text-lg">For Coaches</CardTitle>
                <CardDescription>
                  Create your profile, showcase your certifications, and discover opportunities
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  See your top job matches instantly with detailed score breakdowns showing why you&apos;re a great fit.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-sm bg-white hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                  </svg>
                </div>
                <CardTitle className="text-lg">For Managers</CardTitle>
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
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-3xl font-bold mb-4">Ready to get started?</h3>
            <p className="text-lg text-muted-foreground mb-8">
              Join fitness professionals and hiring managers using Coach 360
            </p>
            <Link href="/sign-up">
              <Button size="lg" className="px-10 h-12 text-base shadow-lg shadow-primary/20">
                Create Your Account
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-secondary/30">
        <div className="container mx-auto px-6 py-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <BrandLogo variant="coach360" size="sm" />
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} Coach 360. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
