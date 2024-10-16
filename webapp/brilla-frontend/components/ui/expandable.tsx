import { cn } from "@/lib/utils";
import React from "react";

type Props = Readonly<{
  open: boolean;
  className?: string;
  children: React.ReactNode;
}>;

export function Expandable({ open, className, children }: Props) {
  return (
    <div
      className={cn(
        "grid overflow-hidden transition-all duration-300",
        className,
        open ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
      )}
    >
      <div className="min-h-0">{children}</div>
    </div>
  );
}
