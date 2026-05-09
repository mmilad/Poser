import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { PoseResolutionError, resolvePose } from "@/lib/poseResolver";

const requestSchema = z.object({
  text: z.string().min(1),
  characterHandedness: z.enum(["left", "right"]).default("right")
});

export async function POST(request: NextRequest) {
  const payload = requestSchema.parse(await request.json());
  try {
    return NextResponse.json(resolvePose(payload.text, payload.characterHandedness));
  } catch (error) {
    if (error instanceof PoseResolutionError) {
      return NextResponse.json({ detail: error.message }, { status: 422 });
    }
    throw error;
  }
}
