'use client';

import { CopilotChat } from "@/components/copilot-chat";
import { RequireAuth } from "@/components/RequireAuth";

const CopilotPageInner = () => {
  return <CopilotChat />;
};

export default function CopilotPage() {
  return <RequireAuth><CopilotPageInner /></RequireAuth>;
}