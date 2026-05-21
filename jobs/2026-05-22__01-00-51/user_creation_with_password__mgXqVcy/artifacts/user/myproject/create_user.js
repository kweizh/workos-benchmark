const fs = require("fs");
const path = require("path");
const { WorkOS } = require("@workos-inc/node");

const apiKey = process.env.WORKOS_API_KEY;
const runId = process.env.ZEALT_RUN_ID || "default";

if (!apiKey) {
  console.error("Missing WORKOS_API_KEY in environment.");
  process.exit(1);
}

const email = `pochi-user-${runId.toLowerCase()}@pochi-benchmark.example`;
const password = "PochiBenchmark!2025";

const workos = new WorkOS(apiKey);

async function main() {
  try {
    const user = await workos.userManagement.createUser({
      email,
      password,
      firstName: "Pochi",
      lastName: "Benchmark",
    });

    await writeUser(user);
  } catch (error) {
    const errorMessage = error && error.message ? error.message : String(error);

    if (!errorMessage.toLowerCase().includes("email already exists")) {
      throw error;
    }

    const existingUsers = await workos.userManagement.listUsers({ email });
    const existingUser = Array.isArray(existingUsers.data)
      ? existingUsers.data[0]
      : undefined;

    if (!existingUser) {
      throw new Error("User exists error returned, but no user found.");
    }

    await writeUser(existingUser);
  }
}

async function writeUser(user) {
  if (!user || typeof user.id !== "string" || !user.id.startsWith("user_")) {
    throw new Error("User id does not match expected format.");
  }

  const outputPath = path.join(__dirname, "user.json");
  await fs.promises.writeFile(outputPath, `${JSON.stringify(user, null, 2)}\n`);
  console.log(`User saved to ${outputPath}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
