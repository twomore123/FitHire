import Image from "next/image";

interface BrandLogoProps {
  variant?: "fithire" | "coach360" | "icon";
  size?: "sm" | "md" | "lg";
  className?: string;
}

const dimensions = {
  fithire: { sm: { w: 160, h: 50 }, md: { w: 220, h: 69 }, lg: { w: 300, h: 94 } },
  coach360: { sm: { w: 180, h: 90 }, md: { w: 260, h: 130 }, lg: { w: 360, h: 180 } },
  icon: { sm: { w: 44, h: 44 }, md: { w: 64, h: 64 }, lg: { w: 96, h: 96 } },
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
