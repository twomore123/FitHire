"use client";

interface ScheduleDisplayProps {
  availableTimes: string[];
}

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const DAY_ABBREVIATIONS: { [key: string]: string } = {
  Monday: "Mon",
  Tuesday: "Tue",
  Wednesday: "Wed",
  Thursday: "Thu",
  Friday: "Fri",
  Saturday: "Sat",
  Sunday: "Sun",
};

const TIME_PERIODS = [
  { label: "AM", value: "AM" },
  { label: "PM", value: "PM" },
  { label: "Evening", value: "Evening" },
];

export function ScheduleDisplay({ availableTimes }: ScheduleDisplayProps) {
  const isSlotSelected = (day: string, period: string): boolean => {
    const slot = `${DAY_ABBREVIATIONS[day]} ${period}`;
    return availableTimes.includes(slot);
  };

  return (
    <div className="space-y-3">
      {/* Header Row */}
      <div className="grid grid-cols-4 gap-2">
        <div className="text-xs font-medium text-muted-foreground"></div>
        {TIME_PERIODS.map((period) => (
          <div key={period.value} className="text-xs font-medium text-center text-muted-foreground">
            {period.label}
          </div>
        ))}
      </div>

      {/* Day Rows */}
      {DAYS.map((day) => (
        <div key={day} className="grid grid-cols-4 gap-2">
          <div className="text-sm font-medium flex items-center">
            {DAY_ABBREVIATIONS[day]}
          </div>
          {TIME_PERIODS.map((period) => {
            const selected = isSlotSelected(day, period.value);
            return (
              <div
                key={period.value}
                className={`
                  h-10 rounded-md border text-xs font-medium
                  flex items-center justify-center transition-colors
                  ${
                    selected
                      ? "bg-primary text-primary-foreground border-primary"
                      : "bg-zinc-50 text-muted-foreground border-zinc-200"
                  }
                `}
              >
                {selected ? "✓" : ""}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
