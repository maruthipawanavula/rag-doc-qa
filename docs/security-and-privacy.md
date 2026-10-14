# Security and Privacy

## Two-factor authentication (2FA)

Every user can enable two-factor authentication from **Profile →
Security → Two-factor authentication**. Lumen Desk supports authenticator
apps (TOTP) and hardware security keys (WebAuthn). Admins on Pro and
Enterprise plans can require 2FA for the whole workspace. Keep your
recovery codes somewhere safe: without them, a locked-out user needs an
admin to reset their 2FA.

## Single sign-on (SSO / SAML)

Pro and Enterprise workspaces can enforce SAML single sign-on with
identity providers such as Okta, Microsoft Entra ID, and Google
Workspace. When SSO is enforced, password login is disabled for all
users except one break-glass admin account. SCIM provisioning is
available on Enterprise.

## Encryption

Data is encrypted in transit with TLS 1.2 or higher and encrypted at
rest with AES-256. Attachments stored in Lumen Desk are kept in
SOC 2-audited object storage with per-workspace keys.

## Privacy and data handling

Lumen Desk is GDPR compliant: we sign a Data Processing Addendum on
request, store EU customer data in EU regions when the workspace region
is set to EU, and never sell customer data or use it to train third-party
models. Conversation data is retained while your workspace is active;
after you close a workspace, data is permanently deleted within 30 days,
except invoices which tax law requires us to keep for 7 years.

## Certifications and subprocessors

Lumen Desk undergoes an annual SOC 2 Type II audit. A current list of
subprocessors (hosting, email delivery, error tracking) is published on
our trust page and updated at least 30 days before any change takes
effect.
