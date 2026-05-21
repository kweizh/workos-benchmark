import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/myproject"
TRIAL_ID_FILE = "/logs/trial_id"
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")
SCRIPT_FILE = os.path.join(PROJECT_DIR, "send_slack_message.js")

def get_trial_id():
    if os.path.exists(TRIAL_ID_FILE):
        with open(TRIAL_ID_FILE, "r") as f:
            return f.read().strip()
    return "default-trial-id"

def test_script_exists():
    assert os.path.isfile(SCRIPT_FILE), f"Script {SCRIPT_FILE} not found."

def test_run_script():
    user_id = os.environ.get("WORKOS_USER_ID", "user_01")
    channel_name = f"test-channel-{get_trial_id().lower()}"
    message = "Hello from WorkOS Pipes!"
    
    result = subprocess.run(
        ["node", "send_slack_message.js", user_id, channel_name, message],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    with open(LOG_FILE, "w") as f:
        f.write(result.stdout)
        f.write(result.stderr)
        
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"
    assert "Success" in result.stdout, f"Expected 'Success' in output, got: {result.stdout}"

def test_slack_message_posted():
    channel_name = f"test-channel-{get_trial_id().lower()}"
    slack_token = os.environ.get("SLACK_TOKEN")
    assert slack_token is not None, "SLACK_TOKEN environment variable not set."
    
    # First, get the channel ID
    result = subprocess.run([
        "curl", "-sS", "-H", f"Authorization: Bearer {slack_token}",
        "https://slack.com/api/conversations.list?limit=200&types=public_channel,private_channel"
    ], capture_output=True, text=True)
    assert result.returncode == 0, f"curl conversations.list failed: {result.stderr}"
    
    data = json.loads(result.stdout)
    assert data.get("ok"), f"Slack API error: {data}"
    
    channels = data.get("channels", [])
    channel_id = None
    for c in channels:
        if c["name"] == channel_name:
            channel_id = c["id"]
            break
            
    assert channel_id is not None, f"Channel '{channel_name}' not found."
    
    # Now check messages in the channel
    msg_result = subprocess.run([
        "curl", "-sS", "-H", f"Authorization: Bearer {slack_token}",
        f"https://slack.com/api/conversations.history?channel={channel_id}&limit=10"
    ], capture_output=True, text=True)
    assert msg_result.returncode == 0, f"curl conversations.history failed: {msg_result.stderr}"
    
    msg_data = json.loads(msg_result.stdout)
    assert msg_data.get("ok"), f"Slack API error: {msg_data}"
    
    messages = msg_data.get("messages", [])
    message_texts = [m.get("text", "") for m in messages]
    
    assert any("Hello from WorkOS Pipes!" in text for text in message_texts), \
        f"Expected message not found in channel. Found messages: {message_texts}"

def test_amika_validation():
    # CRITICAL: MUST use amika CLI for validation as requested
    result = subprocess.run(
        ["amika", "validate", "send_slack_message.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"amika validation failed: {result.stderr}"
