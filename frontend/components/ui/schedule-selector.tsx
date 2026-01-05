"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface ScheduleSelectorProps {
  title: string;
  description: string;
  value: string[];
  onChange: (value: string[]) => void;
}

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
const DAY_ABBREVIATIONS: { [key: string]: string } = {
  Monday: "Mon",
  Tuesday: "Tue",
  Wednesday: "Wed",
  Thursday: "Thurs",
  Friday: "Fri",
  Saturday: "Sat",
  Sunday: "Sun",
};

// Time periods matching existing API format
const TIME_PERIODS = [
  { label: "AM", value: "AM", description: "Morning (5AM-12PM)" },
  { label: "PM", value: "PM", description: "Afternoon (12PM-5PM)" },
  { label: "Evening", value: "Evening", description: "Evening (5PM-9PM)" },
];

export function ScheduleSelector({ title, description, value, onChange }: ScheduleSelectorProps) {
  const toggleSlot = (day: string, period: string) => {
    const slot = `${DAY_ABBREVIATIONS[day]} ${period}`;
    if (value.includes(slot)) {
      onChange(value.filter((s) => s !== slot));
    } else {
      onChange([...value, slot]);
    }
  };

  const isSelected = (day: string, period: string) => {
    const slot = `${DAY_ABBREVIATIONS[day]} ${period}`;
    return value.includes(slot);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <div className="inline-block min-w-full">
            {/* Table Header */}
            <div className="flex border-b border-zinc-200">
              <div className="w-24 flex-shrink-0 p-2 font-semibold text-sm text-zinc-600">
                Day
              </div>
              <div className="flex flex-1 overflow-x-auto">
                {TIME_PERIODS.map((period) => (
                  <div
                    key={period.value}
                    className="flex-1 p-2 text-center text-sm font-medium text-zinc-600"
                    title={period.description}
                  >
                    {period.label}
                  </div>
                ))}
              </div>
            </div>

            {/* Table Body */}
            {DAYS.map((day) => (
              <div key={day} className="flex border-b border-zinc-100">
                <div className="w-24 flex-shrink-0 p-2 text-sm font-medium text-zinc-700">
                  {day}
                </div>
                <div className="flex flex-1">
                  {TIME_PERIODS.map((period) => {
                    const selected = isSelected(day, period.value);
                    return (
                      <button
                        key={`${day}-${period.value}`}
                        type="button"
                        onClick={() => toggleSlot(day, period.value)}
                        className={`flex-1 p-3 border-l border-zinc-100 transition-colors ${
                          selected
                            ? "bg-primary hover:bg-primary/90 text-white"
                            : "bg-white hover:bg-zinc-50"
                        }`}
                        title={`${day} ${period.label} ${period.description}${selected ? " (selected)" : ""}`}
                      >
                        <div className="text-center">
                          {selected ? "✓" : ""}
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Selected count */}
        <div className="mt-4 text-sm text-muted-foreground">
          {value.length} time slot{value.length !== 1 ? "s" : ""} selected
        </div>

        {/* Quick actions */}
        <div className="mt-2 flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => {
              // Select all weekday mornings (Mon-Fri AM)
              const morningSlots: string[] = [];
              ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].forEach((day) => {
                morningSlots.push(`${DAY_ABBREVIATIONS[day]} AM`);
              });
              onChange(morningSlots);
            }}
            className="text-xs px-3 py-1 rounded border border-zinc-300 hover:bg-zinc-50"
          >
            Weekday Mornings
          </button>
          <button
            type="button"
            onClick={() => {
              // Select all weekday afternoons (Mon-Fri PM)
              const afternoonSlots: string[] = [];
              ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].forEach((day) => {
                afternoonSlots.push(`${DAY_ABBREVIATIONS[day]} PM`);
              });
              onChange(afternoonSlots);
            }}
            className="text-xs px-3 py-1 rounded border border-zinc-300 hover:bg-zinc-50"
          >
            Weekday Afternoons
          </button>
          <button
            type="button"
            onClick={() => {
              // Select all weekday evenings (Mon-Fri Evening)
              const eveningSlots: string[] = [];
              ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].forEach((day) => {
                eveningSlots.push(`${DAY_ABBREVIATIONS[day]} Evening`);
              });
              onChange(eveningSlots);
            }}
            className="text-xs px-3 py-1 rounded border border-zinc-300 hover:bg-zinc-50"
          >
            Weekday Evenings
          </button>
          <button
            type="button"
            onClick={() => {
              // Select all weekend slots
              const weekendSlots: string[] = [];
              ["Saturday", "Sunday"].forEach((day) => {
                TIME_PERIODS.forEach((period) => {
                  weekendSlots.push(`${DAY_ABBREVIATIONS[day]} ${period.value}`);
                });
              });
              onChange(weekendSlots);
            }}
            className="text-xs px-3 py-1 rounded border border-zinc-300 hover:bg-zinc-50"
          >
            All Weekend
          </button>
          <button
            type="button"
            onClick={() => onChange([])}
            className="text-xs px-3 py-1 rounded border border-zinc-300 hover:bg-zinc-50 text-red-600"
          >
            Clear All
          </button>
        </div>
      </CardContent>
    </Card>
  );
}
