# Security and functional report, v7.1

Only items marked TESTED were run. Nothing was tested against a live Firebase project, a real device or real payments.

| # | Issue found | Severity | Why dangerous | Change | Verification |
|---|---|---|---|---|---|
| 1 | Server trusted the amount sent by the browser | Critical | Anyone could pay Rs 1 for a Rs 6,500 bill | Server disabled (503 for payments) | Code review only |
| 2 | Server bill endpoint had no ownership check | Critical | Any user could read another owner's bills (IDOR) | Removed with the server | Code review only |
| 3 | Bills kept in server memory, separate JWT secret | High | Data lost on restart; weak sessions | Removed | Code review only |
| 4 | Data only in one browser | High | Data loss, no multi-device | Firestore sync with rev check, backups, conflict dialog | TESTED against an in-memory mock (8 checks). NOT tested on real Firestore |
| 5 | No server-side access rules | High | Nothing protects cloud data | `firestore.rules` | NOT tested (emulator unavailable) |
| 6 | Duplicate receipt numbers, wrong "Send again" function, silent save failures | Medium | Wrong receipt opened; unseen data loss | Fixed in v6.1 | TESTED |
| 7 | Account deletion left cloud data | High | Would claim deletion while data remained | Cloud document deleted before login and local data | NOT tested on a real account |
| 8 | XSS via names, addresses, notes, receipts | High | Script runs in the owner's session | Existing escaping checked | TESTED: 0 executions on 11 screens and 9 dialogs; control payload fires when unescaped |
| 9 | No security headers | Medium | Clickjacking, mixed content | `firebase.json`; CSP in Report-Only | NOT tested |

## Not done
- Strong CSP: inline `onclick` handlers remain, so CSP allows `unsafe-inline` and is Report-Only.
- Rules cannot validate fields inside the JSON data blob; separate documents for hostels, residents and bills would. One document is limited to about 1 MB.
- Razorpay, webhooks, gateway-verified payments: not built. All payments are owner-recorded.
- Secure time-limited receipt links: not built.
- Not run: rules tests, dependency scan, accessibility audit, widths other than 280/360/390/820/1440, PDF/Excel/QR/camera/offline/PWA checks. Privacy and terms pages still describe v6 and must be updated before launch.
- Not production ready.
