const express = require('express');
const { WorkOS } = require('@workos-inc/node');

const app = express();
const port = 3000;

app.use(express.json());

const workos = new WorkOS(process.env.WORKOS_API_KEY);
const clientId = process.env.WORKOS_CLIENT_ID;

app.post('/api/magic-link', async (req, res) => {
  try {
    const { email } = req.body;
    const session = await workos.userManagement.createMagicAuth({ email });
    res.json({ code: session.code });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/verify', async (req, res) => {
  try {
    const { email, code } = req.body;
    const response = await workos.userManagement.authenticateWithMagicAuth({
      clientId,
      code,
    });
    res.json(response.user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
