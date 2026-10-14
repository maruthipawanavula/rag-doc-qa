# Integrations

## Slack

Connect Slack from **Settings → Integrations → Slack** to get Lumen Desk
notifications in a channel: new conversations, mentions, and SLA breach
warnings. Agents can also create a conversation from any Slack message
with the `/lumendesk` slash command. Slack integration is available on
the Pro and Enterprise plans.

## Salesforce

The Salesforce integration shows the customer's account, open
opportunities, and recent cases in the sidebar of every conversation.
Sync is one-way from Salesforce to Lumen Desk and refreshes every 15
minutes. Available on Pro and Enterprise; a Salesforce admin must approve
the connected app in your org.

## Zapier and automation platforms

With Zapier you can push Lumen Desk events — new conversation,
conversation closed, customer reply — into 5,000+ other apps, or create
Lumen Desk conversations from form submissions and spreadsheets. Pick
Lumen Desk in Zapier and authenticate with an API key (see below).

## API keys and the developer API

Generate an API key under **Settings → Developers → API keys**. Keys are
scoped: choose read-only or full access, and rotate a key at any time —
rotating immediately revokes the old key. The REST API base URL is
`https://api.lumendesk.app/v2`. Rate limits are 600 requests per minute
per workspace on Pro and 2,400 on Enterprise.

## Webhooks

Webhooks send an HTTPS POST with a JSON payload whenever selected events
happen: `conversation.created`, `conversation.replied`,
`conversation.closed`, and `customer.created`. Configure endpoints under
**Settings → Developers → Webhooks**. Each delivery is signed with your
webhook secret (HMAC-SHA256) so you can verify it came from Lumen Desk.
Failed deliveries retry with exponential backoff for 24 hours.
