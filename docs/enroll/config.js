/**
 * Student enrollment commerce config (public, client-side).
 *
 * HONEST STATUS: Payments are INACTIVE until Enmanuel pastes live Stripe Payment Link
 * and/or PayPal URLs below and sets enabled: true. No Stripe secret keys belong here
 * or anywhere else in this static repo — Payment Links only.
 *
 * GOING LIVE (the only steps he must do — nothing else):
 *   1. Create one Stripe Payment Link per tier (or one PayPal payment link per tier).
 *   2. Paste the three live URLs into stripePaymentLink / paypalLink below.
 *   3. Set stripeEnabled / paypalEnabled true for each tier with a live link.
 *   4. Flip paymentsLive to true.
 *   5. Commit, deploy, and complete one real test purchase per tier, then refund it.
 *
 * After editing: commit, push, and wait for Cloudflare Workers Assets deploy.
 */
window.IL_ENROLL = {
  currency: "USD",
  paymentsLive: false,
  // Flip paymentsLive to true only after live links are pasted and tested.
  disclaimer:
    "Checkout opens soon — join the waitlist and we'll email you the moment seats go live.",
  tiers: [
    {
      id: "prep-sprint",
      name: "Prep Sprint",
      badge: "Interview prep",
      blurb:
        "The complete interview-prep track: a structured 3-phase study plan (math, programming, DevOps) plus timed drill packs built from real question banks. A study path — not employment, no placement.",
      publishablePrice: "$149",
      period: "one-time",
      features: [
        "3-phase prep syllabus: math, programming, DevOps",
        "Timed interview drill packs with real question banks",
        "Personal onboarding email from the founder",
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
        "The 52-week DevSecOps path: foundations, platform and cloud, then Kubernetes plus security — with weekly build artifacts, SuperLab hardening loops, Adapt gates, and Noah side-quests on every phase. Maps your study to AZ-104 / AZ-400 / CKA / CKS exam shapes. Honest third-party prep: no vendor affiliation, no exam vouchers bundled.",
      publishablePrice: "$499",
      period: "one-time",
      features: [
        "52-week phased curriculum with weekly build artifacts",
        "SuperLab hardening loops and Adapt gates on every phase",
        "AZ-104 / AZ-400 / CKA / CKS exam-shape mapping (prep only, no vouchers)",
        "Monthly check-in with the founder",
      ],
      stripeEnabled: false,
      paypalEnabled: false,
      stripePaymentLink: "https://buy.stripe.com/PLACEHOLDER_DEVSECOPS_MASTERY",
      paypalLink: "https://www.paypal.com/ncp/payment/PLACEHOLDER_DEVSECOPS_MASTERY",
    },
    {
      id: "full-academy",
      name: "Full Academy",
      badge: "Everything",
      blurb:
        "Prep Sprint plus DevSecOps Mastery, with orientation across the whole knowledge OS: ten academies, five deep tracks, 68 certification bootcamps, role tracks, and labs. One payment for the full surface.",
      publishablePrice: "$799",
      period: "one-time",
      features: [
        "Everything in Prep Sprint and DevSecOps Mastery",
        "Full catalog orientation: 10 academies, 5 deep tracks, 68 bootcamps",
        "Priority reply window with the founder",
      ],
      stripeEnabled: false,
      paypalEnabled: false,
      stripePaymentLink: "https://buy.stripe.com/PLACEHOLDER_FULL_ACADEMY",
      paypalLink: "https://www.paypal.com/ncp/payment/PLACEHOLDER_FULL_ACADEMY",
    },
  ],
};
