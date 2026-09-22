/**
 * Student enrollment commerce config (public, client-side).
 *
 * HONEST STATUS: Payments are INACTIVE until Enmanuel pastes live Stripe Payment Link
 * and/or PayPal URLs below and sets enabled: true. No Stripe secret keys belong here
 * or anywhere else in this static repo — Payment Links only.
 *
 * After editing: commit, push, and wait for Cloudflare Workers Assets deploy.
 * See /ops/payments.md and /admin/.
 */
window.IL_ENROLL = {
  currency: "USD",
  paymentsLive: false, // flip to true only after live links are pasted and tested
  disclaimer:
    "Checkout links are placeholders. Card and PayPal signup stay inactive until the operator pastes live Payment Link / PayPal URLs into this file and redeploys.",
  tiers: [
    {
      id: "prep-sprint",
      name: "Prep Sprint",
      badge: "Interview crush",
      blurb:
        "Guided access framing for the BNY-aimed 3-phase prep track (math → programming → DevOps + drills). Study path — not employment.",
      publishablePrice: "$149",
      period: "one-time",
      features: [
        "Prep hub syllabus map",
        "Interview drill packs pointer",
        "Email kickoff from operator (manual until webhooks)",
      ],
      stripeEnabled: false,
      paypalEnabled: false,
      stripePaymentLink: "https://buy.stripe.com/PLACEHOLDER_PREP_SPRINT",
      paypalLink: "https://www.paypal.com/ncp/payment/PLACEHOLDER_PREP_SPRINT",
    },
    {
      id: "devsecops-mastery",
      name: "DevSecOps Mastery",
      badge: "12-month path",
      blurb:
        "Long curriculum framing: BU/NSCC/KodeKloud + AZ-104 / AZ-400 / CKA / CKS. Cross-links Prep — does not duplicate the sprint.",
      publishablePrice: "$499",
      period: "one-time",
      features: [
        "Mastery path checkpoints",
        "Cert ladder checklist",
        "Monthly check-in slot (operator-scheduled)",
      ],
      stripeEnabled: false,
      paypalEnabled: false,
      stripePaymentLink: "https://buy.stripe.com/PLACEHOLDER_DEVSECOPS_MASTERY",
      paypalLink: "https://www.paypal.com/ncp/payment/PLACEHOLDER_DEVSECOPS_MASTERY",
    },
    {
      id: "full-academy",
      name: "Full Academy",
      badge: "Bundle",
      blurb:
        "Prep Sprint + DevSecOps Mastery + paths hub orientation (DS certs, NVIDIA free AI, FDE stub when imported). Best if you want the whole static KOS surface.",
      publishablePrice: "$799",
      period: "one-time",
      features: [
        "All Prep + Mastery framing",
        "Paths hub walkthrough",
        "Priority operator reply window",
      ],
      stripeEnabled: false,
      paypalEnabled: false,
      stripePaymentLink: "https://buy.stripe.com/PLACEHOLDER_FULL_ACADEMY",
      paypalLink: "https://www.paypal.com/ncp/payment/PLACEHOLDER_FULL_ACADEMY",
    },
  ],
};
