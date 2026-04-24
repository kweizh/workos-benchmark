const express = require("express");
const { WorkOS } = require("@workos-inc/node");

const app = express();
app.use(express.json());

const workos = new WorkOS(process.env.WORKOS_API_KEY);

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.post("/enroll", async (req, res) => {
  const { email, issuer } = req.body;
  try {
    const factor = await workos.mfa.enrollFactor({
      type: "totp",
      totpIssuer: issuer,
      totpUser: email,
    });
    res.json({
      factorId: factor.id,
      secret: factor.totp.secret,
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.post("/challenge", async (req, res) => {
  const { factorId } = req.body;
  try {
    const challenge = await workos.mfa.challengeFactor({
      authenticationFactorId: factorId,
    });
    res.json({
      challengeId: challenge.id,
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.post("/verify", async (req, res) => {
  const { challengeId, code } = req.body;
  try {
    const response = await workos.mfa.verifyChallenge({
      authenticationChallengeId: challengeId,
      code,
    });
    res.json({
      valid: response.valid,
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
