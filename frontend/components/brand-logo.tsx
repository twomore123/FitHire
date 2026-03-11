interface BrandLogoProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizes = {
  sm: "text-lg",
  md: "text-2xl",
  lg: "text-4xl",
};

export function BrandLogo({ size = "md", className = "" }: BrandLogoProps) {
  return (
    <span className={`font-light tracking-tight ${sizes[size]} ${className}`}>
      coach
      <span className="relative inline-flex items-center ml-0.5">
        <span className="font-light">3</span>
        <span className="relative">
          <span className="font-light">6</span>
        </span>
        <span className="relative">
          <span className="font-light">0</span>
          <svg
            viewBox="0 0 24 24"
            fill="none"
            className="absolute -top-[0.15em] -right-[0.05em] w-[0.55em] h-[0.55em]"
          >
            <circle cx="12" cy="12" r="10.5" stroke="currentColor" strokeWidth="1.5" fill="none" />
            <path
              d="M14.5 8.5C14.5 8.5 13 10 12 12C11 14 10.5 16 10.5 16"
              stroke="currentColor"
              strokeWidth="1.2"
              strokeLinecap="round"
            />
            <path
              d="M12 12C12 12 13.5 11 15 11.5"
              stroke="currentColor"
              strokeWidth="1.2"
              strokeLinecap="round"
            />
            <path
              d="M12 12C12 12 10.5 10.5 9 11"
              stroke="currentColor"
              strokeWidth="1.2"
              strokeLinecap="round"
            />
          </svg>
        </span>
      </span>
    </span>
  );
}
