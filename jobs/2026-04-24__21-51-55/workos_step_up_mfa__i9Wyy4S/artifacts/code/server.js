const express = require("express");
const { WorkOS } = require("@workos-inc/node");

const app = express();
app.use(express.json());

const workos = new WorkOS(process.env.WORKOS_API_KEY);

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.post("/enroll", async (req, res) => {
  try {
    const { email, issuer } = req.body;
    const factor = await workos.mfa.enrollFactor({
      type: "totp",
      issuer: issuer,
      user: email,
    });
    
    res.json({
      factorId: factor.id,
      secret: factor.totp.secret,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post("/challenge", async (req, res) => {
  try {
    const { factorId } = req.body;
    const challenge = await workos.mfa.challengeFactor({
      authenticationFactorId: factorId,
    });
    
    res.json({
      challengeId: challenge.id,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post("/verify", async (req, res) => {
  try {
    const { challengeId, code } = req.body;
    const verify = await workos.mfa.verifyChallenge({
      authenticationChallengeId: challengeId,
      code: code,
    });
    
    res.json({
      valid: verify.valid,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
