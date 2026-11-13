# Nivas Hostel Manager

| Folder or file | What it is |
|---|---|
| `publish/` | **Upload this folder** to your host. It is the whole app. |
| `nivas-demo.html` | One-file demo with sample data. Open it in any browser. Not for publishing. |
| `server-optional/` | Old Razorpay starter. Not used by the app. Do not upload. |

## Publish in 4 steps
1. **Firebase:** console.firebase.google.com, create a project. Authentication, Sign-in method: turn on Email/Password, Google, Apple (Apple needs a paid Apple Developer account) and **Email link (passwordless sign-in)**. The last one is needed for Delete account.
2. **Settings:** open `publish/config.js`. Paste your Firebase web config into `firebase`, set `site` to your hosted address with a trailing slash (for example `https://yourname.github.io/nivas/`), and check the `support` and `publisher` details.
3. **Host:** upload everything inside `publish/` to GitHub Pages or Firebase Hosting (HTTPS is required). In Firebase, Authentication, Settings, Authorized domains: add your domain.
4. **Test:** sign up, verify the email, add a hostel and a customer, record a payment and send the receipt to your own number.

## Pages for Play Store and App Store
After hosting, these addresses are public and need no sign-in:
- `https://your-site/privacy.html`
- `https://your-site/terms.html`
- `https://your-site/delete-account.html` (use this as the "account deletion URL" in Google Play)

## Receipts
After a payment, the app opens WhatsApp or the SMS app with a short message and a link. When the customer opens the link, the PDF (same layout as the printed hostel receipt) is made in their browser and downloads. Nothing is stored on a server, so a link works as long as your site is hosted. Anyone with the link can read that receipt. For tamper-proof receipts store each bill in Firestore and check it when the link opens. Names in Telugu print correctly if the customer's phone has a Telugu font (most do).

## Payment details
UPI QR scan (camera or photo), manual UPI ID, and manual bank account. Checks: UPI format and common handles, account number length and made-up patterns, holder name, and the IFSC is looked up live in Razorpay's public list. Only a bank can prove ownership of an account, so ask owners to send themselves Rs. 1.

## Download data (Excel and PDF)
Profile, Download my data (also buttons on Residents and Saved bills). Choose Bills, Residents, Payments due, My hostels or Everything, and optionally one hostel. Excel has one styled sheet per list (blue header, borders, frozen header, filters, rupee format, totals, print-ready landscape). The PDF is landscape A4 with a title, date, totals and page numbers. Files are made on the phone and never uploaded. UPI and bank details are not included. The Excel and table libraries load from cdnjs the first time someone downloads.

## Delete account
Profile, Delete account, type DELETE, then confirm using the link emailed to the owner. The link ends with `?del=1` and deletes the Firebase account and the data saved on that device.

## Where data is stored
Hostels, residents, bills and payment details are saved in the owner's browser on their device (key `nivas:<uid>`). Moving them to Firestore is a later step; if you do, update the Privacy Policy first.

## Legal pages
The text is in `index.html` (app) and in `privacy.html`, `terms.html`, `delete-account.html`. The name, email and date come from `config.js`. Have a lawyer review the policies before launch. The DPDP Rules, 2025 duties become enforceable on 13 May 2027, and Hyderabad police and GHMC rules for hostels were updated in July 2026, so re-check both from time to time.

## Sign-in setup (Google, Apple, email link reset)
Sign-in works as soon as the four Firebase values in `publish/config.js` are filled in (apiKey, authDomain, projectId, appId) and your site address is added under Firebase, Authentication, Settings, Authorized domains. Until then the app shows a friendly message and the Preview button. "Forgot password?" sends a reset link to the owner's email through Firebase.

## Receipts
Each receipt link opens a white-paper receipt in the same layout as the printed hostel book, with Download PDF and Print buttons. The bill shows the hostel name, address and contact numbers saved in My hostels. Wrong data (phone, name, amounts, etc.) is marked in red under the field.


## v7.3: clean Apple-style look
- Flat white grouped cards on a light grey background with hairline borders. No glass, blur, gradients or decorative banner. The dashboard now starts with the greeting, quick actions and figures; recording a payment is the blue + button or the Payment shortcut.

## v7.1: what is new
- **Cloud sync (Firestore).** After sign-in each owner's data syncs to one private document `owners/{uid}`. Local data is kept, uploaded on first sync, and backed up locally before anything is replaced. If cloud and device both changed, the app asks which to keep. A small status label shows Saving / Synced / Offline / Retry.
- **Strict rules:** `firestore.rules` (owner-only, verified email, field types, size, rev must rise by 1, everything else denied).
- **Account deletion** deletes the cloud document first, then the login, then local data.
- **Online payments are disabled.** The old Razorpay server was unsafe and is replaced by a stub.
- **Close (X) button** on every sheet, picker, alert and sub-screen. **Tab bar has 5 buttons:** Home, Hostels, +, Residents, Payments. Profile is the round avatar at the top.
- Security headers and a Report-Only CSP are in `firebase.json`.

## Set up (about 15 minutes)
1. Firebase console: create a project, add a Web app, paste its config into `publish/config.js`.
2. Authentication: enable Email/Password, Email link and Google. Add your domain under Authorized domains.
3. Firestore: create a database, then `firebase deploy --only firestore:rules`.
4. `firebase deploy --only hosting` (serves `publish/` over HTTPS).
5. Set `site` in `config.js` to your hosted address.
6. Enable Firestore scheduled backups in the Google Cloud console.

## Tests (`tests/`)
`python3 tests/xss_regression.py <path to nivas-demo.html>` and `python3 tests/sync_mock_test.py` (need Playwright). `firestore.rules.test.js` has not been run.
