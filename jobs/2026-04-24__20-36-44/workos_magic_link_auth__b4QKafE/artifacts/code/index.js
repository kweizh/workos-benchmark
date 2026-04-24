const express = require('express');
const { WorkOS } = require('@workos-inc/node');

const app = express();
app.use(express.json());

const workos = new WorkOS(process.env.WORKOS_API_KEY);
const clientId = process.env.WORKOS_CLIENT_ID;

app.post('/api/magic-link', async (req, res) => {
  try {
    const { email } = req.body;
    if (!email) {
      return res.status(400).json({ error: 'Email is required' });
    }

    const magicAuth = await workos.userManagement.createMagicAuth({
      email,
    });

    res.json({ code: magicAuth.code });
  } catch (error) {
    console.error('Error creating magic auth:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/verify', async (req, res) => {
  try {
    const { email, code } = req.body;
    if (!email || !code) {
      return res.status(400).json({ error: 'Email and code are required' });
    }

    const { user } = await workos.userManagement.authenticateWithMagicAuth({
      clientId,
      email,
      code,
    });

    res.json(user);
  } catch (error) {
    console.error('Error verifying magic auth:', error);
    res.status(500).json({ error: error.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
