export type PoseDefinition = {
  poseId: string;
  aliases: string[];
  action?: string;
  phase?: string;
  handedness: "left" | "right" | "neutral";
  limbStates: Record<string, string>;
};

export const POSE_REGISTRY: PoseDefinition[] = [
  {
    poseId: "attack_x_prep_right",
    aliases: ["attack x prep", "preparing for attack x", "ready attack x"],
    action: "attack_x",
    phase: "prep",
    handedness: "right",
    limbStates: { right_hand: "up", left_leg: "back" }
  },
  {
    poseId: "idle_guard_right",
    aliases: ["guard stance", "idle guard"],
    action: "guard",
    phase: "idle",
    handedness: "right",
    limbStates: { right_hand: "mid", left_leg: "mid" }
  }
];

export class PoseResolutionError extends Error {}

const normalize = (text: string) => text.trim().toLowerCase().replace(/\s+/g, " ");

function extractConstraints(raw: string) {
  const text = normalize(raw);
  const limbStates: Record<string, string> = {};

  if ((/\bright hand\b.*\bup\b/.test(text)) || (/\bup\b.*\bright hand\b/.test(text))) limbStates.right_hand = "up";
  if ((/\bleft leg\b.*\bback\b/.test(text)) || (/\bback\b.*\bleft leg\b/.test(text))) limbStates.left_leg = "back";

  return {
    raw: text,
    action: text.includes("attack x") && text.includes("prepar") ? "attack_x" : undefined,
    phase: text.includes("attack x") && text.includes("prepar") ? "prep" : undefined,
    limbStates
  };
}

function similarity(a: string, b: string): number {
  if (a === b) return 1;
  const aSet = new Set(a.split(" "));
  const bSet = new Set(b.split(" "));
  let overlap = 0;
  for (const t of aSet) if (bSet.has(t)) overlap += 1;
  return overlap / Math.max(aSet.size, bSet.size, 1);
}

export function resolvePose(command: string, characterHandedness: "left" | "right" = "right") {
  const normalized = normalize(command);
  const constraints = extractConstraints(command);

  const ranked = POSE_REGISTRY.map((pose) => {
    let score = 0;

    if (normalized.startsWith("use pose ")) {
      const desired = normalized.slice("use pose ".length).trim();
      if (desired === pose.poseId) score += 1000;
      else if (pose.aliases.includes(desired)) score += 500;
    }

    if (constraints.action && constraints.action === pose.action) score += 150;
    if (constraints.phase && constraints.phase === pose.phase) score += 120;

    for (const [part, state] of Object.entries(constraints.limbStates)) {
      if (pose.limbStates[part] === state) score += 60;
    }

    for (const alias of pose.aliases) score += Math.floor(40 * similarity(normalized, alias));
    if (pose.handedness === characterHandedness || pose.handedness === "neutral") score += 25;

    return { poseId: pose.poseId, score, pose };
  }).sort((a, b) => (b.score - a.score) || a.poseId.localeCompare(b.poseId));

  if (!ranked.length || ranked[0].score < 140) {
    throw new PoseResolutionError("POSE_NOT_FOUND: No pose satisfies required constraints.");
  }

  return {
    poseId: ranked[0].poseId,
    score: ranked[0].score,
    constraints,
    candidates: ranked.map(({ poseId, score }) => ({ poseId, score }))
  };
}
