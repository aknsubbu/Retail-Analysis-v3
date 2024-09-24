import React from "react";

import { ThemeToggle } from "./theme-toggle";

import { Separator } from "@/components/ui/separator";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Dock, DockIcon } from "@/components/magicui/dock";

// import { ModeToggle } from "@/components/mode-toggle";

export type IconProps = React.HTMLAttributes<SVGElement>;

export function DockDemo() {
  return (
    <div className="relative flex h-[100px] w-full flex-col items-center justify-center overflow-hidden rounded-lg min-w-[500px]">
      <TooltipProvider>
        <Dock direction="middle">
          <h1 className="text-2xl font-light p-5">
            {" "}
            AI-powered Retail Analytics
          </h1>
          <Separator
            className="h-full py-2 bg-gray-500"
            orientation="vertical"
          />
          <DockIcon>
            <Tooltip>
              <TooltipTrigger asChild>
                <ThemeToggle />
              </TooltipTrigger>
              <TooltipContent>
                <p>Theme</p>
              </TooltipContent>
            </Tooltip>
          </DockIcon>
        </Dock>
      </TooltipProvider>
    </div>
  );
}
