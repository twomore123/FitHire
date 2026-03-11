import Image from "next/image";

interface BrandLogoProps {
  variant?: "fithire" | "coach360" | "icon";
  size?: "sm" | "md" | "lg";
  className?: string;
}

const dimensions = {
  fithire: { sm: { w: 120, h: 38 }, md: { w: 160, h: 50 }, lg: { w: 220, h: 69 } },
  coach360: { sm: { w: 140, h: 70 }, md: { w: 200, h: 100 }, lg: { w: 300, h: 150 } },
  icon: { sm: { w: 32, h: 32 }, md: { w: 48, h: 48 }, lg: { w: 72, h: 72 } },
};

const srcs = {
  fithire: "/logos/fithire-by-coach360.png",
  coach360: "/logos/coach360-wordmark.png",
  icon: "/logos/360-icon-green.png",
};

export function BrandLogo({ variant = "fithire", size = "md", className = "" }: BrandLogoProps) {
  const { w, h } = dimensions[variant][size];
  return (
    <Image
      src={srcs[variant]}
      alt={variant === "icon" ? "Coach 360" : variant === "coach360" ? "Coach 360" : "FitHire by Coach 360"}
      width={w}
      height={h}
      className={className}
      priority
    />
  );
}
