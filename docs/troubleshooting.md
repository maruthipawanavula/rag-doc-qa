# Troubleshooting

## Emails are not syncing into the inbox

If new emails stopped arriving, check these in order:

1. Open **Settings → Inboxes** and look for a red "connection broken"
   badge. OAuth connections to Google and Microsoft sometimes need to be
   re-authorized after a password change — click **Reconnect**.
2. If you use forwarding, send a test message to your forwarding address
   and confirm your mail provider's forwarding rule is still enabled.
3. Check the customer's spam or quarantine folder on your own mail
   server; messages flagged there never reach Lumen Desk.

Most sync problems are reconnect issues: about 8 out of 10 cases are
fixed by re-authorizing the mailbox connection.

## Notifications are not arriving

Desktop and mobile notifications are controlled per user under
**Profile → Notifications**. If notifications stopped after working
before, check that your browser or phone has not revoked the site's
notification permission, and that your workspace admin has not enabled
the "quiet hours" setting for your team. Slack notifications have their
own toggle under **Settings → Integrations → Slack**.

## Search feels slow or returns wrong results

Search indexes new conversations within 2 minutes. If a recent
conversation is missing from search, wait a few minutes and try again.
For very large workspaces (over 500,000 conversations), use filters —
status, inbox, date range — before typing keywords; filtered searches
run against a smaller index and return noticeably faster.

## Contact import failed or skipped rows

After every CSV import you receive an email report. Rows are skipped
when the email address is invalid, the row is a duplicate of an existing
contact, or required columns are missing. Download the error report from
the import history, fix the rows, and re-import just those rows —
duplicates are safely ignored on the second pass.

## The app shows a blank page or keeps logging me out

Clear your browser cache and cookies for your workspace subdomain, then
sign in again. If you use a strict tracking-prevention browser setting,
allow cookies for `*.lumendesk.app`: the session cookie is required for
login. Still stuck? Try an incognito window to rule out extensions —
ad blockers and script blockers are the most common cause of a blank
page.
